# ⭐ Starred Hub

我的 GitHub 星标仓库自动归档。

每天 08:00（北京时间）由 GitHub Actions 自动扫描星标列表，按**功能**和**平台**两个维度重新分类并更新文档。

---

_首次同步尚未运行。执行 `Actions → Sync starred repos → Run workflow` 后，本文件会被自动生成的内容替换。_

| 文件 | 作用 |
|:---|:---|
| `config/rules.toml` | 分类关键词规则 |
| `config/overrides.toml` | 手动指定某个仓库的分类 |
| `scripts/sync.py` | 同步主程序（纯标准库，无第三方依赖） |
| `.github/workflows/sync-stars.yml` | 每天 8 点的定时任务 |
