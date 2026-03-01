#!/usr/bin/env python3
"""Replace inline language links with a dropdown on all pages."""
import os
import re

# Language dropdown HTML for each language version
DROPDOWN_EN = '''<div class="relative group">
                        <button class="flex items-center gap-1 text-slate-600 hover:text-cyan-600 transition">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                            <span class="font-medium">EN</span>
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                        </button>
                        <div class="absolute right-0 mt-2 w-32 bg-white rounded-lg shadow-lg border border-slate-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                            <a href="/" class="block px-4 py-2 text-sm font-medium text-cyan-600 bg-cyan-50">English</a>
                            <a href="/es/" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50">Español</a>
                            <a href="/de/" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 rounded-b-lg">Deutsch</a>
                        </div>
                    </div>'''

DROPDOWN_ES = '''<div class="relative group">
                        <button class="flex items-center gap-1 text-slate-600 hover:text-cyan-600 transition">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                            <span class="font-medium">ES</span>
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                        </button>
                        <div class="absolute right-0 mt-2 w-32 bg-white rounded-lg shadow-lg border border-slate-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                            <a href="/" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 rounded-t-lg">English</a>
                            <a href="/es/" class="block px-4 py-2 text-sm font-medium text-cyan-600 bg-cyan-50">Español</a>
                            <a href="/de/" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 rounded-b-lg">Deutsch</a>
                        </div>
                    </div>'''

DROPDOWN_DE = '''<div class="relative group">
                        <button class="flex items-center gap-1 text-slate-600 hover:text-cyan-600 transition">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                            <span class="font-medium">DE</span>
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                        </button>
                        <div class="absolute right-0 mt-2 w-32 bg-white rounded-lg shadow-lg border border-slate-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                            <a href="/" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 rounded-t-lg">English</a>
                            <a href="/es/" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50">Español</a>
                            <a href="/de/" class="block px-4 py-2 text-sm font-medium text-cyan-600 bg-cyan-50 rounded-b-lg">Deutsch</a>
                        </div>
                    </div>'''

# Patterns to match existing language switchers (various formats)
PATTERNS = [
    # EN pages: various formats of EN | ES | DE links
    r'<a href="/es/"[^>]*>ES</a>\s*\n?\s*<a href="/de/"[^>]*>DE</a>(\s*\n?\s*<a href="/de/"[^>]*>DE</a>)?',
    r'<span[^>]*>EN</span>\s*\n?\s*<a href="/es/"[^>]*>ES</a>\s*\n?\s*<a href="/de/"[^>]*>DE</a>',
    # ES pages
    r'<a href="/"[^>]*>EN</a>\s*\n?\s*<a href="/de/"[^>]*>DE</a>',
    r'<a href="/"[^>]*>EN</a>\s*\n?\s*<span[^>]*>ES</span>',
    # DE pages  
    r'<a href="/"[^>]*>EN</a>\s*\n?\s*<a href="/es/"[^>]*>ES</a>',
    r'<span[^>]*>DE</span>',
]

def get_lang_from_path(filepath):
    """Determine language from file path."""
    if '/es/' in filepath:
        return 'es'
    elif '/de/' in filepath:
        return 'de'
    return 'en'

def get_dropdown(lang):
    """Get appropriate dropdown for language."""
    if lang == 'es':
        return DROPDOWN_ES
    elif lang == 'de':
        return DROPDOWN_DE
    return DROPDOWN_EN

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    lang = get_lang_from_path(filepath)
    dropdown = get_dropdown(lang)
    
    # Try each pattern
    for pattern in PATTERNS:
        content = re.sub(pattern, dropdown, content, flags=re.MULTILINE)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all HTML files."""
    count = 0
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
                    print(f"✓ Updated: {filepath}")
    
    print(f"\n🎉 Done! Updated {count} files.")

if __name__ == '__main__':
    main()
