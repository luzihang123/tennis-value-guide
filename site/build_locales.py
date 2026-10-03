#!/usr/bin/env python3
"""Generate language shells and copy Markdown for the browser reader."""
from html import escape
from pathlib import Path
from shutil import copytree, rmtree
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent
REPO = 'https://github.com/luzihang123/tennis-value-guide'
BASE = 'https://clarklu.com/tennis-value-guide/'
CITY_DIRS = (('shanghai', '上海'), ('tokyo', '东京'))
CITY_TOPICS = ['01-订场', '02-约球', '03-教练', '04-陪练', '05-网球墙',
               '06-发球机与练习场', '07-试拍与租拍', '08-穿线',
               '09-赛事与活动', '10-网旅']
GUIDE_PATHS = [
    'book/01-入门与预算.md', 'book/02-技术与练习/README.md',
    'book/03-装备与训练器材/README.md', 'book/04-数字工具与智能硬件/README.md',
    'book/05-健身/README.md', 'book/06-场地与订场.md',
    'book/07-约球与比赛.md',
]
CITY_GROUPS = ((0, 6), (6, 8), (8, 10))
TEXT = {
    'zh': {
        'lang': 'zh-CN', 'title': '高性价比网球指南', 'nav': ('指南', '城市'),
        'hero': ('把钱和时间', '花在更多好球上。'),
        'intro': '从入门、练习和装备，到健身、场地与约球。中文正文持续更新，英文和日文译文会在中文确认后加入。',
        'button': '查看指南 ↓', 'guide': '指南目录', 'city_heading': '城市篇',
        'city_intro': '从上海和东京开始。东京篇目前是待确认的中文骨架。',
        'notice': '目前正文以中文为准。英文和日文先提供已翻译的目录骨架。',
        'topics': [
            ('入门与预算', '从第一次打球开始'), ('技术与练习', '动作、计划与跨球类学习'),
            ('装备与训练器材', '球拍、球鞋、发球机'), ('数字工具与智能硬件', '小程序、App、硬件'),
            ('健身', '体能、恢复与饮食'), ('场地与订场', '怎样比较场地'), ('约球与比赛', '找球友、拼场、比赛'),
        ],
        'cities': ('上海', '东京'),
        'city_topics': ('订场', '约球', '教练', '陪练', '网球墙', '发球机与练习场', '试拍与租拍', '穿线', '赛事与活动', '网旅'),
        'city_groups': ('打球与练习', '器材与服务', '活动与网旅'),
        'detail_pending': '内容待整理。', 'back': '返回指南目录',
        'overview': '概览', 'back_city': '返回城市目录', 'back_topic': '返回分类目录',
        'contribute': '参与共建 ↗',
    },
    'en': {
        'lang': 'en', 'title': 'Tennis Value Guide', 'nav': ('Guide', 'Cities'),
        'hero': ('Spend less time guessing.', 'Play more good tennis.'),
        'intro': 'A practical outline for getting started, practising, choosing gear, staying fit and finding places to play.',
        'button': 'Explore the guide ↓', 'guide': 'Guide outline', 'city_heading': 'City guides',
        'city_intro': 'Starting with Shanghai and Tokyo.',
        'notice': 'The detailed articles currently exist in Chinese. English translations will follow after the Chinese text is reviewed.',
        'topics': [
            ('Getting started & budget', 'Plan your first sessions'), ('Technique & practice', 'Strokes, routines and skills from other sports'),
            ('Gear & training tools', 'Rackets, shoes and ball machines'), ('Digital tools & smart hardware', 'Mini apps, apps and devices'),
            ('Fitness', 'Conditioning, recovery and food'), ('Courts & booking', 'Compare the real cost of a court'),
            ('Partners & matches', 'Find players and join matches'),
        ],
        'cities': ('Shanghai', 'Tokyo'),
        'city_topics': ('Courts', 'Find players', 'Coaches', 'Hitting partners', 'Practice walls',
                        'Ball machines & practice courts', 'Demo & rental rackets', 'Stringing',
                        'Tournaments & events', 'Tennis trips'),
        'city_groups': ('Play & practice', 'Gear & services', 'Events & trips'),
        'detail_pending': 'Content coming soon.', 'back': 'Back to the guide',
        'overview': 'Overview', 'back_city': 'Back to city topics', 'back_topic': 'Back to this topic',
        'contribute': 'Contribute ↗',
    },
    'ja': {
        'lang': 'ja', 'title': 'コスパのよいテニスガイド', 'nav': ('ガイド', '都市別'),
        'hero': ('お金と時間を賢く使って、', 'もっとテニスを楽しもう。'),
        'intro': '始め方、練習、用具、体づくり、コート探し、仲間探しをまとめたガイドの骨組みです。',
        'button': 'ガイドを見る ↓', 'guide': 'ガイドの目次', 'city_heading': '都市別ガイド',
        'city_intro': '上海と東京から始めます。',
        'notice': '詳しい記事は現在中国語のみです。中国語版の内容確認後、順次日本語に翻訳します。',
        'topics': [
            ('始め方と予算', '最初の一歩と費用'), ('技術と練習', '基本動作、練習計画、他競技からの学び'),
            ('用具と練習器具', 'ラケット、シューズ、球出し機'), ('デジタルツールとスマート機器', 'ミニアプリ、アプリ、機器'),
            ('体づくり', '体力、回復、食事'), ('コートと予約', 'コートの実質的な費用を比べる'),
            ('仲間と試合', '相手を探し、試合に参加する'),
        ],
        'cities': ('上海', '東京'),
        'city_topics': ('コート予約', '仲間探し', 'コーチ', '練習相手', '壁打ち', '球出し機と練習場',
                        '試打とレンタル', 'ガット張り', '大会とイベント', 'テニス旅行'),
        'city_groups': ('プレーと練習', '用具とサービス', 'イベントと旅行'),
        'detail_pending': '内容は準備中です。', 'back': 'ガイドの目次に戻る',
        'overview': '概要', 'back_city': '都市別の目次に戻る', 'back_topic': 'カテゴリに戻る',
        'contribute': '共同編集 ↗',
    },
}



def reader_link(path):
    return 'reader.html?path=' + quote(path, safe='')


def render_home(code, data):
    q = lambda value: escape(value, quote=True)
    prefix = '../' if code != 'zh' else ''
    navigation = f'<a href="#guide">{q(data["nav"][0])}</a><a href="#cities">{q(data["nav"][1])}</a><a href="{REPO}">GitHub ↗</a>'
    languages = ''
    for key, label in [('zh', '中文'), ('en', 'English'), ('ja', '日本語')]:
        active = ' aria-current="page"' if key == code else ''
        url = './' if key == code else ('../' if key == 'zh' else f'{"" if code == "zh" else "../"}{key}/')
        languages += f'<a href="{url}" lang="{TEXT[key]["lang"]}"{active}>{label}</a>'
    cards = ''.join(
        f'<a href="{reader_link(path)}"><small>{i:02d}</small><strong>{q(title)}</strong><span>{q(desc)}</span></a>'
        for i, (path, (title, desc)) in enumerate(zip(GUIDE_PATHS, data['topics']), 1)
    )
    cities = ''.join(
        '<div class="city-block">'
        f'<h3>{q(data["cities"][city_index])}</h3>'
        + ''.join(
            f'<div class="city-group"><h4>{q(data["city_groups"][group_index])}</h4><div class="city-links">'
            + ''.join(
                f'<a href="{reader_link(f"cities/{city_dir}/{CITY_TOPICS[i]}/README.md")}">{q(data["city_topics"][i])} ↗</a>'
                for i in range(start, end)
            ) + '</div></div>'
            for group_index, (start, end) in enumerate(CITY_GROUPS)
        ) + '</div>'
        for city_index, (_, city_dir) in enumerate(CITY_DIRS)
    )
    alternates = ''.join(
        f'<link rel="alternate" hreflang="{TEXT[key]["lang"]}" href="{BASE}{"" if key == "zh" else key + "/"}">'
        for key in TEXT
    )
    return f'''<!doctype html>
<html lang="{data['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{q(data['intro'])}">
  <title>{q(data['title'])}</title>
  {alternates}
  <link rel="icon" type="image/svg+xml" href="{prefix}logo.svg">
  <link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
  <header class="wrap"><a class="brand" href="#top"><img src="{prefix}logo.svg" alt="">{q(data['title'])}</a><nav>{navigation}</nav><div class="language" role="group" aria-label="Language">{languages}</div></header>
  <main id="top">
    <section class="hero wrap"><p class="tag">OPEN TENNIS GUIDE</p><h1>{q(data['hero'][0])}<br><em>{q(data['hero'][1])}</em></h1><p>{q(data['intro'])}</p><a class="button" href="#guide">{q(data['button'])}</a></section>
    <section id="guide" class="panel"><div class="wrap"><p class="tag">THE GUIDE</p><h2>{q(data['guide'])}</h2><p class="translation-note">{q(data['notice'])}</p><div class="grid">{cards}</div></div></section>
    <section id="cities" class="wrap city"><p class="tag">CITY NOTES</p><h2>{q(data['city_heading'])}</h2><p>{q(data['city_intro'])}</p><div class="city-grid">{cities}</div></section>
  </main>
  <footer><div class="wrap">{q(data['title'])}<a href="{REPO}">{q(data['contribute'])}</a></div></footer>
</body>
</html>
'''


def render_reader(code, data):
    q = lambda value: escape(value, quote=True)
    prefix = '../' if code != 'zh' else ''
    languages = ''.join(
        f'<a href="#" data-reader-lang="{key}" lang="{TEXT[key]["lang"]}">{label}</a>'
        for key, label in [('zh', '中文'), ('en', 'English'), ('ja', '日本語')]
    )
    return f'''<!doctype html>
<html lang="{data['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{q(data['title'])}</title>
  <link rel="icon" type="image/svg+xml" href="{prefix}logo.svg">
  <link rel="stylesheet" href="{prefix}style.css">
</head>
<body data-content-prefix="{prefix}" data-locale="{code}">
  <header class="wrap"><a class="brand" href="index.html"><img src="{prefix}logo.svg" alt="">{q(data['title'])}</a><div class="language" role="group" aria-label="Language">{languages}</div></header>
  <main class="wrap detail"><a href="index.html">← {q(data['back'])}</a><p class="tag">OPEN TENNIS GUIDE</p><h1 id="reader-title">{q(data['title'])}</h1><p class="translation-note">{q(data['notice'])}</p><div id="reader-content" class="article-body" aria-live="polite">{q(data['detail_pending'])}</div></main>
  <footer><div class="wrap">{q(data['title'])}<a href="{REPO}">{q(data['contribute'])}</a></div></footer>
  <script src="{prefix}reader.js" defer></script>
</body>
</html>
'''


for code, data in TEXT.items():
    destination = ROOT / ('' if code == 'zh' else code)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'index.html').write_text(render_home(code, data), encoding='utf-8')
    (destination / 'reader.html').write_text(render_reader(code, data), encoding='utf-8')

content = ROOT / 'content'
if content.exists():
    rmtree(content)
content.mkdir()
for source_dir in ('book', 'cities'):
    copytree(SOURCE / source_dir, content / source_dir)
print('Generated 3 language shells and copied Markdown content')
