#!/usr/bin/env python3
"""同步 GitHub 星标仓库 -> 分类 -> 重新生成文档。

用法：
    GH_TOKEN=xxx python scripts/sync.py          # 正常同步（Actions 里就是这个）
    python scripts/sync.py --public <用户名>      # 无 token，只读公开星标
    python scripts/sync.py --use-cache           # 不请求接口，用 data/releases.json 重渲染
    python scripts/sync.py --demo                # 用示例数据看排版效果

产物：
    README.md / docs/*.md            总览与各维度清单
    apps/<分类>/README.md             分类索引（含每个应用的最新版本）
    apps/<分类>/<应用>/README.md       应用详情（版本 + 更新说明 + 安装包直链）
    data/stars.json                  星标快照，用来算「新增 / 取消」
    data/releases.json               版本信息缓存，接口失败时兜底

环境变量：
    GH_TOKEN        必填。Classic PAT，只需 read:user 权限
    NEW_DAYS        可选。🆕 标记的天数窗口，默认 14
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

def _write(path: Path, content: str) -> None:
    """总是写 LF，避免 Windows 本地跑完、Actions 跑完出现换行差异。"""
    path.write_text(content, encoding="utf-8", newline="\n")


import pages  # noqa: E402
import releases  # noqa: E402
import render  # noqa: E402
from classifier import apply_override, build_lookup, classify, load_rules  # noqa: E402

TZ = timezone(timedelta(hours=8))
API = "https://api.github.com"
PER_PAGE = 100
MAX_PAGES = 300
NEW_DAYS = int(os.environ.get("NEW_DAYS", "14"))
RELEASE_DAYS = int(os.environ.get("RELEASE_DAYS", "7"))
SKIP_RELEASES = os.environ.get("SKIP_RELEASES", "").lower() in ("1", "true", "yes")

SNAPSHOT = ROOT / "data" / "stars.json"
UNCLASSIFIED = ROOT / "data" / "unclassified.json"
RELEASE_CACHE = ROOT / "data" / "releases.json"
RULES = ROOT / "config" / "rules.toml"
OVERRIDES = ROOT / "config" / "overrides.toml"
APPS_DIR = ROOT / "apps"


def log(*args) -> None:
    print(*args, flush=True)


# ------------------------------------------------------------------ GitHub API


def gh_get(url: str, token: str | None) -> tuple[list | dict, dict]:
    headers = {
        "Accept": "application/vnd.github.star+json, application/vnd.github+json",
        "User-Agent": "starred-hub-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(3):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.load(resp), dict(resp.headers)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:400]
            if e.code in (403, 429) and attempt < 2:
                reset = e.headers.get("X-RateLimit-Reset")
                wait = 60
                if reset:
                    wait = max(5, min(180, int(reset) - int(time.time()) + 3))
                log(f"  ! 触发限流，{wait}s 后重试（第 {attempt + 1} 次）")
                time.sleep(wait)
                continue
            if e.code == 401:
                raise SystemExit("Token 无效或已过期，请重新生成后更新 Secrets.STARS_TOKEN")
            if e.code == 404:
                raise SystemExit(f"资源不存在：{url}")
            raise SystemExit(f"GitHub API {e.code}: {body}")
        except urllib.error.URLError as e:
            if attempt < 2:
                log(f"  ! 网络错误 {e.reason}，5s 后重试")
                time.sleep(5)
                continue
            raise SystemExit(f"网络不可用：{e.reason}")
    raise SystemExit("GitHub API 连续失败")


def normalize(item: dict) -> dict:
    repo = item.get("repo") if isinstance(item.get("repo"), dict) else item
    owner = (repo.get("owner") or {}).get("login") or repo["full_name"].split("/")[0]
    return {
        "full_name": repo["full_name"],
        "name": repo.get("name") or repo["full_name"].split("/")[-1],
        "owner": owner,
        "html_url": repo.get("html_url") or f"https://github.com/{repo['full_name']}",
        "description": (repo.get("description") or "").strip(),
        "homepage": repo.get("homepage") or "",
        "language": repo.get("language") or "",
        "stars": repo.get("stargazers_count") or 0,
        "forks": repo.get("forks_count") or 0,
        "topics": repo.get("topics") or [],
        "license": (repo.get("license") or {}).get("spdx_id") or "",
        "archived": bool(repo.get("archived")),
        "pushed_at": repo.get("pushed_at") or "",
        "starred_at": item.get("starred_at") or repo.get("starred_at") or "",
    }


def fetch_starred(token: str | None, login: str | None) -> tuple[list[dict], str]:
    repos: list[dict] = []
    page = 1
    while page <= MAX_PAGES:
        if login:
            url = f"{API}/users/{login}/starred?per_page={PER_PAGE}&page={page}"
        else:
            url = f"{API}/user/starred?per_page={PER_PAGE}&page={page}&sort=created&direction=desc"
        data, _ = gh_get(url, token)
        if not isinstance(data, list) or not data:
            break
        repos.extend(normalize(it) for it in data)
        log(f"  已拉取 {len(repos)} 个仓库…")
        if len(data) < PER_PAGE:
            break
        page += 1
    if not login:
        me, _ = gh_get(f"{API}/user", token)
        login = (me or {}).get("login") or "unknown"
    return repos, login or "unknown"


# ------------------------------------------------------------------ 快照


def load_snapshot() -> dict:
    if not SNAPSHOT.exists():
        return {"repos": {}, "recently_removed": []}
    try:
        data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        log("  ! 旧快照读取失败，按首次同步处理")
        return {"repos": {}, "recently_removed": []}
    data.setdefault("repos", {})
    data.setdefault("recently_removed", [])
    return data


def load_overrides() -> dict:
    if not OVERRIDES.exists():
        return {}
    import tomllib

    raw = tomllib.loads(OVERRIDES.read_text(encoding="utf-8"))
    return {k.lower(): v for k, v in (raw.get("repos") or {}).items()}


# ------------------------------------------------------------------ 目录名


def assign_dirs(groups: list[tuple[dict, list[dict]]]) -> None:
    """同一分类下如果重名（比如两个人都叫 utils），用 owner 前缀区分。"""
    for _cat, items in groups:
        used: set[str] = set()
        for repo in items:
            name = pages.app_dir_name(repo)
            if name in used:
                name = pages.safe_name(f"{repo['owner']}-{repo['name']}")
            n = 2
            base = name
            while name in used:
                name = f"{base}-{n}"
                n += 1
            used.add(name)
            repo["dir"] = name


def demo_releases(repos: list[dict]) -> None:
    """预览模式：造几条假版本数据，只为看排版。"""
    now = datetime.now(TZ)
    for i, repo in enumerate(sorted(repos, key=lambda r: r["full_name"])):
        if i % 4 == 3:
            repo["rel"] = {"kind": "none", "tag": "", "assets": []}
            continue
        repo["rel"] = {
            "kind": "release",
            "tag": f"v{(i % 3) + 1}.{i % 9}.{i % 5}",
            "title": f"Release {(i % 3) + 1}.{i % 9}.{i % 5}",
            "published_at": (now - timedelta(days=i * 3 % 90)).isoformat(timespec="seconds"),
            "url": f"{repo['html_url']}/releases",
            "prerelease": False,
            "body": "· 修复若干已知问题\n· 优化启动速度\n· 适配新版系统",
            "assets": [
                {"name": f"{repo['name']}-win-x64-setup.exe", "size": 24_000_000, "downloads": 1200 * (i + 1), "url": repo["html_url"]},
                {"name": f"{repo['name']}-macOS-universal.dmg", "size": 31_000_000, "downloads": 800 * (i + 1), "url": repo["html_url"]},
                {"name": f"{repo['name']}-linux-amd64.AppImage", "size": 40_000_000, "downloads": 300 * (i + 1), "url": repo["html_url"]},
            ],
        }
        repo["rel"]["checked_at"] = now.isoformat(timespec="seconds")


def prune_apps(keep: set[Path]) -> int:
    """删掉上次生成、这次已经不存在的应用页（只动带生成标记的文件）。"""
    if not APPS_DIR.exists():
        return 0
    removed = 0
    for path in sorted(APPS_DIR.rglob("*.md"), reverse=True):
        if path in keep:
            continue
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:200]
        except OSError:
            continue
        if not head.startswith(pages.MARKER):
            continue
        path.unlink()
        removed += 1
    for path in sorted(APPS_DIR.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    return removed


# ------------------------------------------------------------------ 主流程


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="同步 GitHub 星标并生成分类文档")
    ap.add_argument("--public", metavar="LOGIN", help="不给 token，读取该用户的公开星标")
    ap.add_argument("--demo", action="store_true", help="用内置示例数据生成预览，不联网")
    ap.add_argument("--use-cache", action="store_true", help="不请求 Release 接口，复用 data/releases.json")
    args = ap.parse_args(argv)

    started = time.time()
    synced_at = datetime.now(TZ)

    if args.demo:
        from demo_data import DEMO_RAW

        log("== 预览模式：使用示例数据 ==")
        repos = [normalize_raw(x) for x in DEMO_RAW]
        login = "your-name"
        prev = {"repos": {}, "recently_removed": []}
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or os.environ.get("STARS_TOKEN")
        if not token and not args.public:
            raise SystemExit(
                "缺少 GH_TOKEN。\n"
                "  Actions 里：Settings -> Secrets -> 新建 STARS_TOKEN\n"
                "  本地运行：GH_TOKEN=xxx python scripts/sync.py\n"
                "  只想看排版：python scripts/sync.py --demo"
            )
        log(f"== 开始同步（{'公开模式' if args.public else 'Token 模式'}）==")
        repos, login = fetch_starred(token if not args.public else None, args.public)
        prev = load_snapshot()

    log(f"账号：{login} · 共 {len(repos)} 个星标仓库")

    # ---- 分类
    rules = load_rules(RULES)
    lookup = build_lookup(rules)
    overrides = load_overrides()

    fallback_platform = "unknown"
    fallback_function = "other"
    unclassified = []

    for repo in repos:
        cls = classify(repo, rules, fallback_platform, fallback_function)
        cls = apply_override(repo, cls, overrides.get(repo["full_name"].lower()), lookup, warn=log)
        repo["cls"] = cls
        if cls["primary_function"] == fallback_function or cls["primary_platform"] == fallback_platform:
            unclassified.append(
                {
                    "full_name": repo["full_name"],
                    "description": repo["description"][:80],
                    "topics": repo["topics"][:8],
                }
            )

    # ---- 与旧快照对比
    prev_repos = prev.get("repos") or {}
    now_iso = synced_at.isoformat(timespec="seconds")
    for repo in repos:
        old = prev_repos.get(repo["full_name"])
        repo["first_seen"] = (old or {}).get("first_seen") or now_iso

    current_names = {r["full_name"] for r in repos}
    removed = list(prev.get("recently_removed") or [])
    for full_name, old in prev_repos.items():
        if full_name not in current_names:
            removed.append(
                {
                    "full_name": full_name,
                    "html_url": old.get("html_url") or f"https://github.com/{full_name}",
                    "description": old.get("description") or "",
                    "removed_at": now_iso,
                }
            )
    removed = removed[-60:]

    # ---- 最新版本
    if args.demo:
        demo_releases(repos)
        log("== 预览模式：使用假版本数据 ==")
    elif args.use_cache:
        log("== 复用本地版本缓存，不请求接口 ==")
        cached = releases.load_cache(RELEASE_CACHE)
        for repo in repos:
            repo["rel"] = cached.get(repo["full_name"]) or {"kind": "none", "tag": "", "assets": []}
    elif SKIP_RELEASES:
        log("== 跳过版本检查（SKIP_RELEASES=1）==")
        for repo in repos:
            repo["rel"] = {"kind": "none", "tag": "", "assets": []}
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or os.environ.get("STARS_TOKEN")
        log(f"== 检查 {len(repos)} 个仓库的最新版本 ==")
        stat = releases.enrich(repos, token if not args.public else None, RELEASE_CACHE)
        log(
            f"  Release {stat.get('release', 0)} · 仅 tag {stat.get('tag', 0)} · 无版本 {stat.get('none', 0)}"
            f" · 沿用缓存 {stat.get('cached', 0)} · 耗时 {stat.get('seconds')}s"
        )
        releases.save_cache(repos, RELEASE_CACHE)

    # ---- 渲染
    ctx = {
        "login": login,
        "synced_at": synced_at,
        "repos": repos,
        "removed": list(reversed(removed)),
        "rules": rules,
        "new_days": NEW_DAYS,
        "release_days": RELEASE_DAYS,
    }
    order_function = [c.slug for c in rules["function"]]
    fn_groups = render.group_by(repos, "functions", order_function, primary=True)
    assign_dirs(fn_groups)

    files = render.render_all(ctx)
    files.update(pages.plan(ctx, fn_groups))

    out_dir = ROOT if not args.demo else ROOT / ".preview"
    keep: set[Path] = set()
    for rel, content in files.items():
        path = out_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _write(path, content.rstrip() + "\n")
        keep.add(path)
    log(f"  写入 {len(files)} 个 Markdown 文件（含 apps/ 目录树）")
    if not args.demo:
        gone = prune_apps(keep)
        if gone:
            log(f"  清理 {gone} 个已失效的应用页")

    # ---- 快照
    snapshot = {
        "user": login,
        "synced_at": now_iso,
        "count": len(repos),
        "repos": {
            r["full_name"]: {
                "html_url": r["html_url"],
                "name": r["name"],
                "description": r["description"],
                "language": r["language"],
                "stars": r["stars"],
                "topics": r["topics"],
                "archived": r["archived"],
                "starred_at": r["starred_at"],
                "first_seen": r["first_seen"],
            }
            for r in repos
        },
        "recently_removed": removed,
    }
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    if not args.demo:
        _write(SNAPSHOT, json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        _write(
            UNCLASSIFIED,
            json.dumps(sorted(unclassified, key=lambda x: x["full_name"]), ensure_ascii=False, indent=2) + "\n",
        )

    # ---- 小结
    new_count = sum(
        1
        for r in repos
        if r.get("starred_at")
        and (synced_at - datetime.fromisoformat(r["starred_at"].replace("Z", "+00:00"))).days <= NEW_DAYS
    )
    log("")
    log(f"完成：{len(repos)} 个仓库 · 🆕 {new_count} 个（{NEW_DAYS} 天内） · 取消 {len(removed)} 个 · 待归类 {len(unclassified)} 个")
    log(f"耗时 {time.time() - started:.1f}s")
    if unclassified:
        log("提示：待归类的仓库见 data/unclassified.json，可以往 config/rules.toml 加关键词，")
        log("     或在 config/overrides.toml 里单独指定。")
    return 0


def normalize_raw(item: dict) -> dict:
    """demo_data 里的简化结构 -> 标准结构。"""
    full_name = item["full_name"]
    return {
        "full_name": full_name,
        "name": full_name.split("/")[-1],
        "owner": full_name.split("/")[0],
        "html_url": f"https://github.com/{full_name}",
        "description": item.get("description", ""),
        "homepage": item.get("homepage", ""),
        "language": item.get("language", ""),
        "stars": item.get("stars", 0),
        "forks": 0,
        "topics": item.get("topics", []),
        "license": item.get("license", ""),
        "archived": item.get("archived", False),
        "pushed_at": "",
        "starred_at": item.get("starred_at", ""),
    }


if __name__ == "__main__":
    raise SystemExit(main())
