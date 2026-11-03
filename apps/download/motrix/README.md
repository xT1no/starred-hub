<!-- 本文件由 starred-hub 自动生成，手动修改会在下次同步时被覆盖 -->

# Motrix

<img src="icon.png" width="72" align="right" alt="Motrix icon">

A full-featured download manager.

## ⬇️ 直接下载

🪟 [安装版 · 127 MB](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-Setup-2.2.1.exe) · 🍎 [arm64 dmg · 131 MB](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-arm64.dmg) · 🐧 [x64 AppImage · 125 MB](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-x86_64.AppImage) · 📦 [zip · 160 MB](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-win.zip)

全部 36 个文件见下方 [安装包](#pkgs) 表格。

| 项目 | 信息 |
|:---|:---|
| 仓库 | [agalwood/Motrix](https://github.com/agalwood/Motrix) |
| 分类 | 📥 [下载 / 网盘](../README.md) |
| 平台 | 🪟 🍎 🐧 🖥️ |
| 语言 | TypeScript |
| Star | 58k · Fork 5.1k |
| License | NOASSERTION |
| 最新版本 | `v2.2.1` |
| 最近更新 | 2026-11-03（今天） |
| 标星日期 | 2023-12-07 |
| 官网 | <https://motrix.app> |

## 📦 最新版本

**`v2.2.1`**　发布于 2026-11-03（今天）

[查看 Release 页面](https://github.com/agalwood/Motrix/releases/tag/v2.2.1)

<details><summary>更新说明</summary>

```text
# Motrix 2.2.1

English | [简体中文](https://github.com/agalwood/Motrix/blob/v2.2.1/docs/release-notes/2.2.1.zh-CN.md)

Motrix 2.2.1 fixes startup recovery for broken magnet sessions and HTTP retries
that previously lost their original request context or download progress.

## Changes since 2.2.0

- Keep a magnet task with missing torrent metadata or a deleted download directory
  from blocking engine startup. Recover from hash-verified application metadata
  where possible; otherwise, back up the engine database and retain the affected
  task as a removable error. Healthy tasks can start, repeated launches do not
  recreate deleted directories, and unrelated task history is preserved. Also
…（完整内容见 Release 页面）
```

</details>

<a id="pkgs"></a>

## ⬇️ 安装包

来自最新 Release，共 36 个文件。下表是官方直链，点名字即可下载。

| 文件 | 适用平台 | 大小 | 累计下载 |
|:---|:---:|:---|---:|
| [Motrix-2.2.1-arm64.dmg](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-arm64.dmg) | 🍎 macOS | 130.7 MB | 35 |
| [Motrix-2.2.1-x64.dmg](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-x64.dmg) | 🍎 macOS | 137.7 MB | 12 |
| [latest-mac.yml](https://github.com/agalwood/Motrix/releases/download/v2.2.1/latest-mac.yml) | 🍎 macOS | 490 B | 6 |
| [beta-mac.yml](https://github.com/agalwood/Motrix/releases/download/v2.2.1/beta-mac.yml) | 🍎 macOS | 490 B | 5 |
| [Motrix-2.2.1-arm64.dmg.blockmap](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-arm64.dmg.blockmap) | 🍎 macOS | 141 KB | 2 |
| [Motrix-2.2.1-x64.dmg.blockmap](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-x64.dmg.blockmap) | 🍎 macOS | 149 KB | 2 |
| [Motrix-Setup-2.2.1.exe](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-Setup-2.2.1.exe) | 🪟 Windows | 127.4 MB | 145 |
| [Motrix-2.2.1-win.zip](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-win.zip) | 🪟 Windows | 159.7 MB | 102 |
| [Motrix-Setup-2.2.1-arm64.exe](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-Setup-2.2.1-arm64.exe) | 🪟 Windows | 121.6 MB | 15 |
| [Motrix-2.2.1-win-arm64.zip](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-win-arm64.zip) | 🪟 Windows | 157.2 MB | 9 |
| [Motrix-Setup-2.2.1-arm64.exe.blockmap](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-Setup-2.2.1-arm64.exe.blockmap) | 🪟 Windows | 131 KB | 2 |
| [Motrix-Setup-2.2.1.exe.blockmap](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-Setup-2.2.1.exe.blockmap) | 🪟 Windows | 136 KB | 2 |
| [Motrix_2.2.1_amd64.deb](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix_2.2.1_amd64.deb) | 🐧 Linux | 106.7 MB | 54 |
| [Motrix-2.2.1-x86_64.AppImage](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-x86_64.AppImage) | 🐧 Linux | 125.4 MB | 21 |
| [Motrix-2.2.1-x86_64.AppImage.zsync](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-x86_64.AppImage.zsync) | 🐧 Linux | 220 KB | 17 |
| [Motrix-2.2.1-arm64.zip](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-arm64.zip) | 🐧 Linux | 125.6 MB | 10 |
| [Motrix-2.2.1.x86_64.rpm](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1.x86_64.rpm) | 🐧 Linux | 94.9 MB | 9 |
| [Motrix-2.2.1-arm64.AppImage](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1-arm64.AppImage) | 🐧 Linux | 125.6 MB | 7 |
| [Motrix_2.2.1_arm64.deb](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix_2.2.1_arm64.deb) | 🐧 Linux | 102.2 MB | 7 |
| [Motrix-2.2.1.aarch64.rpm](https://github.com/agalwood/Motrix/releases/download/v2.2.1/Motrix-2.2.1.aarch64.rpm) | 🐧 Linux | 90.4 MB | 6 |
| [beta-linux-arm64.yml](https://github.com/agalwood/Motrix/releases/download/v2.2.1/beta-linux-arm64.yml) | 🐧 Linux | 836 B | 5 |
| [beta-linux.yml](https://github.com/agalwood/Motrix/releases/download/v2.2.1/beta-linux.yml) | 🐧 Linux | 832 B | 5 |
| [latest-linux-arm64.yml](https://github.com/agalwood/Motrix/releases/download/v2.2.1/latest-linux-arm64.yml) | 🐧 Linux | 836 B | 5 |
| [latest-linux.yml](https://github.com/agalwood/Motrix/releases/download/v2.2.1/latest-linux.yml) | 🐧 Linux | 832 B | 5 |

还有 12 个文件，见 [Release 页面](https://github.com/agalwood/Motrix/releases/tag/v2.2.1)。

## 🔗 快速链接

- 仓库主页 · https://github.com/agalwood/Motrix
- Issues · https://github.com/agalwood/Motrix/issues
- Releases · https://github.com/agalwood/Motrix/releases
- 官网 / 演示 · https://motrix.app

`aria2` `bt` `download` `electron` `linux` `mac` `macos` `magnet` `motrix` `torrent` `windows`

---

← 返回 [📥 下载 / 网盘](../README.md) · [全部应用](../../README.md) · [星标总览](../../../README.md)
