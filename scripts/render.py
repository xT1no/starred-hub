"""把分类好的仓库渲染成 Markdown 文档。

产物：
  README.md                总览
  docs/by-function.md      按功能分类
  docs/by-platform.md      按平台分类
  docs/timeline.md         按标星时间倒序
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime

# ---------------------------------------------------------------- 文本工具


def dwidth(s: str) -> int:
    """粗略显示宽度：中日韩字符算 2。"""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def shorten(s: str, limit: int = 96) -> str:
    s = " ".join((s or "").split())
    if dwidth(s) <= limit:
        return s
    out, w = [], 0
    for c in s:
        w += 2 if ord(c) > 0x2E80 else 1
        if w > limit - 1:
            break
        out.append(c)
    return "".join(out).rstrip() + "…"


def cell(s: str) -> str:
    return shorten(s).replace("|", "\\|").replace("\n", " ")


def fmt_stars(n: int) -> str:
    n = int(n or 0)
    if n >= 1000:
        v = n / 1000
        return (f"{v:.1f}k" if v < 10 else f"{v:.0f}k").replace(".0k", "k")
    return str(n)


def bar(n: int, top: int, width: int = 18) -> str:
    if not top:
        return ""
    return "▇" * max(1, round(n / top * width))


def md_link(repo: dict) -> str:
    return f"[{repo['full_name']}]({repo['html_url']})"


def platforms_text(repo: dict, limit: int = 5) -> str:
    cats = [c for c in repo["cls"]["platforms"] if c.get("emoji")]
    tail = f" +{len(cats) - limit}" if len(cats) > limit else ""
    return (" ".join(c["emoji"] for c in cats[:limit]) + tail).strip() or "—"


def functions_text(repo: dict, limit: int = 3) -> str:
    cats = [c for c in repo["cls"]["functions"] if c.get("emoji")]
    tail = f" +{len(cats) - limit}" if len(cats) > limit else ""
    return (" ".join(c["emoji"] for c in cats[:limit]) + tail).strip() or "—"


def desc_text(repo: dict) -> str:
    desc = repo.get("description") or ""
    note = repo["cls"].get("note")
    if note:
        desc = f"{note}｜{desc}" if desc else note
    if repo.get("archived"):
        desc = "🗄️ 已归档 · " + desc
    return cell(desc) or "—"


def starred_day(repo: dict) -> str:
    return (repo.get("starred_at") or "")[:10] or "—"


def new_badge(repo: dict, new_days: int) -> str:
    iso = repo.get("starred_at") or ""
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return ""
    delta = (datetime.now(dt.tzinfo) - dt).days
    return " 🆕" if delta <= new_days else ""


def _within(iso: str, ref: datetime, days: int) -> bool:
    """iso 时间是否在 ref 之前 days 天以内。"""
    if not iso:
        return False
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return False
    return 0 <= (ref - dt).days <= days


# ---------------------------------------------------------------- 分组


def group_by(repos: list[dict], dim: str, order: list[str], primary: bool = False) -> list[tuple[dict, list[dict]]]:
    """按某个维度分组。

    primary=True 时一个仓库只进「主分类」，保证各分类数量之和等于仓库总数；
    primary=False 时允许多归属（平台维度就是这样）。
    """
    buckets: dict[str, dict] = {}
    for repo in repos:
        cats = repo["cls"][dim][:1] if primary else repo["cls"][dim]
        for cat in cats:
            slot = buckets.setdefault(cat["slug"], {"cat": cat, "repos": []})
            slot["repos"].append(repo)

    def sort_key(slug: str) -> tuple:
        return (order.index(slug), "") if slug in order else (len(order), slug)

    groups = []
    for slug in sorted(buckets, key=sort_key):
        slot = buckets[slug]
        slot["repos"].sort(key=lambda r: (-r.get("stars", 0), r["full_name"].lower()))
        groups.append((slot["cat"], slot["repos"]))
    return groups


def nav_bar(current: str) -> str:
    items = [
        ("readme", "[总览](../README.md)"),
        ("apps", "[应用目录](../apps/README.md)"),
        ("function", "[按功能](by-function.md)"),
        ("platform", "[按平台](by-platform.md)"),
        ("timeline", "[时间线](timeline.md)"),
        ("updates", "[更新动态](updates.md)"),
    ]
    return " · ".join((f"**{label}**" if key == current else label) for key, label in items)


def anchor(slug: str) -> str:
    return f'<a id="{slug}"></a>'


# ---------------------------------------------------------------- README


def render_readme(ctx: dict) -> str:
    repos = ctx["repos"]
    rules = ctx["rules"]
    synced = ctx["synced_at"]
    new_days = ctx["new_days"]

    order_platform = [c.slug for c in rules["platform"]]
    order_function = [c.slug for c in rules["function"]]
    fn_groups = group_by(repos, "functions", order_function, primary=True)
    pf_groups = group_by(repos, "platforms", order_platform)

    fresh = [r for r in repos if new_badge(r, new_days)]
    fresh.sort(key=lambda r: r.get("starred_at") or "", reverse=True)

    total = len(repos)
    langs = Counter(r["language"] for r in repos if r.get("language"))
    top_lang = langs.most_common(8)
    max_lang = top_lang[0][1] if top_lang else 0

    L: list[str] = []
    A = L.append

    A('<div align="center">')
    A("")
    A("# ⭐ Starred Hub")
    A("")
    A(f"**{ctx['login']} 的 GitHub 星标仓库 · 自动归档**")
    A("")
    A(f"`{total}` 个仓库 · `{len(fn_groups)}` 个功能分类 · `{len(pf_groups)}` 个平台分类")
    A("")
    A(f"最近同步：{synced.strftime('%Y-%m-%d %H:%M')} (UTC+8)")
    A("")
    A("[📱 应用目录](apps/README.md) · [按功能浏览](docs/by-function.md) · [按平台浏览](docs/by-platform.md) · [更新动态](docs/updates.md) · [时间线](docs/timeline.md)")
    A("")
    A("</div>")
    A("")
    A("---")
    A("")

    # ---------- 最近更新
    upd = [r for r in repos if (r.get("rel") or {}).get("tag") and (r.get("rel") or {}).get("published_at")]
    upd.sort(key=lambda r: r["rel"]["published_at"], reverse=True)
    fresh_upd = [r for r in upd if _within(r["rel"]["published_at"], synced, 30)]
    if upd:
        A(f"## 🔥 最近更新（30 天内 {len(fresh_upd)} 个应用发布新版）")
        A("")
        A("| 应用 | 最新版本 | 发布 | 分类 | ⭐ |")
        A("|:---|:---|:---:|:---:|---:|")
        for r in (fresh_upd or upd)[:18]:
            cat = r["cls"]["functions"][0]
            A(
                f"| [{r['name']}](apps/{cat['slug']}/{r.get('dir') or r['name']}/README.md) | "
                f"`{r['rel']['tag']}` | {r['rel']['published_at'][:10]} | {cat.get('emoji','')} | "
                f"{fmt_stars(r.get('stars'))} |"
            )
        A("")
        A(f"完整清单见 [更新动态](docs/updates.md)，全部应用见 [应用目录](apps/README.md)。")
        A("")

    # ---------- 最近标星
    if fresh:
        A(f"## 🆕 最近标星（{new_days} 天内 · {len(fresh)} 个）")
        A("")
        A("| 仓库 | 简介 | 平台 | ⭐ | 标星日期 |")
        A("|:---|:---|:---:|:---|---:|")
        for r in fresh[:24]:
            A(f"| {md_link(r)} | {desc_text(r)} | {platforms_text(r)} | {fmt_stars(r.get('stars'))} | {starred_day(r)} |")
        if len(fresh) > 24:
            A("")
            A(f"还有 {len(fresh) - 24} 个，见 [时间线](docs/timeline.md)。")
    else:
        latest = sorted(repos, key=lambda r: r.get("starred_at") or "", reverse=True)[:12]
        stamp = starred_day(latest[0]) if latest else "—"
        A(f"## 🕘 最近标星（{new_days} 天内新增 0 个，最近一次是 {stamp}）")
        A("")
        A("| 仓库 | 简介 | 平台 | 功能 | ⭐ | 标星日期 |")
        A("|:---|:---|:---:|:---:|---|---:|")
        for r in latest:
            A(
                f"| {md_link(r)} | {desc_text(r)} | {platforms_text(r)} | "
                f"{functions_text(r)} | {fmt_stars(r.get('stars'))} | {starred_day(r)} |"
            )
    A("")

    # ---------- 功能概览
    A("## 📂 按功能")
    A("")
    A("| 分类 | 数量 | 代表仓库 |")
    A("|:---|:---:|:---|")
    for cat, items in fn_groups:
        picks = "、".join(f"[{r['name']}]({r['html_url']})" for r in items[:3])
        label = f"{cat.get('emoji','')} [{cat['name']}](docs/by-function.md#{cat['slug']})".replace("  ", " ")
        A(f"| {label} | {len(items)} | {picks} |")
    A("")

    # ---------- 平台概览
    A("## 💻 按平台")
    A("")
    A("| 平台 | 数量 | 代表仓库 |")
    A("|:---|:---:|:---|")
    for cat, items in pf_groups:
        picks = "、".join(f"[{r['name']}]({r['html_url']})" for r in items[:3])
        label = f"{cat.get('emoji','')} [{cat['name']}](docs/by-platform.md#{cat['slug']})".replace("  ", " ")
        A(f"| {label} | {len(items)} | {picks} |")
    A("")

    # ---------- 语言分布
    if top_lang:
        A("## 🧬 主要语言")
        A("")
        A("| 语言 | 数量 | 分布 |")
        A("|:---|:---:|:---|")
        for lang, n in top_lang:
            A(f"| {lang} | {n} | `{bar(n, max_lang)}` |")
        A("")

    # ---------- 取消标星
    removed = ctx.get("removed") or []
    if removed:
        A(f"<details><summary>🚫 最近取消标星（{len(removed)}）</summary>")
        A("")
        for r in removed[:30]:
            A(f"- ~~[{r['full_name']}]({r['html_url']})~~ — {(r.get('description') or '无描述')[:60]}")
        A("")
        A("</details>")
        A("")

    # ---------- 说明
    A("---")
    A("")
    A("## 🔧 这个仓库怎么维护自己")
    A("")
    A("每天早上 **08:00（北京时间）**，GitHub Actions 会调用 GitHub API 拉一遍星标列表，")
    A("重新分类、重写上面这些文档，然后自动提交回来。你不需要做任何事。")
    A("")
    A("想手动触发一次：`Actions` → `Sync starred repos` → `Run workflow`。")
    A("")
    A("| 我想改什么 | 改哪个文件 |")
    A("|:---|:---|")
    A("| 分类关键词、新增分类 | [`config/rules.toml`](config/rules.toml) |")
    A("| 某个仓库归错类了 | [`config/overrides.toml`](config/overrides.toml) |")
    A("| 同步时间、是否自动提交 | [`.github/workflows/sync-stars.yml`](.github/workflows/sync-stars.yml) |")
    A("")
    A("> 本仓库所有 `README.md`、`docs/*.md`、`apps/**` 都是**生成产物**，直接改会在下次同步时被覆盖。")
    A("> 要留自己的备注请写进 `config/overrides.toml`。")
    A("")
    return "\n".join(L)


# ---------------------------------------------------------------- 按功能


def render_by_function(ctx: dict) -> str:
    repos = ctx["repos"]
    order = [c.slug for c in ctx["rules"]["function"]]
    groups = group_by(repos, "functions", order, primary=True)

    L: list[str] = []
    A = L.append
    A('<a id="top"></a>')
    A("")
    A("# 📂 按功能分类")
    A("")
    A(nav_bar("function"))
    A("")
    A(f"共 **{len(repos)}** 个仓库 · **{len(groups)}** 个分类 · 同步于 {ctx['synced_at'].strftime('%Y-%m-%d %H:%M')}")
    A("")
    A("## 目录")
    A("")
    A("| 分类 | 数量 |")
    A("|:---|:---:|")
    for cat, items in groups:
        e = (cat.get("emoji") or "") + " " if cat.get("emoji") else ""
        A(f"| {e}[{cat['name']}](#{cat['slug']}) | {len(items)} |")
    A("")
    A("---")
    A("")

    for cat, items in groups:
        e = (cat.get("emoji") or "") + " " if cat.get("emoji") else ""
        A(anchor(cat["slug"]))
        A(f"## {e}{cat['name']}")
        A("")
        A(f"共 **{len(items)}** 个 · [回到顶部](#top)")
        A("")
        A("| 仓库 | 简介 | 平台 | 语言 | ⭐ | 标星 |")
        A("|:---|:---|:---:|:---|:---|---:|")
        for r in items:
            A(
                f"| {md_link(r)}{new_badge(r, ctx['new_days'])} | {desc_text(r)} | "
                f"{platforms_text(r)} | {r.get('language') or '—'} | "
                f"{fmt_stars(r.get('stars'))} | {starred_day(r)} |"
            )
        A("")

    A("---")
    A("")
    A(legend(ctx, "platforms"))
    return "\n".join(L)


# ---------------------------------------------------------------- 按平台


def render_by_platform(ctx: dict) -> str:
    repos = ctx["repos"]
    order = [c.slug for c in ctx["rules"]["platform"]]
    groups = group_by(repos, "platforms", order)

    L: list[str] = []
    A = L.append
    A('<a id="top"></a>')
    A("")
    A("# 💻 按平台分类")
    A("")
    A(nav_bar("platform"))
    A("")
    A(f"共 **{len(repos)}** 个仓库 · **{len(groups)}** 个平台 · 同步于 {ctx['synced_at'].strftime('%Y-%m-%d %H:%M')}")
    A("")
    A("> 一个仓库支持多个平台时会同时出现在多个分类里，所以各分类数量之和会大于总数。")
    A("")
    A("## 目录")
    A("")
    A("| 平台 | 数量 |")
    A("|:---|:---:|")
    for cat, items in groups:
        e = (cat.get("emoji") or "") + " " if cat.get("emoji") else ""
        A(f"| {e}[{cat['name']}](#{cat['slug']}) | {len(items)} |")
    A("")
    A("---")
    A("")

    for cat, items in groups:
        e = (cat.get("emoji") or "") + " " if cat.get("emoji") else ""
        A(anchor(cat["slug"]))
        A(f"## {e}{cat['name']}")
        A("")
        A(f"共 **{len(items)}** 个 · [回到顶部](#top)")
        A("")
        A("| 仓库 | 简介 | 功能 | 语言 | ⭐ | 标星 |")
        A("|:---|:---|:---:|:---|:---|---:|")
        for r in items:
            A(
                f"| {md_link(r)}{new_badge(r, ctx['new_days'])} | {desc_text(r)} | "
                f"{functions_text(r)} | {r.get('language') or '—'} | "
                f"{fmt_stars(r.get('stars'))} | {starred_day(r)} |"
            )
        A("")

    A("---")
    A("")
    A(legend(ctx, "functions"))
    return "\n".join(L)


# ---------------------------------------------------------------- 时间线


def render_timeline(ctx: dict) -> str:
    repos = sorted(ctx["repos"], key=lambda r: r.get("starred_at") or "", reverse=True)

    L: list[str] = []
    A = L.append
    A('<a id="top"></a>')
    A("")
    A("# 🕒 标星时间线")
    A("")
    A(nav_bar("timeline"))
    A("")
    A(f"共 **{len(repos)}** 个仓库 · 按标星时间倒序 · 同步于 {ctx['synced_at'].strftime('%Y-%m-%d %H:%M')}")
    A("")
    A("---")
    A("")

    current = None
    for r in repos:
        month = (r.get("starred_at") or "")[:7] or "未知"
        if month != current:
            if current is not None:
                A("")
            current = month
            count = sum(1 for x in repos if (x.get("starred_at") or "")[:7] == month)
            A(f"## {month} <sup>{count}</sup>")
            A("")
            A("| 仓库 | 简介 | 功能 | 平台 | 标星 |")
            A("|:---|:---|:---:|:---:|---:|")
        A(
            f"| {md_link(r)} | {desc_text(r)} | {functions_text(r)} | "
            f"{platforms_text(r)} | {starred_day(r)} |"
        )
    A("")
    A("---")
    A("")
    A(legend(ctx, "functions"))
    A("")
    A(legend(ctx, "platforms"))
    return "\n".join(L)


# ---------------------------------------------------------------- 图例


def legend(ctx: dict, dim: str) -> str:
    key = "platform" if dim.startswith("platform") else "function"
    cats = ctx["rules"][key]
    parts = [f"{c.emoji} {c.name}" for c in cats if c.emoji]
    if key == "platform":
        parts.append("❓ 通用 / 未指定")
    else:
        parts.append("📦 其他")
    return "**图标对照**：" + " · ".join(parts)


# ---------------------------------------------------------------- 总入口


def render_all(ctx: dict) -> dict[str, str]:
    return {
        "README.md": render_readme(ctx),
        "docs/by-function.md": render_by_function(ctx),
        "docs/by-platform.md": render_by_platform(ctx),
        "docs/timeline.md": render_timeline(ctx),
    }
