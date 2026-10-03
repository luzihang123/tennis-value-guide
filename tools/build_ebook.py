#!/usr/bin/env python3
"""Build a draft EPUB and standalone HTML from the ordered Markdown chapters."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist"
# The boolean marks a section inside a chapter; its headings shift down one level.
CHAPTERS = [
    ("book/00-阅读指南.md", False),
    ("book/01-入门与预算.md", False),
    ("book/02-技术与练习/README.md", False),
    ("book/02-技术与练习/基础动作.md", True),
    ("book/02-技术与练习/单人练习.md", True),
    ("book/02-技术与练习/练习计划.md", True),
    ("book/02-技术与练习/从其他球类学习网球.md", True),
    ("book/03-装备与训练器材/README.md", False),
    ("book/03-装备与训练器材/球拍与拍线.md", True),
    ("book/03-装备与训练器材/球鞋与服装.md", True),
    ("book/03-装备与训练器材/网球与耗材.md", True),
    ("book/03-装备与训练器材/发球机.md", True),
    ("book/04-数字工具与智能硬件/README.md", False),
    ("book/04-数字工具与智能硬件/网球小程序.md", True),
    ("book/04-数字工具与智能硬件/独立App.md", True),
    ("book/04-数字工具与智能硬件/智能硬件.md", True),
    ("book/05-健身/README.md", False),
    ("book/05-健身/网球专项体能.md", True),
    ("book/05-健身/恢复与伤病预防.md", True),
    ("book/05-健身/饮食与补水.md", True),
    ("book/06-场地与订场.md", False),
    ("book/07-约球与比赛.md", False),
    ("cities/README.md", False),
    ("cities/上海/README.md", True),
    ("cities/上海/订场.md", True),
    ("cities/上海/网球墙.md", True),
    ("cities/上海/陪练.md", True),
    ("cities/上海/约球.md", True),
]


def prepare(source: str, nested: bool) -> str:
    content = (ROOT / source).read_text(encoding="utf-8").strip()
    # The EPUB and standalone HTML use their own table of contents. Local .md
    # links would point outside those files, so show the link text instead.
    content = re.sub(
        r"\[([^\]]+)\]\((?!https?://|mailto:|#)[^)]+\.md(?:#[^)]*)?\)",
        r"\1",
        content,
    )
    if nested:
        content = re.sub(r"^(#{1,5})(?=\s)", r"#\1", content, flags=re.MULTILINE)
    return content


def main() -> int:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        print("缺少 Pandoc：请先安装 https://pandoc.org/installing.html", file=sys.stderr)
        return 1

    missing = [source for source, _ in CHAPTERS if not (ROOT / source).is_file()]
    if missing:
        print("缺少章节文件：" + ", ".join(missing), file=sys.stderr)
        return 1

    OUTPUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        manuscript = Path(temp_dir) / "book.md"
        manuscript.write_text(
            "\n\n".join(prepare(source, nested) for source, nested in CHAPTERS) + "\n",
            encoding="utf-8",
        )
        common = [
            pandoc,
            str(manuscript),
            "--from=gfm",
            "--standalone",
            "--toc",
            "--toc-depth=2",
            "--metadata=title:网球划算学",
            "--metadata=lang:zh-CN",
        ]
        for output_file, options in [
            (OUTPUT / "网球划算学.epub", ["--to=epub3", "--split-level=1"]),
            (OUTPUT / "网球划算学.html", ["--to=html5", "--embed-resources"]),
        ]:
            subprocess.run(common + options + ["--output", str(output_file)], check=True)
            print(output_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
