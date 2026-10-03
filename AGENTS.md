# 项目协作说明

- 项目名称：《高性价比网球指南》。先确认中文内容，再翻译英文和日文；不要自动扩写未确认的正文。
- `book/` 存放跨城市内容，`cities/` 存放城市资料。上海和东京都使用相同的九个城市主题及编号顺序；新增城市时沿用这套目录。
- `site/build_locales.py` 是当前网页的生成入口。改首页目录、文案或空白详情页模板后，运行 `python3 site/build_locales.py`，并提交生成的 `site/` HTML。GitHub Pages 部署时也会运行该脚本。
- 当前尚未从 Markdown 自动生成站内文章。`#guide` 的七个站内详情页只是空骨架；城市主题仍链接到 GitHub Markdown。接入 Markdown 渲染时，再更新这条规则和生成脚本。
- 检查三语首页的城市选择器、九个城市链接、七个指南详情页，以及 `git diff --check`。
- `agents/` 是本地讨论资料目录，已被 `.gitignore` 忽略；公开的协作约定写在本文件。
