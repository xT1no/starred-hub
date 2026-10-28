<!-- 本文件由 starred-hub 自动生成，手动修改会在下次同步时被覆盖 -->

# cloud-fs.github.io

<img src="icon.png" width="72" align="right" alt="cloud-fs.github.io icon">

> CloudFS 网盘挂载文档站

| 项目 | 信息 |
|:---|:---|
| 仓库 | [cloud-fs/cloud-fs.github.io](https://github.com/cloud-fs/cloud-fs.github.io) |
| 分类 | 📥 [下载 / 网盘](../README.md) |
| 平台 | 🐧 |
| 语言 | — |
| Star | 1.7k · Fork 63 |
| License | — |
| 最新版本 | `v1.1.3` |
| 最近更新 | 2026-10-17（10 天前） |
| 标星日期 | 2023-12-06 |

## 📦 最新版本

**`v1.1.3`**　发布于 2026-10-17（10 天前）

[查看 Release 页面](https://github.com/cloud-fs/cloud-fs.github.io/releases/tag/v1.1.3)

<details><summary>更新说明</summary>

```text
CloudDrive2 Core V1.1.3(Web3.1.3)

1. SMB 存储的共享名称可以留空(#630)。 留空时添加的是整台服务器，服务器上的每个共享显示为一个文件夹，不包括 IPC$、C$、ADMIN$ 等管理共享。共享本身不能删除或重命名，也不能在共享这一层新建文件夹或上传文件；不同共享之间不能直接移动文件。填写了共享名称的存储与以前相同。网页版添加 SMB 存储时，
2. 修复从部分 NAS 通过 SMB 复制或读取文件时停在 0 B 的问题(#619)。 一次读取的数据量超过服务器允许的大小时，现在分成多次读取。SMB 存储中设置的端口以前不生效，总是使用 445，现在使用设置的端口
3. 修复复制或上传时个别文件一直显示"预处理中"，所有传输停止，只有重启服务才能恢复的问题(#634)。 预处理连续 30 分钟没有进展时，会结束并自动重试；对一直显示"预处理中"的项目暂停再恢复，会重新开始预处理
4. 修复 123 云盘等 WebDAV 存储挂载一段时间后，部分文件一直下载失败（403 Forbidden），只有删除后重新添加才能恢复的问题(#627)。 WebDAV 服务器给出的下载链接最多使用 10 分钟；下载失败时，会重新向服务器获取链接
5. 修复添加 S3 存储时选择"不要将这些设置同步到云端"不生效的问题(#629)。 以前 S3 存储总是同步到其他设备。已经同步的 S3 存储，需要删除后重新添加，并选择这个选项
6. 修复 S3 存储经过开启了 HTTP/2 的 NGINX（1.26 及更早版本）或雷池 WAF 反向代理时，返回 400 Bad Request 的问题(#629)。 S3 请求失败时，错误信息中会显示具体原因
…（完整内容见 Release 页面）
```

</details>

## ⬇️ 安装包

来自最新 Release，共 13 个文件。下表是官方直链，点名字即可下载。

| 文件 | 适用平台 | 大小 | 累计下载 |
|:---|:---:|:---|---:|
| [clouddrive-2-macos-aarch64-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-macos-aarch64-1.1.3.tgz) | 🍎 macOS | 13.5 MB | 612 |
| [clouddrive-2-macos-x86_64-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-macos-x86_64-1.1.3.tgz) | 🍎 macOS | 14.8 MB | 384 |
| [clouddrive-2-android-universal-1.1.3-233.apk](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-android-universal-1.1.3-233.apk) | 📲 Android | 46.1 MB | 1.6k |
| [clouddrive-2-android-aarch64-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-android-aarch64-1.1.3.tgz) | 📲 Android | 14.4 MB | 382 |
| [clouddrive-2-android-armv7-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-android-armv7-1.1.3.tgz) | 📲 Android | 14.0 MB | 333 |
| [clouddrive-2-android-x86_64-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-android-x86_64-1.1.3.tgz) | 📲 Android | 15.3 MB | 330 |
| [CloudDrive2Setup-X64-1.1.3.exe](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/CloudDrive2Setup-X64-1.1.3.exe) | 🪟 Windows | 13.9 MB | 2.7k |
| [CloudDrive2Setup-Arm64-1.1.3.exe](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/CloudDrive2Setup-Arm64-1.1.3.exe) | 🪟 Windows | 12.9 MB | 425 |
| [clouddrive-2-linux-x86_64-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-linux-x86_64-1.1.3.tgz) | 🐧 Linux | 15.3 MB | 850 |
| [clouddrive-2-linux-aarch64-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-linux-aarch64-1.1.3.tgz) | 🐧 Linux | 14.2 MB | 609 |
| [clouddrive-2-linux-armv7-1.1.3.tgz](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive-2-linux-armv7-1.1.3.tgz) | 🐧 Linux | 16.0 MB | 422 |
| [clouddrive2_1.1.3_x86.fpk](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive2_1.1.3_x86.fpk) | 📦 其他 | 15.7 MB | 584 |
| [clouddrive2_1.1.3_arm.fpk](https://github.com/cloud-fs/cloud-fs.github.io/releases/download/v1.1.3/clouddrive2_1.1.3_arm.fpk) | 📦 其他 | 14.8 MB | 206 |

## 🔗 快速链接

- 仓库主页 · https://github.com/cloud-fs/cloud-fs.github.io
- Issues · https://github.com/cloud-fs/cloud-fs.github.io/issues
- Releases · https://github.com/cloud-fs/cloud-fs.github.io/releases

---

← 返回 [📥 下载 / 网盘](../README.md) · [全部应用](../../README.md) · [星标总览](../../../README.md)
