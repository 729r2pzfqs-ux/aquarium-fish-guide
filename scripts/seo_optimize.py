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
            table[page.parent.name] = S.page_name(html, page.parent.name)
        names[lang] = table
    return names


def process(path, all_fish, fish_index, image_dims, css_ver=None, locale_names=None):
    original = path.read_text(encoding="utf-8")
    lang, fish_id = classify(path)
    html = S.enhance_page(
        original,
        fish=fish_index.get(fish_id) if fish_id else None,
        all_fish=all_fish,
        lang=lang,
        fish_index=fish_index,
        image_dims=image_dims,
        css_ver=css_ver,
        names=(locale_names or {}).get(lang, {}),
    )
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
