# 网站技术架构（目标方案）

## 原则

- 中文是唯一的原始正文。先审核中文，再翻译英文、日文。
- 同一篇文章在三种语言下使用相同的相对路径，便于切换与追踪。
- 翻译缺失时明确提示“此篇暂只有中文”，不暗中显示机器译文。
- 网页由 Markdown 静态生成，通过现有 GitHub Pages 发布；不需要数据库或后端。

## 目标目录

```text
docs/
├── .vitepress/config.mts       # 导航、语言切换、站点路径
├── index.md                    # 中文首页
├── guide/                      # 中文通用指南，文件名用稳定 slug
├── cities/
│   ├── shanghai/
│   └── tokyo/
├── en/
│   ├── index.md                # 英文首页；正文译文确认后再逐篇加入
│   ├── guide/
│   └── cities/
└── ja/
    ├── index.md                # 日文首页；正文译文确认后再逐篇加入
    ├── guide/
    └── cities/
```

例如中文 `docs/guide/first-session.md`、英文 `docs/en/guide/first-session.md` 和日文 `docs/ja/guide/first-session.md` 是同一篇文章。页面路径不随标题翻译而变化。

## 内容流程

1. 中文正文通过 PR 审核合并。
2. AI 以已确认的中文版为输入生成译文草稿，分别放进 `en/`、`ja/`。
3. 人工检查术语、数字、来源链接和本地信息后合并。译文记录对应的中文版本；中文改动后提示译文可能过期。
4. GitHub Actions 构建静态网页并发布到 Pages。语言切换只指向已存在的对应页面；缺失译文显示语言首页的说明。

## 当前阶段

目前保留 `book/`、`cities/` 中的中文原稿。静态首页已提供中文、英文、日文三种目录骨架和切换入口，生成脚本是 `site/build_locales.py`；各语种的正文仍指向中文，页面有明确提示。东京只建中文目录骨架。确认正文后，再逐篇翻译并迁移到上面的 VitePress 结构。
