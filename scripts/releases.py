"""抓取每个仓库的最新 Release（版本号 / 发布日期 / 安装包列表）。

只调用 GitHub 的 public API，不下载安装包本体：
  GET /repos/{owner}/{repo}/releases/latest   有 Release 的仓库
  GET /repos/{owner}/{repo}/tags?per_page=1   只有 tag 没有 Release 的仓库

结果会写进 data/releases.json 做缓存，接口失败时回退到上一次的结果，
避免某天网络抖动就把「最新版本」全清空。
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://api.github.com"
TZ = timezone(timedelta(hours=8))
UA = "starred-hub-release-check"


def _get(url: str, token: str | None) -> tuple[int, object]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": UA,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(3):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, json.load(resp)
        except urllib.error.HTTPError as e:
            return e.code, None
        except Exception:  # noqa: BLE001 —— 连接被重置、超时、半开连接都归到这里
            if attempt < 2:
                time.sleep(0.8 * (attempt + 1))
                continue
            return 0, None
    return 0, None


def _pick_assets(raw: list[dict]) -> list[dict]:
    out = []
    for a in raw[:40]:
        out.append(
            {
                "name": a.get("name") or "",
                "size": a.get("size") or 0,
                "downloads": a.get("download_count") or 0,
                "url": a.get("browser_download_url") or "",
            }
        )
    return out


def _fetch_one(repo: dict, token: str | None) -> dict:
    full = repo["full_name"]
    code, data = _get(f"{API}/repos/{full}/releases/latest", token)

    if code == 200 and isinstance(data, dict):
        return {
            "kind": "release",
            "tag": data.get("tag_name") or "",
            "title": data.get("name") or data.get("tag_name") or "",
            "published_at": data.get("published_at") or "",
            "url": data.get("html_url") or "",
            "prerelease": bool(data.get("prerelease")),
            "body": (data.get("body") or "").strip(),
            "assets": _pick_assets(data.get("assets") or []),
        }

    if code in (403, 429):
        return {"kind": "ratelimit", "tag": "", "assets": []}
    if code == 0:
        return {"kind": "neterror", "tag": "", "assets": []}

    # 没有 Release，退一步看有没有 tag
    code, tags = _get(f"{API}/repos/{full}/tags?per_page=1", token)
    if code == 200 and isinstance(tags, list) and tags:
        return {
            "kind": "tag",
            "tag": tags[0].get("name") or "",
            "title": tags[0].get("name") or "",
            "published_at": "",
            "url": f"https://github.com/{full}/tags",
            "prerelease": False,
            "body": "",
            "assets": [],
        }
    return {"kind": "none", "tag": "", "title": "", "published_at": "", "url": "", "prerelease": False, "body": "", "assets": []}


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("items") or {}
    except (json.JSONDecodeError, OSError):
        return {}


def enrich(repos: list[dict], token: str | None, cache_path: Path, workers: int = 5) -> dict:
    """给每个 repo 补上 repo["rel"]，返回统计信息。"""
    cache = load_cache(cache_path)
    stats = {"release": 0, "tag": 0, "none": 0, "cached": 0, "total": len(repos)}

    def task(repo: dict) -> tuple[str, dict]:
        fresh = _fetch_one(repo, token)
        if fresh["kind"] in ("ratelimit", "neterror"):
            old = cache.get(repo["full_name"])
            if old:
                return repo["full_name"], {**old, "kind": old.get("kind") or "none", "stale": True}
            return repo["full_name"], {"kind": "none", "tag": "", "title": "", "published_at": "", "url": "", "prerelease": False, "body": "", "assets": []}
        return repo["full_name"], fresh

    started = time.time()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = dict(pool.map(task, repos))

    for repo in repos:
        rel = results.get(repo["full_name"]) or {"kind": "none", "tag": "", "assets": []}
        rel["checked_at"] = datetime.now(TZ).isoformat(timespec="seconds")
        repo["rel"] = rel
        if rel.get("stale"):
            stats["cached"] += 1
        else:
            stats[rel.get("kind", "none")] = stats.get(rel.get("kind", "none"), 0) + 1

    stats["seconds"] = round(time.time() - started, 1)
    return stats


def save_cache(repos: list[dict], cache_path: Path) -> None:
    items = {}
    for repo in repos:
        rel = repo.get("rel") or {}
        if not rel or rel.get("kind") == "ratelimit":
            continue
        items[repo["full_name"]] = rel
    payload = {
        "fetched_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "items": items,
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
