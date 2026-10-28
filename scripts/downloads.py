"""把「进应用页 → 找安装包 → 再点一次」压缩成「点一下就下载」。

设计目标只有一个：减少跳转。
- README 的「最近更新」表格里，版本号变成同页锚点；
- 锚点下方就是这个应用最新版的直链，点一次直接落到文件；
- 首页不需要进应用页、更不需要进 GitHub 原仓库。
"""

from __future__ import annotations

import re

# 校验文件 / 更新日志这类不需要出现在「一键下载」里的附件
_SKIP = (
    "sha256", "sha512", "sha1", "checksum", "checksums", ".sig", ".asc", ".md5",
    ".blockmap", ".txt", ".json", ".yml", ".yaml", ".pem", ".sbom",
    "release-notes", "changelog",
)

_GROUPS = [
    ("windows", "🪟", (".exe", ".msi", ".msix", ".msixbundle", ".appx")),
    ("android", "📲", (".apk", ".apks", ".apkm", ".xapk")),
    ("macos", "🍎", (".dmg", ".pkg")),
    ("linux", "🐧", (".appimage", ".deb", ".rpm", ".flatpak", ".snap")),
    ("other", "📦", (".zip", ".7z", ".tar.gz", ".tgz", ".tar.xz", ".jar")),
]

_LABEL = {k: e for k, e, _ in _GROUPS}


def _skip(name: str) -> bool:
    low = name.lower()
    return any(k in low for k in _SKIP)


def group_of(name: str) -> str | None:
    low = name.lower()
    for key, _, exts in _GROUPS:
        if low.endswith(exts):
            return key
    return None


def _score(name: str, group: str) -> tuple[int, int]:
    """同一平台有多个包时，挑最可能是「我该装的那个」。分数越小越优先。"""
    low = name.lower()
    s = 0
    if group == "windows":
        if "arm64" in low or "aarch64" in low:
            s += 8
        if any(k in low for k in ("win32", "x86-32", "i386", "i686")):
            s += 5
        if "x64" in low or "amd64" in low or "x86_64" in low:
            s -= 2
        if any(k in low for k in ("setup", "installer", "instal")):
            s -= 2
        elif "portable" in low:
            s -= 1
    elif group == "android":
        if "arm64" in low:
            s -= 4
        elif "universal" in low:
            s -= 3
        elif "armeabi" in low or "x86" in low:
            s += 4
    elif group == "macos":
        if "universal" in low:
            s -= 3
        elif "arm64" in low or "aarch64" in low:
            s -= 2
        elif "x64" in low or "intel" in low:
            s += 1
    elif group == "linux":
        if "appimage" in low:
            s -= 2
        if "arm64" in low or "aarch64" in low:
            s += 2
    elif group == "other":
        if "portable" in low:
            s -= 3
        if "win" in low:
            s -= 1
    return (s, len(name))


_ARCH = (
    ("arm64-v8a", "arm64"), ("armeabi-v7a", "armv7"), ("aarch64", "arm64"),
    ("arm64", "arm64"), ("x86_64", "x64"), ("amd64", "x64"), ("universal", "通用"),
    ("win32", "x86"), ("x64", "x64"), ("x86", "x86"),
)


def _label(item: dict) -> str:
    """把「Motrix-2.1.0-x86_64.AppImage」变成「x64 AppImage」这种人话。"""
    name = item["name"]
    low = name.lower()
    arch = ""
    for key, val in _ARCH:
        if key in low:
            arch = val
            break
    if low.endswith((".exe", ".msi", ".msix", ".msixbundle", ".appx")):
        kind = "便携版" if "portable" in low else "安装版"
    elif low.endswith((".apk", ".apks", ".apkm", ".xapk")):
        kind = "apk"
    elif low.endswith(".dmg"):
        kind = "dmg"
    elif low.endswith(".pkg"):
        kind = "pkg"
    elif low.endswith(".appimage"):
        kind = "AppImage"
    elif low.endswith(".deb"):
        kind = "deb"
    elif low.endswith(".rpm"):
        kind = "rpm"
    elif low.endswith((".zip", ".7z")):
        kind = "便携版" if "portable" in low else "zip"
    else:
        kind = ""
    parts = [p for p in (arch, kind) if p]
    if parts:
        return " ".join(parts)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    return stem if len(stem) <= 24 else stem[:23] + "…"


def _fmt(n: int) -> str:
    if not n:
        return "?"
    mb = n / 1024**2
    if mb >= 1024:
        return f"{mb / 1024:.1f} GB"
    if mb >= 100:
        return f"{mb:.0f} MB"
    return f"{mb:.1f} MB"


def anchor(repo: dict) -> str:
    """同页锚点。用 full_name 保证全局唯一，且只有 ASCII。"""
    raw = repo.get("full_name") or repo.get("name") or "app"
    return "dl-" + re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")


def best_links(repo: dict, max_groups: int = 5) -> list[dict]:
    """每个平台挑一个最合适的包，供首页一行展示。"""
    rel = repo.get("rel") or {}
    picked: dict[str, dict] = {}
    for a in rel.get("assets") or []:
        name = a.get("name") or ""
        if not name or _skip(name):
            continue
        g = group_of(name)
        if not g:
            continue
        cur = picked.get(g)
        if cur is None or _score(name, g) < _score(cur["name"], g):
            picked[g] = {"group": g, "name": name, "size": a.get("size") or 0,
                         "url": a.get("url") or ""}
    order = [k for k, _, _ in _GROUPS]
    out = [picked[k] for k in order if k in picked]
    return out[:max_groups]


def inline_links(repo: dict, limit: int = 5) -> str:
    """一行搞定：🪟 [x64 安装版 · 41 MB](url) · 📲 [arm64 apk · 32 MB](url) …"""
    parts = []
    for item in best_links(repo, limit):
        emoji = _LABEL[item["group"]]
        parts.append(f"{emoji} [{_label(item)} · {_fmt(item['size'])}]({item['url']})")
    return " · ".join(parts)


def block(repo: dict, detail_href: str, limit: int = 5) -> list[str]:
    """README 里每个应用的三行块：锚点 + 标题 + 直链。"""
    rel = repo.get("rel") or {}
    if not (rel.get("tag") and rel.get("assets")):
        return []
    links = inline_links(repo, limit)
    if not links:
        return []
    cat = repo["cls"]["functions"][0]
    head = (
        f"**{cat.get('emoji','')} {repo['name']}** · `{rel['tag']}` · "
        f"{(rel.get('published_at') or '')[:10]} · [详情]({detail_href})"
    )
    return [
        f'<a id="{anchor(repo)}"></a>',
        "",
        head,
        "",
        links,
        "",
    ]


def render_page(repos: list[dict], ctx: dict, href_of) -> str:
    """docs/downloads.md：全部应用的最新版直链，按更新时间倒序。"""
    now = ctx["synced_at"]
    rows = [r for r in repos if (r.get("rel") or {}).get("tag") and best_links(r)]
    rows.sort(key=lambda r: (r["rel"].get("published_at") or "", r["name"].lower()), reverse=True)

    L: list[str] = ["<!-- 本文件由 starred-hub 自动生成，手动修改会在下次同步时被覆盖 -->", "", '<a id="top"></a>', ""]
    L.append("# ⬇️ 下载索引")
    L.append("")
    L.append(f"**{len(rows)}** 个应用的最新版安装包，全部是官方直链，点一次就落到文件。")
    L.append("")
    L.append("[← 星标总览](../README.md) · [应用目录](../apps/README.md) · [更新动态](updates.md)")
    L.append("")
    L.append("> 每个应用只列「每个平台最该装的那一个」；完整 assets 清单见对应应用页或 `release.json`。")
    L.append("")
    L.append("---")
    L.append("")

    for r in rows:
        cat = r["cls"]["functions"][0]
        L.append(f'<a id="{anchor(r)}"></a>')
        L.append("")
        L.append(f"### {cat.get('emoji','')} {r['name']}")
        L.append("")
        L.append(
            f"`{r['rel']['tag']}` · {(r['rel'].get('published_at') or '')[:10]} · "
            f"[详情]({href_of(r)}) · [原仓库]({r.get('url') or '#'})"
        )
        L.append("")
        L.append(inline_links(r, 6) or "_该版本没有可直链的安装包_")
        L.append("")

    L.append("---")
    L.append("")
    L.append("[← 星标总览](../README.md) · [返回顶部](#top)")
    return "\n".join(L)
