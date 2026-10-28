"""示例数据 —— 只用于 `python scripts/sync.py --demo` 预览排版，不参与正式同步。"""
from datetime import datetime, timedelta, timezone

_TZ = timezone(timedelta(hours=8))


def _days_ago(n: int) -> str:
    return (datetime.now(_TZ) - timedelta(days=n)).isoformat(timespec="seconds")


DEMO_RAW = [
    {
        "full_name": "microsoft/PowerToys",
        "description": "Windows 效率增强工具集，包含窗口管理、快捷键、批量重命名等模块",
        "topics": ["windows", "poweruser", "productivity", "utilities"],
        "language": "C#",
        "stars": 118000,
        "starred_at": _days_ago(2),
    },
    {
        "full_name": "yt-dlp/yt-dlp",
        "description": "A feature-rich command-line audio/video downloader",
        "topics": ["cli", "downloader", "youtube", "ffmpeg"],
        "language": "Python",
        "stars": 102000,
        "starred_at": _days_ago(5),
    },
    {
        "full_name": "obsidianmd/obsidian-releases",
        "description": "Obsidian 的插件与主题发布仓库，本地 Markdown 笔记生态",
        "topics": ["markdown", "note-taking", "knowledge-base"],
        "language": "TypeScript",
        "stars": 8100,
        "starred_at": _days_ago(1),
    },
    {
        "full_name": "localsend/localsend",
        "description": "An open-source cross-platform alternative to AirDrop",
        "topics": ["flutter", "android", "ios", "windows", "macos", "linux", "file-sharing"],
        "language": "Dart",
        "stars": 58000,
        "starred_at": _days_ago(9),
    },
    {
        "full_name": "Kaiyangzhou/dassl.pytorch",
        "description": "A PyTorch toolbox for domain adaptation and semi-supervised learning",
        "topics": ["machine-learning", "deep-learning", "pytorch"],
        "language": "Python",
        "stars": 1300,
        "starred_at": _days_ago(40),
    },
    {
        "full_name": "2dust/v2rayN",
        "description": "A GUI client for Windows, Linux and macOS, support Xray core and sing-box",
        "topics": ["proxy", "vpn", "windows", "linux", "macos"],
        "language": "C#",
        "stars": 79000,
        "starred_at": _days_ago(13),
    },
    {
        "full_name": "smarttubeapp/smarttube",
        "description": "Advanced YouTube client for Android TV with ad blocking and SponsorBlock",
        "topics": ["android-tv", "youtube", "leanback", "video"],
        "language": "Kotlin",
        "stars": 20000,
        "starred_at": _days_ago(6),
    },
    {
        "full_name": "ffmpegwasm/ffmpeg.wasm",
        "description": "FFmpeg for browser, powered by WebAssembly",
        "topics": ["webassembly", "ffmpeg", "video", "browser"],
        "language": "JavaScript",
        "stars": 15000,
        "starred_at": _days_ago(70),
    },
    {
        "full_name": "sindresorhus/awesome",
        "description": "😎 Awesome lists about all kinds of interesting topics",
        "topics": ["awesome-list", "lists", "resources"],
        "language": "",
        "stars": 350000,
        "starred_at": _days_ago(200),
    },
    {
        "full_name": "hoppscotch/hoppscotch",
        "description": "Open source API development ecosystem - Postman 的开源替代",
        "topics": ["api", "developer-tools", "pwa", "vue"],
        "language": "TypeScript",
        "stars": 65000,
        "starred_at": _days_ago(3),
    },
    {
        "full_name": "Genymobile/scrcpy",
        "description": "Display and control your Android device",
        "topics": ["android", "adb", "cli", "screen-mirroring"],
        "language": "C",
        "stars": 112000,
        "starred_at": _days_ago(120),
    },
    {
        "full_name": "chatboxai/chatbox",
        "description": "User-friendly Desktop Client App for AI Models/LLMs (GPT, Claude, Gemini)",
        "topics": ["ai", "chatgpt", "electron", "desktop-app", "llm"],
        "language": "TypeScript",
        "stars": 32000,
        "starred_at": _days_ago(4),
    },
    {
        "full_name": "shahedbd/awesome-android-tv",
        "description": "A curated list of awesome Android TV apps, tools and resources",
        "topics": ["awesome-list", "android-tv", "resources"],
        "language": "",
        "stars": 620,
        "starred_at": _days_ago(320),
    },
    {
        "full_name": "lobehub/lobe-chat",
        "description": "🤯 Lobe Chat - an open-source, modern design AI chat framework",
        "topics": ["ai", "chatgpt", "nextjs", "self-hosted", "design-system"],
        "language": "TypeScript",
        "stars": 55000,
        "starred_at": _days_ago(8),
    },
]
