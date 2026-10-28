"""规则分类器：把仓库按「平台」和「功能」两个维度打标。

所有规则都来自 config/rules.toml，规则在文件里的顺序就是优先级：
顺序越靠前，命中后越可能成为该仓库的「主分类」。

匹配对象 = 仓库名 + 仓库名分词 + topics + 描述（全部小写）。
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DIMENSIONS = ("platform", "function")


@dataclass
class Category:
    name: str
    slug: str
    emoji: str = ""
    patterns: list[str] = field(default_factory=list)
    regexes: list[re.Pattern] = field(default_factory=list)

    def matches(self, hay: str) -> bool:
        return any(r.search(hay) for r in self.regexes)

    def as_dict(self) -> dict:
        return {"name": self.name, "slug": self.slug, "emoji": self.emoji}


def _compile(pattern: str) -> re.Pattern:
    """把关键词编译成「两侧不能紧邻英数字」的正则，避免 git 命中 github。"""
    escaped = re.escape(pattern.lower())
    return re.compile(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])")


def load_rules(path: Path) -> dict[str, list[Category]]:
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    out: dict[str, list[Category]] = {}
    for dim in DIMENSIONS:
        cats: list[Category] = []
        for idx, item in enumerate(raw.get(dim, []), start=1):
            patterns = [str(p) for p in item.get("patterns", [])]
            cat = Category(
                name=item["name"],
                slug=item.get("slug") or f"{dim}{idx:02d}",
                emoji=item.get("emoji", ""),
                patterns=patterns,
            )
            cat.regexes = [_compile(p) for p in patterns]
            cats.append(cat)
        out[dim] = cats
    return out


def build_lookup(rules: dict[str, list[Category]]) -> dict[str, dict[str, Category]]:
    """name / slug 双索引，方便 overrides.toml 里两种写法都能用。"""
    lookup: dict[str, dict[str, Category]] = {}
    for dim in DIMENSIONS:
        idx: dict[str, Category] = {}
        for cat in rules[dim]:
            idx[cat.name] = cat
            idx[cat.slug] = cat
        lookup[dim] = idx
    return lookup


def haystack(repo: dict) -> str:
    name = repo.get("name") or ""
    spaced = re.sub(r"[-_.]+", " ", name)
    topics = " ".join(repo.get("topics") or [])
    desc = repo.get("description") or ""
    return f"{name} {spaced} {topics} {desc}".lower()


def classify(
    repo: dict,
    rules: dict[str, list[Category]],
    fallback_platform: str = "unknown",
    fallback_function: str = "other",
    max_tags: int | None = None,
) -> dict:
    hay = haystack(repo)

    platforms = [c for c in rules["platform"] if c.matches(hay)]
    functions = [c for c in rules["function"] if c.matches(hay)]

    if not platforms:
        platforms = [Category(name="未标注平台", slug=fallback_platform, emoji="❓")]
    if not functions:
        functions = [Category(name="其他", slug=fallback_function, emoji="📦")]

    if max_tags:
        platforms, functions = platforms[:max_tags], functions[:max_tags]

    return {
        "platforms": [c.as_dict() for c in platforms],
        "functions": [c.as_dict() for c in functions],
        "primary_platform": platforms[0].slug,
        "primary_function": functions[0].slug,
    }


def apply_override(
    repo: dict,
    cls: dict,
    override: dict | None,
    lookup: dict[str, dict[str, Category]],
    warn=print,
) -> dict:
    """手动分类优先于自动分类：写了哪个维度就整体替换哪个维度。"""
    if not override:
        return cls

    for dim, key in (("platform", "platforms"), ("function", "functions")):
        wanted = override.get(dim)
        if not wanted:
            continue
        cats: list[Category] = []
        for item in wanted:
            cat = lookup[dim].get(item)
            if cat is None:
                warn(f"  ! overrides 里的分类不存在：{repo['full_name']} -> {item}")
                continue
            cats.append(cat)
        if cats:
            cls[key] = [c.as_dict() for c in cats]
            cls["primary_" + dim] = cats[0].slug

    if override.get("note"):
        cls["note"] = override["note"]
    return cls
