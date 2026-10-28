"""应用文件夹里的附属文件：图标。

图标取仓库所有者的 GitHub 头像（owner.png），每个约 20~60 KB，
只在缺失或大小异常时下载，所以日常同步不会重复请求。
"""
from __future__ import annotations

import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

UA = "starred-hub-icon"
ICON_URL = "https://github.com/{owner}.png?size=200"
MIN_BYTES = 512


def _download(owner: str, target: Path) -> bool:
    if target.exists() and target.stat().st_size >= MIN_BYTES:
        return False
    url = ICON_URL.format(owner=owner)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = resp.read()
            ctype = resp.headers.get("Content-Type", "")
    except (urllib.error.URLError, OSError):
        return False
    if len(data) < MIN_BYTES or "image" not in ctype:
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return True


def ensure_icons(repos: list[dict], apps_dir: Path, workers: int = 8) -> int:
    """给每个应用文件夹补 icon.png，返回新下载的数量。"""
    jobs = []
    for repo in repos:
        cat = repo["cls"]["functions"][0]
        target = apps_dir / cat["slug"] / (repo.get("dir") or repo["name"]) / "icon.png"
        jobs.append((repo["owner"], target))

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda j: _download(*j), jobs))
    return sum(1 for r in results if r)
