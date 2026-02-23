#!/usr/bin/env python3
"""Generate fish care guide pages from JSON data."""

import json
import os
from pathlib import Path

# Load fish data
with open('data/fish.json', 'r') as f:
    fish_data = json.load(f)

def celsius(f_temp):
    """Convert Fahrenheit to Celsius."""
    return round((f_temp - 32) * 5/9)

def get_care_badge_color(level):
    """Return badge colors for care level."""
    colors = {
        'easy': ('bg-green-100', 'text-green-700'),
        'moderate': ('bg-yellow-100', 'text-yellow-700'),
        'hard': ('bg-red-100', 'text-red-700')
    }
    return colors.get(level.lower(), ('bg-gray-100', 'text-gray-700'))

def get_temperament_badge_color(temperament):
    """Return badge colors for temperament."""
    colors = {
        'peaceful': ('bg-emerald-100', 'text-emerald-700'),
        'semi-aggressive': ('bg-amber-100', 'text-amber-700'),
        'aggressive': ('bg-red-100', 'text-red-700')
    }
    return colors.get(temperament.lower(), ('bg-gray-100', 'text-gray-700'))

def format_compatible_list(items, current_fish_id):
    """Format compatible/avoid list items."""
    html = ''
    for item in items[:5]:  # Limit to 5 items
        # Clean up item name for display
        display_name = item.replace('-', ' ').replace('_', ' ').title()
        html += f'''                        <div class="flex items-center gap-3 p-3 bg-emerald-50 rounded-xl">
                            <span class="text-2xl">🐟</span>
                            <span class="font-medium text-slate-700">{display_name}</span>
                        </div>
'''
    return html

def format_avoid_list(items, current_fish_id):
    """Format avoid list items with warnings."""
    html = ''
    for item in items[:4]:  # Limit to 4 items
        display_name = item.replace('-', ' ').replace('_', ' ').title()
        html += f'''                        <div class="flex items-center gap-3 p-3 bg-red-50 rounded-xl">
                            <span class="text-2xl">⚠️</span>
                            <div>
                                <span class="font-medium text-slate-700 block">{display_name}</span>
                                <span class="text-sm text-red-600">Not compatible</span>
                            </div>
                        </div>
'''
    return html

def generate_html(fish):
    """Generate HTML page for a fish."""
    fish_id = fish['id']
    name = fish['name']
    scientific = fish['scientific']
    category = fish['category'].title()
    
    # Care level badge
    care_bg, care_text = get_care_badge_color(fish['care_level'])
    care_level = fish['care_level'].title()
    
    # Temperament badge
    temp_bg, temp_text = get_temperament_badge_color(fish['temperament'])
    temperament = fish['temperament'].title()
    
    # Temperature conversion
    temp_min_f = fish['temp_min']
    temp_max_f = fish['temp_max']
    temp_min_c = celsius(temp_min_f)
    temp_max_c = celsius(temp_max_f)
    
    # Schooling info
    schooling_badge = ''
    school_section = ''
    if fish['schooling']:
        schooling_badge = '<span class="bg-cyan-100 text-cyan-700 px-3 py-1 rounded-full text-sm font-medium">Schooling</span>'
        school_section = f'''<div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                            <i data-lucide="users" class="w-6 h-6 text-cyan-500"></i>
                            <div>
                                <p class="text-xs text-slate-500">School Size</p>
                                <p class="font-semibold text-slate-700">{fish['school_size']}+ fish</p>
                            </div>
                        </div>'''
    
    # Compatible and avoid lists
    compatible_html = format_compatible_list(fish.get('compatible_with', []), fish_id)
    avoid_html = format_avoid_list(fish.get('avoid_with', []), fish_id)
    
    # Meta description
    meta_desc = f"Complete {name} care guide. Learn about tank size ({fish['min_tank_gallons']} gallons), water parameters ({temp_min_f}-{temp_max_f}°F, pH {fish['ph_min']}-{fish['ph_max']}), compatible tankmates, and expert care tips."
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google Analytics Placeholder -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXXXXX');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} Care Guide | FishFinder</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="https://fishfinder.guide/fish/{fish_id}/">
    <meta property="og:title" content="{name} Care Guide | FishFinder">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://fishfinder.guide/fish/{fish_id}/">
    <meta property="og:type" content="article">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        .rating-bar {{ height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; }}
        .rating-bar::after {{ content: ''; display: block; height: 100%; border-radius: 4px; background: linear-gradient(90deg, #06b6d4, #14b8a6); }}
    </style>

    <!-- Schema.org Fish Markup -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "https://fishfinder.guide/fish/{fish_id}/"
      }},
      "headline": "{name}: Care Guide, Tank Size & Compatibility",
      "description": "{fish['description']}",
      "author": {{
        "@type": "Organization",
        "name": "FishFinder"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "FishFinder",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://fishfinder.guide/favicon.svg"
        }}
      }},
      "about": {{
        "@type": "Animal",
        "name": "{name}",
        "scientificName": "{scientific}",
        "description": "{fish['description']}"
      }}
    }}
    </script>

    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://fishfinder.guide/"}},
        {{"@type": "ListItem", "position": 2, "name": "Fish", "item": "https://fishfinder.guide/search/"}},
        {{"@type": "ListItem", "position": 3, "name": "{name}"}}
      ]
    }}
    </script>
</head>
<body class="bg-slate-50 text-slate-800">
    <nav class="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-4">
            <div class="flex items-center justify-between">
                <a href="/" class="flex items-center gap-2">
                    <svg class="w-7 h-7 text-cyan-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M6.5 12c.94-3.46 4.94-6 8.5-6 3.56 0 6.06 2.54 7 6-.94 3.46-3.44 6-7 6-3.56 0-7.56-2.54-8.5-6Z"/>
                        <path d="M18 12v.5"/>
                        <path d="M16 10c1 0 2 1 2 2s-1 2-2 2"/>
                        <path d="M2 12h3"/>
                    </svg>
                    <span class="font-bold text-xl bg-gradient-to-r from-cyan-600 to-teal-600 bg-clip-text text-transparent">FishFinder</span>
                </a>
                <div class="flex items-center gap-6">
                    <a href="/search/" class="text-slate-600 hover:text-slate-900 font-medium hidden sm:block">Browse Fish</a>
                    <a href="/quiz/" class="text-slate-600 hover:text-slate-900 font-medium hidden sm:block">Quiz</a>
                    <a href="/compatibility/" class="text-slate-600 hover:text-slate-900 font-medium hidden sm:block">Compatibility</a>
                    <a href="/compare/" class="bg-gradient-to-r from-cyan-500 to-teal-600 text-white px-5 py-2.5 rounded-xl font-semibold hover:shadow-lg hover:shadow-cyan-500/25 transition">Compare</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-6xl mx-auto px-4 py-8">
        <!-- Breadcrumb -->
        <nav class="text-sm text-slate-500 mb-6">
            <a href="/" class="hover:text-cyan-600">Home</a>
            <span class="mx-2">/</span>
            <a href="/search/" class="hover:text-cyan-600">Fish</a>
            <span class="mx-2">/</span>
            <span class="text-slate-700">{name}</span>
        </nav>

        <!-- Hero Section -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden mb-8">
            <div class="md:flex">
                <div class="md:w-2/5">
                    <div class="w-full aspect-[4/5] bg-gradient-to-br from-cyan-100 via-teal-100 to-blue-100 flex items-center justify-center border-r border-slate-200 p-6">
                        <img src="/images/fish/{fish_id}.webp" alt="{name}" class="w-full h-full object-contain" onerror="this.onerror=null; this.style.display='none'; this.parentElement.innerHTML='<span class=\\'text-8xl\\'>🐟</span>';">
                    </div>
                </div>
                <div class="md:w-3/5 p-6 md:p-8">
                    <div class="flex flex-wrap gap-2 mb-4">
                        <span class="{temp_bg} {temp_text} px-3 py-1 rounded-full text-sm font-medium">{temperament}</span>
                        <span class="{care_bg} {care_text} px-3 py-1 rounded-full text-sm font-medium">{care_level}</span>
                        {schooling_badge}
                    </div>
                    <h1 class="text-3xl md:text-4xl font-bold text-slate-900 mb-2">{name}</h1>
                    <p class="text-slate-500 italic mb-6">{scientific}</p>
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                            <i data-lucide="box" class="w-6 h-6 text-cyan-500"></i>
                            <div>
                                <p class="text-xs text-slate-500">Minimum Tank</p>
                                <p class="font-semibold text-slate-700">{fish['min_tank_gallons']} Gallons</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                            <i data-lucide="ruler" class="w-6 h-6 text-cyan-500"></i>
                            <div>
                                <p class="text-xs text-slate-500">Adult Size</p>
                                <p class="font-semibold text-slate-700">{fish['size_inches']} inches</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                            <i data-lucide="thermometer" class="w-6 h-6 text-cyan-500"></i>
                            <div>
                                <p class="text-xs text-slate-500">Temperature</p>
                                <p class="font-semibold text-slate-700">{temp_min_f}-{temp_max_f}°F ({temp_min_c}-{temp_max_c}°C)</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                            <i data-lucide="droplet" class="w-6 h-6 text-cyan-500"></i>
                            <div>
                                <p class="text-xs text-slate-500">pH Range</p>
                                <p class="font-semibold text-slate-700">{fish['ph_min']}-{fish['ph_max']}</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                            <i data-lucide="clock" class="w-6 h-6 text-cyan-500"></i>
                            <div>
                                <p class="text-xs text-slate-500">Lifespan</p>
                                <p class="font-semibold text-slate-700">{fish['lifespan_years']} years</p>
                            </div>
                        </div>
                        {school_section}
                    </div>
                </div>
            </div>
        </div>

        <!-- Description -->
        <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
            <h2 class="text-xl font-bold text-slate-900 mb-4">About {name}</h2>
            <div class="prose text-slate-600 leading-relaxed space-y-4">
                <p>{fish['description']}</p>
            </div>
        </section>

        <!-- Care Requirements -->
        <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
            <h2 class="text-xl font-bold text-slate-900 mb-6">Care Requirements</h2>
            <div class="grid md:grid-cols-2 gap-6">
                <div>
                    <h3 class="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <i data-lucide="box" class="w-5 h-5 text-cyan-500"></i>
                        Tank Setup
                    </h3>
                    <ul class="space-y-2 text-slate-600">
                        <li class="flex items-start gap-2">
                            <span class="text-cyan-500">•</span>
                            Minimum {fish['min_tank_gallons']}-gallon tank required
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-cyan-500">•</span>
                            Temperature: {temp_min_f}-{temp_max_f}°F ({temp_min_c}-{temp_max_c}°C)
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-cyan-500">•</span>
                            pH: {fish['ph_min']} - {fish['ph_max']}
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-cyan-500">•</span>
                            Category: {category}
                        </li>
                    </ul>
                </div>
                <div>
                    <h3 class="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <i data-lucide="utensils" class="w-5 h-5 text-cyan-500"></i>
                        Diet & Feeding
                    </h3>
                    <ul class="space-y-2 text-slate-600">
                        <li class="flex items-start gap-2">
                            <span class="text-cyan-500">•</span>
                            Diet type: {fish['diet'].title()}
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-cyan-500">•</span>
                            Feed 1-2 times daily
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-cyan-500">•</span>
                            Varied diet recommended
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- Compatibility -->
        <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
            <h2 class="text-xl font-bold text-slate-900 mb-6">Tank Mate Compatibility</h2>
            
            <div class="grid md:grid-cols-2 gap-6">
                <div>
                    <h3 class="font-semibold text-emerald-700 mb-3 flex items-center gap-2">
                        <i data-lucide="check-circle" class="w-5 h-5"></i>
                        Compatible With
                    </h3>
                    <div class="space-y-2">
{compatible_html}                    </div>
                </div>
                <div>
                    <h3 class="font-semibold text-red-700 mb-3 flex items-center gap-2">
                        <i data-lucide="x-circle" class="w-5 h-5"></i>
                        Avoid Keeping With
                    </h3>
                    <div class="space-y-2">
{avoid_html}                    </div>
                </div>
            </div>
            
            <div class="mt-6 text-center">
                <a href="/compatibility/" class="inline-flex items-center gap-2 text-cyan-600 font-semibold hover:text-cyan-700 transition">
                    Check more combinations with our Compatibility Checker
                    <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </a>
            </div>
        </section>

        <!-- Care Tips -->
        <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
            <h2 class="text-xl font-bold text-slate-900 mb-6">Care Tips</h2>
            <div class="bg-gradient-to-br from-cyan-50 to-teal-50 p-5 rounded-xl border border-cyan-100">
                <h3 class="font-semibold text-cyan-800 mb-2 flex items-center gap-2">
                    <i data-lucide="lightbulb" class="w-5 h-5"></i>
                    Expert Tips
                </h3>
                <p class="text-slate-600">{fish['care_tips']}</p>
            </div>
        </section>

        <!-- Quick Facts -->
        <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
            <h2 class="text-xl font-bold text-slate-900 mb-6">Quick Facts</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="text-center p-4 bg-slate-50 rounded-xl">
                    <p class="text-2xl font-bold text-cyan-600">{fish['min_tank_gallons']}G</p>
                    <p class="text-sm text-slate-500">Min Tank Size</p>
                </div>
                <div class="text-center p-4 bg-slate-50 rounded-xl">
                    <p class="text-2xl font-bold text-cyan-600">{fish['size_inches']}"</p>
                    <p class="text-sm text-slate-500">Adult Size</p>
                </div>
                <div class="text-center p-4 bg-slate-50 rounded-xl">
                    <p class="text-2xl font-bold text-cyan-600">{fish['lifespan_years']}yr</p>
                    <p class="text-sm text-slate-500">Lifespan</p>
                </div>
                <div class="text-center p-4 bg-slate-50 rounded-xl">
                    <p class="text-2xl font-bold text-cyan-600">{fish['school_size'] if fish['schooling'] else '1'}+</p>
                    <p class="text-sm text-slate-500">{'Min School' if fish['schooling'] else 'Can Keep Solo'}</p>
                </div>
            </div>
        </section>

        <!-- CTA -->
        <div class="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-2xl p-8 text-center border border-cyan-100">
            <h2 class="text-2xl font-bold text-slate-900 mb-3">Build Your Perfect Community Tank</h2>
            <p class="text-slate-600 mb-6">Find compatible tankmates for your {name}</p>
            <div class="flex flex-wrap justify-center gap-4">
                <a href="/compatibility/" class="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-teal-600 text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg transition">
                    <i data-lucide="check-circle" class="w-5 h-5"></i>
                    Compatibility Checker
                </a>
                <a href="/compare/?fish1={fish_id}" class="inline-flex items-center gap-2 bg-white text-slate-700 border border-slate-200 px-6 py-3 rounded-xl font-semibold hover:border-slate-300 transition">
                    <i data-lucide="scale" class="w-5 h-5"></i>
                    Compare with Others
                </a>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-12 px-4 mt-16">
        <div class="max-w-6xl mx-auto">
            <div class="flex flex-col md:flex-row items-center justify-between gap-6">
                <div class="flex items-center gap-2">
                    <svg class="w-8 h-8 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M6.5 12c.94-3.46 4.94-6 8.5-6 3.56 0 6.06 2.54 7 6-.94 3.46-3.44 6-7 6-3.56 0-7.56-2.54-8.5-6Z"/>
                        <path d="M18 12v.5"/>
                    </svg>
                    <span class="text-xl font-bold">FishFinder</span>
                </div>
                <div class="flex gap-8 text-sm text-slate-400">
                    <a href="/quiz/" class="hover:text-white transition">Fish Quiz</a>
                    <a href="/compare/" class="hover:text-white transition">Compare</a>
                    <a href="/compatibility/" class="hover:text-white transition">Compatibility</a>
                    <a href="/faq/" class="hover:text-white transition">FAQ</a>
                </div>
            </div>
            <div class="border-t border-slate-800 mt-8 pt-8 text-center text-sm text-slate-500">
                <p>© 2026 FishFinder. Made with 🐠 for fish lovers everywhere.</p>
            </div>
        </div>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>'''
    return html

def generate_sitemap(fish_list):
    """Generate sitemap.xml with all fish URLs."""
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://fishfinder.guide/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://fishfinder.guide/search/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://fishfinder.guide/quiz/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://fishfinder.guide/compatibility/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://fishfinder.guide/compare/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://fishfinder.guide/faq/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
'''
    for fish in fish_list:
        sitemap += f'''  <url>
    <loc>https://fishfinder.guide/fish/{fish['id']}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    sitemap += '</urlset>'
    return sitemap

# Main execution
if __name__ == '__main__':
    base_dir = Path(__file__).parent
    fish_dir = base_dir / 'fish'
    
    # Generate pages for each fish
    generated = 0
    for fish in fish_data:
        fish_id = fish['id']
        page_dir = fish_dir / fish_id
        page_dir.mkdir(parents=True, exist_ok=True)
        
        html = generate_html(fish)
        page_file = page_dir / 'index.html'
        page_file.write_text(html)
        generated += 1
        print(f"✓ Generated: {fish['name']} ({fish_id})")
    
    # Generate sitemap
    sitemap = generate_sitemap(fish_data)
    sitemap_file = base_dir / 'sitemap.xml'
    sitemap_file.write_text(sitemap)
    print(f"\n✓ Generated sitemap.xml with {len(fish_data)} fish URLs")
    
    print(f"\n🎉 Done! Generated {generated} fish pages.")
