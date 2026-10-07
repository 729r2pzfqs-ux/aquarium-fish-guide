#!/usr/bin/env python3
"""Fix schema.org Article markup: add datePublished and dateModified to fish species pages."""

import os
import re
import sys

# Directories to scan for fish species pages
FISH_DIRS = [
    "fish",
    "de/fische",
    "es/peces",
    "fr/poissons",
]

# Also check article directories (though they may already have dates)
ARTICLE_DIRS = [
    "articles",
    "de/artikel",
    "es/articulos",
]

DATE_PUBLISHED = "2025-09-19"
DATE_MODIFIED = "2026-10-07"

# Pattern: match the "image": "https://fishfinder.guide/images/fish/....webp", line
# and insert datePublished/dateModified after it
IMAGE_LINE_PATTERN = re.compile(
    r'("image": "https://fishfinder\.guide/images/fish/[^"]+\.webp",)\n'
)

# Pattern to check if dates already exist
ALREADY_HAS_DATES = re.compile(r'"datePublished"')


def fix_file(filepath):
    """Add datePublished and dateModified after the image line in Article schema."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has datePublished
    if ALREADY_HAS_DATES.search(content):
        return False

    # Skip if no Article schema
    if '"@type": "Article"' not in content:
        return False

    # Find the image line and add dates after it
    def replacer(match):
        image_line = match.group(1)
        # Detect indentation from the image line
        indent = "      "  # default 6 spaces
        return (
            f'{image_line}\n'
            f'{indent}"datePublished": "{DATE_PUBLISHED}",\n'
            f'{indent}"dateModified": "{DATE_MODIFIED}",\n'
        )

    new_content = IMAGE_LINE_PATTERN.sub(replacer, content)

    if new_content == content:
        # Image pattern didn't match - try a more general approach for articles
        # Match any "image": "...", line within an Article schema block
        general_pattern = re.compile(
            r'("image": "[^"]+",)\n'
        )
        new_content = general_pattern.sub(replacer, content)

    if new_content == content:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_dirs = FISH_DIRS + ARTICLE_DIRS
    modified_count = 0
    skipped_count = 0
    error_count = 0

    for dir_name in all_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if not os.path.isdir(dir_path):
            print(f"Directory not found: {dir_path}")
            continue

        for root, dirs, files in os.walk(dir_path):
            # Skip __bad and __corrupted_rename directories
            dirs[:] = [d for d in dirs if not d.endswith('__bad') and not d.endswith('__corrupted_rename')]

            for fname in files:
                if fname != 'index.html':
                    continue
                filepath = os.path.join(root, fname)
                try:
                    if fix_file(filepath):
                        modified_count += 1
                    else:
                        skipped_count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}", file=sys.stderr)
                    error_count += 1

    print(f"\nResults:")
    print(f"  Modified: {modified_count}")
    print(f"  Skipped (already had dates or no Article schema): {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total files checked: {modified_count + skipped_count + error_count}")


if __name__ == '__main__':
    main()
