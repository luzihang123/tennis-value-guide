# 项目协作说明

- 项目名称：《高性价比网球指南》。先确认中文内容，再翻译英文和日文；不要自动扩写未确认的正文。
- `book/` 存放跨城市内容，器材测评也在这里；`cities/` 存放城市资料。上海和东京都使用相同的十个城市主题及编号顺序；每个主题目录含 `README.md` 和子文章。
- 网页采用静态 HTML、原生 JavaScript 和 Markdown。`site/reader.js` 在浏览器中读取并展示 Markdown，站内文章链接保持在网站内。英文、日文界面已翻译，正文仍以中文为准。
- `site/build_locales.py` 生成三语首页和阅读器外壳，并将 `book/`、`cities/` 复制到 `site/content/`。改目录、文章或网页文案后运行 `python3 site/build_locales.py`；提交生成的首页和阅读器 HTML，`site/content/` 不入库。GitHub Pages 部署时会重新运行脚本。
- 检查三语首页中上海、东京各十个主题入口、通用指南的器材文章、城市主题的子文章、站内跳转，以及 `git diff --check`。
- `agents/` 是本地讨论资料目录，已被 `.gitignore` 忽略；公开的协作约定写在本文件。
