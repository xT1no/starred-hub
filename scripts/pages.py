"""生成 apps/ 目录树。

结构（按功能一级分类，一个应用一个文件夹）：

    apps/
    ├── README.md                  全部应用总索引
    ├── proxy/
    │   ├── README.md              分类索引（含每个应用的最新版本）
    │   └── clash-verge-rev/
    │       └── README.md          应用详情（最新版本 + 安装包直链 + 更新说明）
    └── video/...

文件夹名用英文 slug，链接稳定、跨平台不会乱码；中文分类名写在每个 README 的标题里。
"""
from __future__ import annotations

import re
from datetime import datetime

MARKER = "<!-- 本文件由 starred-hub 自动生成，手动修改会在下次同步时被覆盖 -->"

RESERVED = {
    "con", "prn", "aux", "nul",
    "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
}


# ------------------------------------------------------------------ 工具


def safe_name(name: str) -> str:
    """仓库名 -> 合法的目录名。"""
    s = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "-", name).strip("-._").lower()
    s = s or "repo"
    return f"_{s}" if s in RESERVED else s


def app_dir_name(repo: dict) -> str:
    return safe_name(repo["name"])


def write_dir(repo: dict) -> str:
    return (repo.get("dir") or app_dir_name(repo))


def fmt_size(n: int) -> str:
    n = int(n or 0)
    if n >= 1024 * 1024 * 1024:
        return f"{n / 1024 / 1024 / 1024:.1f} GB"
    if n >= 1024 * 1024:
        return f"{n / 1024 / 1024:.1f} MB"
    if n >= 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n} B"


def fmt_stars(n) -> str:
    n = int(n or 0)
    if n >= 1000:
        v = n / 1000
        return (f"{v:.1f}k" if v < 10 else f"{v:.0f}k").replace(".0k", "k")
    return str(n)


def day(iso: str) -> str:
    return (iso or "")[:10] or "—"


def ago(iso: str, now: datetime) -> str:
    if not iso:
        return "—"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return "—"
    d = (now - dt).days
    if d < 0:
        return day(iso)
    if d == 0:
        return "今天"
    if d == 1:
        return "昨天"
    if d < 30:
        return f"{d} 天前"
    if d < 365:
        return f"{d // 30} 个月前"
    return f"{d // 365} 年前"


def tag_of(repo: dict) -> str:
    rel = repo.get("rel") or {}
    return rel.get("tag") or ""


def release_of(repo: dict) -> dict:
    return repo.get("rel") or {}


def updated_at(repo: dict) -> str:
    rel = release_of(repo)
    return rel.get("published_at") or repo.get("pushed_at") or ""


def cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def one_line(s: str, limit: int = 110) -> str:
    s = " ".join((s or "").split())
    return s if len(s) <= limit else s[: limit - 1] + "…"


# ------------------------------------------------------------------ 安装包平台识别

_PLAT_MAP = [
    ("🍎 macOS", ("darwin", "macos", "osx", "mac-", "-mac", ".dmg", "universal2", "apple-silicon")),
    ("📺 AndroidTV", ("androidtv", "-tv", "leanback")),
    ("📲 Android", ("android", ".apk", "apks", "arm64-v8a", "armeabi", "armeabi-v7a")),
    ("🪟 Windows", ("windows", "win32", "win64", "win-", "-win", ".exe", ".msi", ".msix", "setup-x64")),
    ("🐧 Linux", ("linux", "appimage", ".deb", ".rpm", "arm64", "amd64")),
    ("🌐 Web", (".zip", ".crx", ".xpi", "chrome", "firefox", "edge")),
    ("⌨️ CLI", ("cli", "x86_64", "musl")),
]

_PLAT_RANK = {label: i for i, (label, _) in enumerate(_PLAT_MAP)}
_PLAT_RANK["🔐 校验文件"] = 90
_PLAT_RANK["📦 其他"] = 99


def guess_platform(filename: str) -> str:
    low = (filename or "").lower()
    if any(k in low for k in ("sha256", "sha512", "checksum", ".sig", "sha1sum")):
        return "🔐 校验文件"
    for label, keys in _PLAT_MAP:
        if any(k in low for k in keys):
            return label
    return "📦 其他"


def clean_body(body: str, max_lines: int = 14, max_chars: int = 900) -> str:
    """把 Release 说明里的 HTML 注释、空行去掉，保留结构但限制长度。"""
    text = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)
    lines = [ln.rstrip() for ln in text.splitlines()]
    out: list[str] = []
    total = 0
    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        if total + len(ln) > max_chars or len(out) >= max_lines:
            out.append("…（完整内容见 Release 页面）")
            break
        out.append(ln[:160])
        total += len(ln)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


# ------------------------------------------------------------------ 应用详情页


def render_app(repo: dict, cat: dict, ctx: dict) -> str:
    rel = release_of(repo)
    now = ctx["synced_at"]
    L: list[str] = [MARKER, ""]

    L.append(f"# {repo['name']}")
    L.append("")
    desc = repo.get("description") or ""
    note = repo["cls"].get("note")
    if note:
        L.append(f"> {note}")
        L.append("")
    if desc:
        L.append(desc)
        L.append("")
    if repo.get("archived"):
        L.append("> 🗄️ **该仓库已归档，作者不再维护。**")
        L.append("")

    L.append("| 项目 | 信息 |")
    L.append("|:---|:---|")
    L.append(f"| 仓库 | [{repo['full_name']}]({repo['html_url']}) |")
    L.append(f"| 分类 | {cat.get('emoji','')} [{cat['name']}](../README.md) |")
    pfs = " ".join(c.get("emoji") or "" for c in repo["cls"]["platforms"]).strip()
    L.append(f"| 平台 | {pfs or '—'} |")
    L.append(f"| 语言 | {repo.get('language') or '—'} |")
    L.append(f"| Star | {fmt_stars(repo.get('stars'))} · Fork {fmt_stars(repo.get('forks'))} |")
    L.append(f"| License | {(repo.get('license') or '—')} |")
    L.append(f"| 最新版本 | `{rel.get('tag')}` |" if rel.get("tag") else "| 最新版本 | 无版本标记 |")
    L.append(f"| 最近更新 | {day(updated_at(repo))}（{ago(updated_at(repo), now)}） |")
    L.append(f"| 标星日期 | {day(repo.get('starred_at'))} |")
    if repo.get("homepage"):
        L.append(f"| 官网 | <{repo['homepage']}> |")
    L.append("")

    # ---- 最新版本
    L.append("## 📦 最新版本")
    L.append("")
    if rel.get("kind") == "release":
        head = f"**`{rel.get('tag')}`**"
        if rel.get("title") and rel["title"] != rel.get("tag"):
            head += f" · {rel['title']}"
        L.append(f"{head}　发布于 {day(rel.get('published_at'))}（{ago(rel.get('published_at'), now)}）")
        L.append("")
        L.append(f"[查看 Release 页面]({rel.get('url')})")
        L.append("")
        body = clean_body(rel.get("body") or "")
        if body:
            L.append("<details><summary>更新说明</summary>")
            L.append("")
            L.append("```text")
            L.append(body)
            L.append("```")
            L.append("")
            L.append("</details>")
            L.append("")
    elif rel.get("kind") == "tag":
        L.append(f"该仓库没有发布 Release，最新 tag 为 **`{rel.get('tag')}`**。")
        L.append("")
        L.append(f"[查看全部 tag]({rel.get('url')})")
        L.append("")
    else:
        L.append("该仓库没有 Release / tag 记录（常见于规则表、订阅源、脚本类仓库）。")
        L.append("")

    # ---- 安装包
    assets = rel.get("assets") or []
    if assets:
        L.append("## ⬇️ 安装包")
        L.append("")
        L.append(f"来自最新 Release，共 {len(assets)} 个文件。下表是官方直链，点名字即可下载。")
        L.append("")
        L.append("| 文件 | 适用平台 | 大小 | 累计下载 |")
        L.append("|:---|:---:|:---|---:|")
        ordered = sorted(assets, key=lambda a: (_PLAT_RANK.get(guess_platform(a["name"]), 99), -a.get("downloads", 0)))
        for a in ordered[:24]:
            L.append(
                f"| [{one_line(a['name'], 60)}]({a['url']}) | {guess_platform(a['name'])} | "
                f"{fmt_size(a['size'])} | {fmt_stars(a['downloads'])} |"
            )
        if len(ordered) > 24:
            L.append("")
            L.append(f"还有 {len(ordered) - 24} 个文件，见 [Release 页面]({rel.get('url')})。")
        L.append("")

    # ---- 快速链接
    L.append("## 🔗 快速链接")
    L.append("")
    L.append(f"- 仓库主页 · {repo['html_url']}")
    L.append(f"- Issues · {repo['html_url']}/issues")
    L.append(f"- Releases · {repo['html_url']}/releases")
    if repo.get("homepage"):
        L.append(f"- 官网 / 演示 · {repo['homepage']}")
    L.append("")
    if repo.get("topics"):
        L.append("`" + "` `".join(repo["topics"][:12]) + "`")
        L.append("")
    L.append("---")
    L.append("")
    L.append("← 返回 [" + f"{cat.get('emoji','')} {cat['name']}".strip() + "](../README.md) · [全部应用](../../README.md) · [星标总览](../../../README.md)")
    return "\n".join(L)


# ------------------------------------------------------------------ 分类索引页


def render_category(cat: dict, repos: list[dict], ctx: dict) -> str:
    now = ctx["synced_at"]
    days = ctx.get("release_days", 7)
    fresh = [r for r in repos if _recent(repo=updated_at(r), now=now, days=days)]
    L: list[str] = [MARKER, ""]
    L.append(f"# {cat.get('emoji','')} {cat['name']}")
    L.append("")
    L.append(f"共 **{len(repos)}** 个应用 · 其中 **{len(fresh)}** 个最近 {days} 天有更新")
    L.append("")
    L.append("[← 全部应用](../README.md) · [星标总览](../../README.md)")
    L.append("")

    L.append("## 📋 应用清单")
    L.append("")
    L.append("| 应用 | 简介 | 平台 | 最新版本 | 更新 | ⭐ |")
    L.append("|:---|:---|:---:|:---:|:---:|---:|")
    ordered = sorted(repos, key=lambda r: (updated_at(r) or "", r["name"].lower()), reverse=True)
    for r in ordered:
        tag = tag_of(r) or "—"
        link = f"[{r['name']}]({write_dir(r)}/README.md)"
        badge = " 🆕" if _recent(repo=updated_at(r), now=now, days=days) else ""
        L.append(
            f"| {link}{badge} | {cell(one_line(r.get('description') or r['cls'].get('note') or '—', 64))} | "
            f"{' '.join(c.get('emoji') or '' for c in r['cls']['platforms'][:4]).strip() or '—'} | "
            f"`{tag}` | {ago(updated_at(r), now)} | {fmt_stars(r.get('stars'))} |"
        )
    L.append("")

    if fresh:
        L.append("## 🔥 最近更新")
        L.append("")
        L.append("| 应用 | 版本 | 发布日期 |")
        L.append("|:---|:---|:---:|")
        for r in sorted(fresh, key=lambda x: updated_at(x), reverse=True)[:12]:
            L.append(f"| [{r['name']}]({write_dir(r)}/README.md) | `{tag_of(r) or '—'}` | {day(updated_at(r))} |")
        L.append("")

    L.append("---")
    L.append("")
    L.append("[← 全部应用](../README.md) · [返回星标总览](../../README.md)")
    return "\n".join(L)


def _recent(*, repo: str, now: datetime, days: int) -> bool:
    if not repo:
        return False
    try:
        dt = datetime.fromisoformat(repo.replace("Z", "+00:00"))
    except ValueError:
        return False
    return (now - dt).days <= days


# ------------------------------------------------------------------ 总索引


def render_index(groups: list[tuple[dict, list[dict]]], ctx: dict) -> str:
    now = ctx["synced_at"]
    days = ctx.get("release_days", 7)
    total = sum(len(items) for _, items in groups)
    with_rel = sum(1 for _, items in groups for r in items if tag_of(r))
    L: list[str] = [MARKER, ""]
    L.append("# 📱 应用目录")
    L.append("")
    L.append(f"共 **{total}** 个应用，按功能分成 **{len(groups)}** 个文件夹；其中 **{with_rel}** 个记录了最新版本。")
    L.append("")
    L.append("[← 星标总览](../README.md) · [按功能](../docs/by-function.md) · [按平台](../docs/by-platform.md) · [更新动态](../docs/updates.md)")
    L.append("")

    L.append("## 📁 文件夹")
    L.append("")
    L.append("| 分类 | 应用数 | 有版本号 | 最近更新 |")
    L.append("|:---|:---:|:---:|:---:|")
    for cat, items in groups:
        latest = max((updated_at(r) for r in items), default="")
        L.append(
            f"| {cat.get('emoji','')} [{cat['name']}]({cat['slug']}/README.md) | {len(items)} | "
            f"{sum(1 for r in items if tag_of(r))} | {ago(latest, now)} |"
        )
    L.append("")

    L.append(f"## 🔥 最近 {days} 天有更新")
    L.append("")
    fresh = [r for _, items in groups for r in items if _recent(repo=updated_at(r), now=now, days=days)]
    fresh.sort(key=lambda r: updated_at(r), reverse=True)
    if fresh:
        L.append("| 应用 | 版本 | 发布 | 分类 |")
        L.append("|:---|:---|:---:|:---:|")
        for r in fresh[:40]:
            cat = r["cls"]["functions"][0]
            L.append(
                f"| [{r['name']}]({cat['slug']}/{write_dir(r)}/README.md) | `{tag_of(r) or '—'}` | "
                f"{day(updated_at(r))} | {cat.get('emoji','')} |"
            )
        if len(fresh) > 40:
            L.append("")
            L.append(f"还有 {len(fresh) - 40} 个，见 [更新动态](../docs/updates.md)。")
    else:
        L.append(f"_最近 {days} 天没有应用发布新版本。_")
    L.append("")
    L.append("---")
    L.append("")
    L.append("> 每个文件夹里的 `README.md` 是自动生成的应用详情，包含最新版本、更新说明和官方安装包直链。")
    return "\n".join(L)


# ------------------------------------------------------------------ 更新动态


def render_updates(groups: list[tuple[dict, list[dict]]], ctx: dict) -> str:
    now = ctx["synced_at"]
    rows = [r for _, items in groups for r in items if tag_of(r)]
    rows.sort(key=lambda r: updated_at(r), reverse=True)

    L: list[str] = ['<a id="top"></a>', ""]
    L.append("# 🔄 应用更新动态")
    L.append("")
    L.append(
        f"跟踪 **{len(rows)}** 个有版本号的应用，按最新版本发布时间倒序 · 同步于 {now.strftime('%Y-%m-%d %H:%M')}"
    )
    L.append("")
    L.append("[← 星标总览](../README.md) · [应用目录](../apps/README.md) · [按功能](by-function.md) · [按平台](by-platform.md)")
    L.append("")
    L.append("---")
    L.append("")

    current = None
    for r in rows[:200]:
        month = (updated_at(r) or "")[:7] or "未知"
        if month != current:
            if current is not None:
                L.append("")
            current = month
            L.append(f"## {month}")
            L.append("")
            L.append("| 应用 | 版本 | 发布 | 分类 | 简介 |")
            L.append("|:---|:---|:---:|:---:|:---|")
        cat = r["cls"]["functions"][0]
        L.append(
            f"| [{r['name']}](../apps/{cat['slug']}/{write_dir(r)}/README.md) | `{tag_of(r)}` | "
            f"{day(updated_at(r))} | {cat.get('emoji','')} | {cell(one_line(r.get('description') or '—', 58))} |"
        )
    L.append("")
    return "\n".join(L)


# ------------------------------------------------------------------ 入口


def plan(ctx: dict, groups: list[tuple[dict, list[dict]]]) -> dict[str, str]:
    """返回 {相对路径: 内容}。"""
    files: dict[str, str] = {"apps/README.md": render_index(groups, ctx)}
    for cat, items in groups:
        files[f"apps/{cat['slug']}/README.md"] = render_category(cat, items, ctx)
        for repo in items:
            files[f"apps/{cat['slug']}/{write_dir(repo)}/README.md"] = render_app(repo, cat, ctx)
    files["docs/updates.md"] = render_updates(groups, ctx)
    return files
