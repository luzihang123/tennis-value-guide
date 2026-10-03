# 网站技术架构

## 阅读方式

参考 [HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter)：网站是静态 HTML 加原生 JavaScript，浏览器通过 `fetch` 读取 Markdown；不需要数据库或后端，也不使用电子书框架。本站保留独立的页面设计，用相同的内容读取方式。

- `book/` 是跨城市的中文正文，器材测评属于这里。
- `cities/<城市>/<主题>/README.md` 是城市主题入口，同目录的 Markdown 是子文章。
- `site/index.html`、`site/en/index.html`、`site/ja/index.html` 是三语目录。
- `site/reader.html`、`site/en/reader.html`、`site/ja/reader.html` 共用 `site/reader.js`，在浏览器中读取对应 Markdown，并把正文里的相对链接保持为站内阅读链接。
- `site/build_locales.py` 生成三语目录与阅读器外壳，将 Markdown 复制到 `site/content/`。GitHub Pages 部署时自动执行；这个复制目录不提交到 Git。

## 内容与翻译

中文先写、先核对。英文和日文目前只翻译界面与目录，正文沿用中文，并在阅读页说明。将来有经过确认的译文时，再按同一文章路径增加语言版本。

本地预览先运行 `python3 site/build_locales.py`，再在 `site/` 目录运行 `python3 -m http.server 8000`。浏览器通过 HTTP 读取 Markdown，直接打开本地 HTML 文件无法正常加载正文。
