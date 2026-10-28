<!-- 本文件由 starred-hub 自动生成，手动修改会在下次同步时被覆盖 -->

# localsend

<img src="icon.png" width="72" align="right" alt="localsend icon">

> 跨设备局域网文件互传（类 AirDrop）

An open-source cross-platform alternative to AirDrop

| 项目 | 信息 |
|:---|:---|
| 仓库 | [localsend/localsend](https://github.com/localsend/localsend) |
| 分类 | ⚙️ [系统增强 / 优化](../README.md) |
| 平台 | 🖥️ |
| 语言 | Dart |
| Star | 96k · Fork 5.4k |
| License | Apache-2.0 |
| 最新版本 | `v1.18.2` |
| 最近更新 | 2026-08-21（2 个月前） |
| 标星日期 | 2025-10-28 |
| 官网 | <https://localsend.org> |

## 📦 最新版本

**`v1.18.2`**　发布于 2026-08-21（2 个月前）

[查看 Release 页面](https://github.com/localsend/localsend/releases/tag/v1.18.2)

<details><summary>更新说明</summary>

```text
This release fixes compatibility issues with 1.17.0 and earlier.
Note: The Windows binaries have been updated to include a signature.

- feat: drag and drop files into the "Receive via link" browser page
- feat(desktop): allow customizing the web share pages by placing HTML files in a `web` folder next to the executable
- feat(cli): add version info to the Windows executable
- feat(linux): set actual version in the AppImage
- security: do not follow HTTP redirects sent by peers
- fix: restore compatibility with 1.17.0 and earlier versions on missing multicast networks
- fix: devices running 1.17.0 and earlier could not add 1.18.0+ device as favorite
- fix: ignore proxies, fixes "TLS info not found" when a system proxy (e.g. Shadowrocket) is enabled
- fix: automatically restart the HTTP / multicast server when it dies or when the app resumes
- fix: drag and drop with a mix of folders and files
…（完整内容见 Release 页面）
```

</details>

## ⬇️ 安装包

来自最新 Release，共 20 个文件。下表是官方直链，点名字即可下载。

| 文件 | 适用平台 | 大小 | 累计下载 |
|:---|:---:|:---|---:|
| [LocalSend-1.18.2.dmg](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2.dmg) | 🍎 macOS | 50.3 MB | 638k |
| [LocalSend-CLI-1.18.2-macos-arm-64.tar.gz](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-CLI-1.18.2-macos-arm-64.tar.gz) | 🍎 macOS | 3.9 MB | 2k |
| [LocalSend-CLI-1.18.2-macos-x86-64.tar.gz](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-CLI-1.18.2-macos-x86-64.tar.gz) | 🍎 macOS | 4.2 MB | 1.3k |
| [LocalSend-1.18.2-android-arm64v8.apk](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-android-arm64v8.apk) | 📲 Android | 44.4 MB | 190k |
| [LocalSend-1.18.2-android-arm32v7.apk](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-android-arm32v7.apk) | 📲 Android | 37.5 MB | 21k |
| [LocalSend-1.18.2-android-google-play.apk](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-android-google-play.apk) | 📲 Android | 122.3 MB | 21k |
| [LocalSend-1.18.2-android-x64.apk](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-android-x64.apk) | 📲 Android | 46.7 MB | 8.3k |
| [LocalSend-1.18.2-windows-x86-64.exe](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-windows-x86-64.exe) | 🪟 Windows | 19.0 MB | 745k |
| [LocalSend-1.18.2-windows-x86-64-unsigned.exe](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-windows-x86-64-unsigned.exe) | 🪟 Windows | 18.1 MB | 173k |
| [LocalSend-1.18.2-windows-x86-64.zip](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-windows-x86-64.zip) | 🪟 Windows | 24.9 MB | 141k |
| [LocalSend-1.18.2-windows-arm-64.zip](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-windows-arm-64.zip) | 🪟 Windows | 23.3 MB | 6.9k |
| [LocalSend-CLI-1.18.2-windows-x86-64.exe](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-CLI-1.18.2-windows-x86-64.exe) | 🪟 Windows | 9.3 MB | 6k |
| [LocalSend-CLI-1.18.2-windows-arm-64.exe](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-CLI-1.18.2-windows-arm-64.exe) | 🪟 Windows | 8.0 MB | 1.3k |
| [LocalSend-1.18.2-linux-x86-64.deb](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-linux-x86-64.deb) | 🐧 Linux | 23.5 MB | 97k |
| [LocalSend-1.18.2-linux-x86-64.AppImage](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-linux-x86-64.AppImage) | 🐧 Linux | 63.4 MB | 27k |
| [LocalSend-1.18.2-linux-x86-64.tar.gz](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-linux-x86-64.tar.gz) | 🐧 Linux | 30.5 MB | 17k |
| [LocalSend-1.18.2-linux-arm-64.deb](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-linux-arm-64.deb) | 🐧 Linux | 23.5 MB | 7k |
| [LocalSend-CLI-1.18.2-linux-x86-64.tar.gz](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-CLI-1.18.2-linux-x86-64.tar.gz) | 🐧 Linux | 4.5 MB | 3.1k |
| [LocalSend-1.18.2-linux-arm-64.tar.gz](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-1.18.2-linux-arm-64.tar.gz) | 🐧 Linux | 30.9 MB | 2.8k |
| [LocalSend-CLI-1.18.2-linux-arm-64.tar.gz](https://github.com/localsend/localsend/releases/download/v1.18.2/LocalSend-CLI-1.18.2-linux-arm-64.tar.gz) | 🐧 Linux | 4.4 MB | 1.3k |

## 🔗 快速链接

- 仓库主页 · https://github.com/localsend/localsend
- Issues · https://github.com/localsend/localsend/issues
- Releases · https://github.com/localsend/localsend/releases
- 官网 / 演示 · https://localsend.org

`dart` `file-sharing` `flutter` `flutter-apps`

---

← 返回 [⚙️ 系统增强 / 优化](../README.md) · [全部应用](../../README.md) · [星标总览](../../../README.md)
