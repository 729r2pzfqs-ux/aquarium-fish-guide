#!/usr/bin/env python3
"""Page shell and content helpers for /articles/ pages.

Keeps every article on the same chrome (header, breadcrumb, footer, schema)
as the three that were hand-written, so new ones drop straight in.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import seo_lib as S

SITE = "https://fishfinder.guide"
GA_ID = "G-CWDX74LPLP"
AHREFS_KEY = "9lr6YCArhHF3Ga0FR3XXAA"

FISH = S.load_fish()
FISH_BY_ID = S.by_id(FISH)


# --------------------------------------------------------------------------
# Content helpers
# --------------------------------------------------------------------------

def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def attr(text):
    return text.replace("&", "&amp;").replace('"', "&quot;")


def fish_link(fish_id, label=None):
    """Inline link to a species page, labelled with its name by default."""
    fish = FISH_BY_ID[fish_id]
    return (f'<a href="/fish/{fish_id}/" class="text-cyan-600 font-medium '
            f'hover:underline">{esc(label or fish["name"])}</a>')


def p(text):
    return f'<p class="text-slate-600 mb-4">{text}</p>'


def callout(kind, heading, body):
    """kind: note (cyan) | warn (amber) | stop (red) | win (emerald)"""
    styles = {
        "note": ("bg-cyan-50", "border-cyan-200", "text-cyan-500",
                 "text-cyan-800", "text-cyan-700", "info"),
        "warn": ("bg-amber-50", "border-amber-200", "text-amber-500",
                 "text-amber-800", "text-amber-700", "alert-triangle"),
        "stop": ("bg-red-50", "border-red-200", "text-red-500",
                 "text-red-800", "text-red-700", "x-circle"),
        "win": ("bg-emerald-50", "border-emerald-200", "text-emerald-500",
                "text-emerald-800", "text-emerald-700", "check-circle"),
    }
    bg, border, icon_c, head_c, body_c, icon = styles[kind]
    return f'''<div class="{bg} border {border} rounded-xl p-6 my-6">
                        <div class="flex gap-3">
                            <i data-lucide="{icon}" class="w-6 h-6 {icon_c} flex-shrink-0"></i>
                            <div>
                                <h4 class="font-bold {head_c} mb-1">{esc(heading)}</h4>
                                <p class="{body_c} text-sm">{body}</p>
                            </div>
                        </div>
                    </div>'''


def steps(items):
    """items: list of (heading, body_html)"""
    rows = ""
    for n, (heading, body) in enumerate(items, 1):
        rows += f'''
                        <div class="flex gap-4">
                            <div class="w-10 h-10 bg-cyan-100 rounded-full flex items-center justify-center font-bold text-cyan-600 flex-shrink-0">{n}</div>
                            <div>
                                <h4 class="font-bold text-slate-800">{esc(heading)}</h4>
                                <p class="text-slate-600 mt-1">{body}</p>
                            </div>
                        </div>'''
    return f'<div class="space-y-6 my-8">{rows}\n                    </div>'


def table(headers, rows, note=None):
    head = "".join(
        f'<th class="text-left font-semibold text-slate-700 px-4 py-3">{esc(h)}</th>'
        for h in headers)
    body = ""
    for row in rows:
        cells = "".join(f'<td class="px-4 py-3 text-slate-600 align-top">{c}</td>'
                        for c in row)
        body += f'<tr class="border-t border-slate-100">{cells}</tr>'
    caption = (f'<p class="text-sm text-slate-500 mt-3">{note}</p>' if note else "")
    return f'''<div class="my-8 overflow-x-auto rounded-2xl border border-slate-200">
                        <table class="w-full text-sm bg-white">
                            <thead class="bg-slate-50"><tr>{head}</tr></thead>
                            <tbody>{body}</tbody>
                        </table>
                    </div>{caption}'''


def species_table(fish_ids, note=None, metric=True):
    """Spec table built straight from data/fish.json, every row linked."""
    rows = []
    for fid in fish_ids:
        f = FISH_BY_ID[fid]
        tank = (f'{f["min_tank_gallons"]} gal / {S.litres(f["min_tank_gallons"])} L'
                if metric else f'{f["min_tank_gallons"]} gal')
        size = (f'{S.inches_text(f["size_inches"])} / {S.centimetres(f["size_inches"])} cm'
                if metric else S.inches_text(f["size_inches"]))
        temp = (f'{f["temp_min"]}-{f["temp_max"]}°F / '
                f'{S.celsius(f["temp_min"])}-{S.celsius(f["temp_max"])}°C')
        group = f'{f["school_size"]}+' if f["schooling"] else "—"
        rows.append([fish_link(fid), tank, size, temp,
                     f'pH {f["ph_min"]}-{f["ph_max"]}', group])
    return table(["Species", "Minimum tank", "Adult size", "Temperature",
                  "pH", "Group size"], rows, note)


def cards(items, columns=3):
    """items: list of (emoji, title, body_html, tone)"""
    tones = {
        "red": ("bg-red-50", "text-red-800", "text-red-700"),
        "orange": ("bg-orange-50", "text-orange-800", "text-orange-700"),
        "green": ("bg-green-50", "text-green-800", "text-green-700"),
        "cyan": ("bg-cyan-50", "text-cyan-800", "text-cyan-700"),
        "slate": ("bg-slate-50", "text-slate-800", "text-slate-600"),
    }
    out = ""
    for emoji, title, body, tone in items:
        bg, head_c, body_c = tones[tone]
        out += f'''
                        <div class="{bg} rounded-xl p-5">
                            <div class="text-3xl mb-2">{emoji}</div>
                            <h4 class="font-bold {head_c}">{esc(title)}</h4>
                            <p class="text-sm {body_c} mt-2">{body}</p>
                        </div>'''
    return (f'<div class="grid md:grid-cols-{columns} gap-4 my-8">{out}'
            '\n                    </div>')


def stocking_plan(name, tank, entries, why):
    """A named stocking combination: entries is a list of (count, fish_id)."""
    lines = ""
    for count, fid in entries:
        f = FISH_BY_ID[fid]
        lines += (f'<li class="flex items-start gap-2"><span class="text-cyan-500">•</span>'
                  f'<span><strong class="text-slate-700">{count}×</strong> '
                  f'{fish_link(fid)} <span class="text-slate-500">'
                  f'({S.inches_text(f["size_inches"])})</span></span></li>')
    return f'''<div class="bg-white rounded-2xl border border-slate-200 p-6 my-6">
                        <div class="flex flex-wrap items-baseline justify-between gap-2 mb-4">
                            <h3 class="text-lg font-bold text-slate-900">{esc(name)}</h3>
                            <span class="text-sm text-slate-500">{esc(tank)}</span>
                        </div>
                        <ul class="space-y-2 text-slate-600 mb-4">{lines}</ul>
                        <p class="text-sm text-slate-500">{why}</p>
                    </div>'''


def bullets(items):
    lines = "".join(
        f'<li class="flex items-start gap-2"><span class="text-cyan-500">•</span>'
        f'<span>{item}</span></li>' for item in items)
    return f'<ul class="space-y-2 text-slate-600 my-6">{lines}</ul>'


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------

_HEADER = '''    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
            <a href="/" class="flex items-center gap-2">
                <svg class="w-8 h-8 text-cyan-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6.5 12c.94-3.46 4.94-6 8.5-6 3.56 0 6.06 2.54 7 6-.94 3.46-3.44 6-7 6-3.56 0-7.56-2.54-8.5-6Z"/>
                    <path d="M18 12v.5"/>
                    <path d="M16 10c1 0 2 1 2 2s-1 2-2 2"/>
                    <path d="M2 12h3"/>
                    <path d="M5 12 Q2 8 3 5"/>
                    <path d="M5 12 Q2 16 3 19"/>
                </svg>
                <span class="text-xl font-bold bg-gradient-to-r from-cyan-600 to-teal-600 bg-clip-text text-transparent">FishFinder</span>
            </a>
            <nav class="flex items-center gap-4 text-sm font-medium">
                <a href="/articles/" class="text-slate-600 hover:text-cyan-600 transition">Articles</a>
                <a href="/search/" class="text-slate-600 hover:text-cyan-600 transition hidden sm:block">Browse Fish</a>
                <a href="/quiz/" class="bg-gradient-to-r from-cyan-500 to-teal-600 text-white px-4 py-2 rounded-xl font-semibold hover:shadow-lg transition">Find Your Fish</a>
            </nav>
        </div>
    </header>
'''

_FOOTER = '''    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-12 px-4 mt-16">
        <div class="max-w-6xl mx-auto">
            <div class="flex flex-col md:flex-row items-center justify-between gap-6">
                <div class="flex items-center gap-2">
                    <svg class="w-8 h-8 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M6.5 12c.94-3.46 4.94-6 8.5-6 3.56 0 6.06 2.54 7 6-.94 3.46-3.44 6-7 6-3.56 0-7.56-2.54-8.5-6Z"/>
                        <path d="M18 12v.5"/>
                        <path d="M16 10c1 0 2 1 2 2s-1 2-2 2"/>
                        <path d="M2 12h3"/>
                        <path d="M5 12 Q2 8 3 5"/>
                        <path d="M5 12 Q2 16 3 19"/>
                    </svg>
                    <span class="text-xl font-bold">FishFinder</span>
                </div>
                <div class="flex flex-wrap justify-center gap-x-6 gap-y-2 text-sm text-slate-300">
                    <a href="/quiz/" class="hover:text-white transition">Quiz</a>
                    <a href="/compatibility/" class="hover:text-white transition">Compatibility</a>
                    <a href="/setups/" class="hover:text-white transition">Setups</a>
                    <a href="/articles/" class="hover:text-white transition">Articles</a>
                </div>
            </div>
            <div class="border-t border-slate-800 mt-8 pt-8 text-center text-sm text-slate-300">
                <p>© 2026 FishFinder. Made with 🐠 for fish lovers everywhere. · <a href="/privacy/" class="underline hover:no-underline">Privacy</a></p>
            </div>
        </div>
    </footer>
'''


def _faq_schema(entries):
    questions = ",\n".join(
        f'''        {{
            "@type": "Question",
            "name": {json.dumps(q, ensure_ascii=False)},
            "acceptedAnswer": {{
                "@type": "Answer",
                "text": {json.dumps(a, ensure_ascii=False)}
            }}
        }}''' for q, a in entries)
    return f'''    <script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{questions}
    ]
}}
    </script>'''


def _faq_section(entries):
    items = "\n".join(
        f'''                    <div class="border-b border-slate-100 last:border-0 pb-4 last:pb-0">
                        <h3 class="font-semibold text-slate-900 mb-1">{esc(q)}</h3>
                        <p class="text-slate-600">{esc(a)}</p>
                    </div>''' for q, a in entries)
    return f'''
                <section id="faq" class="mb-12">
                    <h2 class="text-2xl mb-4">Frequently Asked Questions</h2>
                    <div class="space-y-4 mt-6">
{items}
                    </div>
                </section>'''


def render(article, index):
    """Render one article dict to a complete HTML page."""
    slug = article["slug"]
    url = f"{SITE}/articles/{slug}/"
    toc = "\n".join(
        f'                    <li><a href="#{anchor}" class="hover:text-cyan-600 transition">→ {esc(label)}</a></li>'
        for anchor, label in article["toc"])

    sections = ""
    for section in article["sections"]:
        sections += f'''
                <section id="{section['id']}" class="mb-12">
                    <h2 class="text-2xl mb-4">{esc(section['h2'])}</h2>
                    {section['html']}
                </section>'''
    sections += _faq_section(article["faq"])

    cta = article["cta"]
    buttons = ""
    for i, (href, label, icon) in enumerate(cta["buttons"]):
        style = ("bg-white text-cyan-600" if i == 0
                 else "bg-cyan-600 text-white border-2 border-white/30 hover:bg-cyan-700")
        buttons += f'''
                        <a href="{href}" class="inline-flex items-center justify-center gap-2 {style} px-6 py-3 rounded-xl font-semibold hover:shadow-lg transition">
                            <i data-lucide="{icon}" class="w-5 h-5"></i>
                            {esc(label)}
                        </a>'''

    related = ""
    for other_slug in article["related"]:
        other = index[other_slug]
        related += f'''
                <a href="/articles/{other_slug}/" class="bg-white rounded-2xl p-6 border border-slate-100 hover:shadow-lg transition">
                    <span class="text-sm text-cyan-600 font-medium">{esc(other['kicker'])}</span>
                    <h3 class="text-lg font-bold text-slate-800 mt-2">{esc(other['card_title'])}</h3>
                    <p class="text-slate-600 text-sm mt-2">{esc(other['card_blurb'])}</p>
                </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>

    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#06b6d4">

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(article['title'])} | FishFinder</title>
    <meta name="description" content="{attr(article['description'])}">
    <link rel="canonical" href="{url}">

    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{attr(article['h1'])}">
    <meta property="og:description" content="{attr(article['description'])}">
    <meta property="og:site_name" content="FishFinder">

    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{attr(article['card_title'])} | FishFinder">
    <meta name="twitter:description" content="{attr(article['description'])}">

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": {json.dumps(article['h1'], ensure_ascii=False)},
      "description": {json.dumps(article['description'], ensure_ascii=False)},
      "url": "{url}",
      "datePublished": "{article['published']}",
      "dateModified": "{article['modified']}",
      "author": {{
        "@type": "Organization",
        "name": "FishFinder"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "FishFinder",
        "logo": {{
          "@type": "ImageObject",
          "url": "{SITE}/favicon.svg"
        }}
      }}
    }}
    </script>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},
        {{"@type": "ListItem", "position": 2, "name": "Articles", "item": "{SITE}/articles/"}},
        {{"@type": "ListItem", "position": 3, "name": {json.dumps(article['card_title'], ensure_ascii=False)}}}
      ]
    }}
    </script>

{_faq_schema(article['faq'])}

    <link rel="stylesheet" href="/css/tailwind.css">
{S.LUCIDE_TAG}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="alternate" hreflang="en" href="{url}">
    <link rel="alternate" hreflang="x-default" href="{url}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{AHREFS_KEY}" async></script>
</head>
<body class="bg-slate-50 min-h-screen text-slate-800">
{_HEADER}
    <main class="max-w-4xl mx-auto px-4 py-12">
        <!-- Breadcrumb -->
        <nav class="text-sm text-slate-500 mb-8">
            <a href="/" class="hover:text-cyan-600">Home</a>
            <span class="mx-2">›</span>
            <a href="/articles/" class="hover:text-cyan-600">Articles</a>
            <span class="mx-2">›</span>
            <span class="text-slate-700">{esc(article['card_title'])}</span>
        </nav>

        <article class="bg-white rounded-3xl shadow-sm border border-slate-100 p-8 md:p-12">
            <!-- Header -->
            <header class="mb-10">
                <div class="flex items-center gap-2 text-sm text-cyan-600 font-medium mb-4">
                    <i data-lucide="{article['icon']}" class="w-4 h-4"></i>
                    {esc(article['kicker'])}
                </div>
                <h1 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">{esc(article['h1'])}</h1>
                <p class="text-xl text-slate-600">{article['lede']}</p>
                <div class="flex items-center gap-4 mt-6 text-sm text-slate-500">
                    <span>Updated {article['updated_label']}</span>
                    <span>•</span>
                    <span>{article['read_time']}</span>
                </div>
            </header>

            <!-- Table of Contents -->
            <div class="bg-slate-50 rounded-2xl p-6 mb-10">
                <h2 class="font-bold text-slate-800 mb-4">In This Guide</h2>
                <ul class="space-y-2 text-slate-600">
{toc}
                    <li><a href="#faq" class="hover:text-cyan-600 transition">→ Frequently asked questions</a></li>
                </ul>
            </div>

            <!-- Content -->
            <div class="prose prose-lg max-w-none prose-headings:font-bold prose-headings:text-slate-900 prose-a:text-cyan-600 prose-a:no-underline hover:prose-a:underline">
{sections}

                <!-- CTA -->
                <section class="bg-gradient-to-r from-cyan-500 to-teal-600 rounded-2xl p-8 text-center text-white mt-12">
                    <h3 class="text-2xl font-bold mb-3">{esc(cta['heading'])}</h3>
                    <p class="text-cyan-100 mb-6">{esc(cta['text'])}</p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">{buttons}
                    </div>
                </section>

            </div>
        </article>

        <!-- Related Articles -->
        <section class="mt-12">
            <h2 class="text-xl font-bold text-slate-900 mb-6">Related Articles</h2>
            <div class="grid md:grid-cols-2 gap-6">{related}
            </div>
        </section>
    </main>

{_FOOTER}
    <script>
        renderIcons();
    </script>
</body>
</html>'''

    return S.enhance_page(html, fish_index=FISH_BY_ID,
                          image_dims=S.load_image_dims(),
                          css_ver=S.css_version())
