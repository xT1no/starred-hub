<!-- 本文件由 starred-hub 自动生成，手动修改会在下次同步时被覆盖 -->

# iptv-api

<img src="icon.png" width="72" align="right" alt="iptv-api icon">

⚡️ IPTV直播源自动更新工具：自动采集、校验、测速并生成可播放结果，支持 M3U/TXT/API 输出、自定义频道、IPv4/IPv6、Docker、GitHub Actions、CLI 与 GUI 多端部署

| 项目 | 信息 |
|:---|:---|
| 仓库 | [Guovin/iptv-api](https://github.com/Guovin/iptv-api) |
| 分类 | ⚡ [自动化 / 部署](../README.md) |
| 平台 | 📺 ⌨️ |
| 语言 | Python |
| Star | 26k · Fork 7.6k |
| License | NOASSERTION |
| 最新版本 | `3.1.0` |
| 最近更新 | 2026-10-12（16 天前） |
| 标星日期 | 2026-04-16 |
| 官网 | <https://guovin.github.io/iptv-api/> |

## 📦 最新版本

**`3.1.0`** · v3.1.0　发布于 2026-10-12（16 天前）

[查看 Release 页面](https://github.com/Guovin/iptv-api/releases/tag/3.1.0)

<details><summary>更新说明</summary>

```text
### 2026/10/12

### 🚀 新增功能

- 桌面版支持自动下载、校验和安装更新，并保留用户配置及运行数据。
- 支持在设置中迁移配置与输出目录，便于便携使用和备份（#1403）。
- GitHub Actions 生成的订阅支持通过 GitHub Pages 访问、预览和复制链接，通过 Releases 下载历史结果；同时提供运行日志和中英文切换。
- 扩充频道别名库，优化别名与数据源编辑体验；修改别名后下次更新即可生效，无需重启（#1082、#1418）。

### 🐛 修复与优化

- 优化大规模频道数据的查询与界面刷新，减少频道管理卡顿（#1408）。
- 限制 EPG 解析和直播采样的资源占用，修复单个请求取消导致整轮测速中断的问题（#1389、#1407）。
- 修复 Docker 代理配置被空环境变量覆盖的问题，直播测速与媒体探测保持直连，恢复 HLS 临时目录兼容性。
…（完整内容见 Release 页面）
```

</details>

## ⬇️ 安装包

来自最新 Release，共 3 个文件。下表是官方直链，点名字即可下载。

| 文件 | 适用平台 | 大小 | 累计下载 |
|:---|:---:|:---|---:|
| [IPTV-API-GUI-macOS-ARM64-v3.1.0.zip](https://github.com/Guovin/iptv-api/releases/download/3.1.0/IPTV-API-GUI-macOS-ARM64-v3.1.0.zip) | 🍎 macOS | 67.8 MB | 271 |
| [IPTV-API-GUI-Windows-X64-v3.1.0.zip](https://github.com/Guovin/iptv-api/releases/download/3.1.0/IPTV-API-GUI-Windows-X64-v3.1.0.zip) | 🪟 Windows | 82.5 MB | 1.4k |
| [SHA256SUMS.txt](https://github.com/Guovin/iptv-api/releases/download/3.1.0/SHA256SUMS.txt) | 🔐 校验文件 | 204 B | 158 |

## 🔗 快速链接

- 仓库主页 · https://github.com/Guovin/iptv-api
- Issues · https://github.com/Guovin/iptv-api/issues
- Releases · https://github.com/Guovin/iptv-api/releases
- 官网 / 演示 · https://guovin.github.io/iptv-api/

`auto-update` `awesome` `epg` `iptv` `iptv-api` `iptv-channels` `iptv-free` `iptv-m3u` `iptv-m3u8` `iptv-playlist` `ipv4` `ipv6`

---

← 返回 [⚡ 自动化 / 部署](../README.md) · [全部应用](../../README.md) · [星标总览](../../../README.md)
