#!/usr/bin/env python3
"""Update fish pages to use verified correct images only"""

import os
import re

BASE_DIR = os.path.expanduser("~/clawd/aquarium-fish")
FISH_DIR = os.path.join(BASE_DIR, "fish")

# Verified correct images only
VERIFIED_IMAGES = {
    "neon-tetra",
    "betta-fish",
    "discus",
    "angelfish",
    "cherry-shrimp",
    "mystery-snail",
    "pleco-bristlenose",
}

def update_fish_page(fish_id):
    """Update a single fish page with correct image"""
    page_path = os.path.join(FISH_DIR, fish_id, "index.html")
    
    if not os.path.exists(page_path):
        return False, "not found"
    
    with open(page_path, 'r') as f:
        content = f.read()
    
    # Extract fish name from title
    name_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    fish_name = name_match.group(1).strip() if name_match else fish_id.replace('-', ' ').title()
    
    if fish_id in VERIFIED_IMAGES:
        new_image_div = f'''<div class="md:w-2/5">
                    <!-- Real image -->
                    <div class="w-full aspect-[4/5] bg-slate-100 relative overflow-hidden border-r border-slate-200">
                        <img src="/images/fish/{fish_id}.png" 
                             alt="{fish_name}" 
                             class="w-full h-full object-cover"
                             loading="lazy">
                    </div>
                </div>'''
    else:
        new_image_div = f'''<div class="md:w-2/5">
                    <!-- Image placeholder -->
                    <div class="w-full aspect-[4/5] bg-gradient-to-br from-cyan-100 via-teal-100 to-blue-100 flex items-center justify-center border-r border-slate-200">
                        <div class="text-center">
                            <span class="text-8xl block mb-4">🐟</span>
                            <span class="text-slate-400 text-sm">Image coming soon</span>
                        </div>
                    </div>
                </div>'''
    
    # Pattern to match the entire md:w-2/5 div
    pattern = r'<div class="md:w-2/5">.*?</div>\s*</div>\s*</div>(\s*<div class="md:w-3/5)'
    
    def replacer(match):
        return new_image_div + match.group(1)
    
    new_content, count = re.subn(pattern, replacer, content, count=1, flags=re.DOTALL)
    
    if count > 0:
        with open(page_path, 'w') as f:
            f.write(new_content)
        return True, "updated"
    
    return False, "pattern not found"

def main():
    print("🐠 Updating fish pages with verified images...")
    print(f"📷 Verified images: {len(VERIFIED_IMAGES)}")
    print()
    
    updated = 0
    errors = []
    
    fish_dirs = sorted([d for d in os.listdir(FISH_DIR) 
                        if os.path.isdir(os.path.join(FISH_DIR, d))])
    
    for fish_id in fish_dirs:
        success, status = update_fish_page(fish_id)
        if success:
            has_image = "✅" if fish_id in VERIFIED_IMAGES else "⬜"
            print(f"{has_image} {fish_id}")
            updated += 1
        else:
            print(f"❌ {fish_id}: {status}")
            errors.append(fish_id)
    
    print()
    print(f"{'='*50}")
    print(f"✅ Updated: {updated}")
    print(f"📷 With real images: {len([f for f in fish_dirs if f in VERIFIED_IMAGES])}")
    print(f"⬜ With placeholders: {updated - len([f for f in fish_dirs if f in VERIFIED_IMAGES])}")

if __name__ == "__main__":
    main()
