#!/usr/bin/env python3
"""Apply the SEO/performance fixes from seo_lib to every static page.

Idempotent: running it twice produces no further diff. Run from the repo root:

    python3 scripts/seo_optimize.py            # rewrite in place
    python3 scripts/seo_optimize.py --dry-run  # report only
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import seo_lib as S

ROOT = S.ROOT

# path prefix -> (language, url template)
FISH_DIRS = [
    ("fish", "en"),
    ("de/fische", "de"),
    ("es/peces", "es"),
    ("fr/poissons", "fr"),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__"}

_H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL)
_FAQ_SCHEMA_RE = re.compile(
    r"<!-- FAQ Schema -->\s*<script type=\"application/ld\+json\">.*?</script>",
    re.DOTALL,
)
_FAQ_SECTION_RE = re.compile(
    re.escape(S.FAQ_MARKER) + r".*?</section>", re.DOTALL
)
_TANKMATE_SECTION_RE = re.compile(
    re.escape(S.TANKMATE_MARKER) + r".*?</section>\s*(?=<|$)", re.DOTALL
)
_DESC_RES = [
    re.compile(r'(<meta name="description" content=")[^"]*(")'),
    re.compile(r'(<meta property="og:description" content=")[^"]*(")'),
    re.compile(r'(<meta name="twitter:description" content=")[^"]*(")'),
]


def html_files():
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def classify(path):
    """Return (lang, fish_id) for a fish detail page, else (lang, None)."""
    rel = path.relative_to(ROOT).as_posix()
    for prefix, lang in FISH_DIRS:
        if rel.startswith(prefix + "/") and rel.endswith("/index.html"):
            fish_id = rel[len(prefix) + 1: -len("/index.html")]
            return lang, fish_id
    for prefix, lang in (("de/", "de"), ("es/", "es"), ("fr/", "fr")):
        if rel.startswith(prefix):
            return lang, None
    return "en", None


def local_name(html, fallback):
    match = _H1_RE.search(html)
    if not match:
        return fallback
    name = re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return name or fallback


def attr_escape(text):
    return text.replace("&", "&amp;").replace('"', "&quot;")


def apply_meta(html, fish, lang, name):
    desc = attr_escape(S.meta_description(fish, lang, name))
    for pattern in _DESC_RES:
        html = pattern.sub(lambda m: m.group(1) + desc + m.group(2), html)
    return html


def apply_faq_schema(html, fish, lang, name):
    schema = S.faq_schema(fish, lang, name)
    if _FAQ_SCHEMA_RE.search(html):
        return _FAQ_SCHEMA_RE.sub(lambda m: schema, html, count=1)
    return html.replace("</head>", f"    {schema}\n</head>", 1)


def apply_sections(html, fish, all_fish, lang, name, image_dims, names=None):
    faq = S.faq_section(fish, lang, name)
    mates = S.tankmate_section(fish, all_fish, lang, name, image_dims, names)

    if _FAQ_SECTION_RE.search(html):
        html = _FAQ_SECTION_RE.sub(lambda m: faq, html, count=1)
        new_faq = ""
    else:
        new_faq = faq

    if _TANKMATE_SECTION_RE.search(html):
        html = _TANKMATE_SECTION_RE.sub(lambda m: mates + "\n", html, count=1)
        new_mates = ""
    else:
        new_mates = mates

    additions = "\n".join(block for block in (new_mates, new_faq) if block)
    if additions:
        html = html.replace("</main>", f"{additions}\n</main>", 1)
    return html


def collect_locale_names():
    """fish id -> display name, per language, taken from each page's own <h1>."""
    names = {}
    for prefix, lang in FISH_DIRS:
        table = {}
        base = ROOT / prefix
        if not base.is_dir():
            names[lang] = table
            continue
        for page in base.glob("*/index.html"):
            html = page.read_text(encoding="utf-8")
            table[page.parent.name] = local_name(html, page.parent.name)
        names[lang] = table
    return names


def process(path, all_fish, fish_index, image_dims, css_ver=None, locale_names=None):
    original = path.read_text(encoding="utf-8")
    html = original
    lang, fish_id = classify(path)
    fish = fish_index.get(fish_id) if fish_id else None

    html = S.fix_lucide(html)
    html = S.version_css_link(html, css_ver)
    names = (locale_names or {}).get(lang, {})
    html = S.fix_images(html, fish_index, lang, image_dims,
                        hero_slug=fish_id if fish else None, names=names)

    if fish is not None and "</main>" in html:
        name = local_name(html, fish["name"])
        html = apply_meta(html, fish, lang, name)
        html = apply_faq_schema(html, fish, lang, name)
        html = apply_sections(html, fish, all_fish, lang, name, image_dims, names)

    return original, html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    all_fish = S.load_fish()
    fish_index = S.by_id(all_fish)
    image_dims = S.load_image_dims()
    css_ver = S.css_version()
    locale_names = collect_locale_names()

    changed = 0
    total = 0
    for path in html_files():
        total += 1
        original, html = process(path, all_fish, fish_index, image_dims,
                                 css_ver, locale_names)
        if html != original:
            changed += 1
            if not args.dry_run:
                path.write_text(html, encoding="utf-8")

    verb = "would change" if args.dry_run else "updated"
    print(f"{verb} {changed} of {total} HTML files")


if __name__ == "__main__":
    main()
