#!/usr/bin/env python3
"""Generate German fish pages from English ones."""
import os
import re
import shutil

# Directories
EN_FISH_DIR = "fish"
DE_FISH_DIR = "de/fische"

# Create output directory
os.makedirs(DE_FISH_DIR, exist_ok=True)

# Translation patterns (English -> German)
TRANSLATIONS = [
    # Meta/HTML
    (r'lang="en"', 'lang="de"'),
    
    # Title and meta tags
    (r'Care Guide \| FishFinder', 'Pflegeanleitung | FishFinder'),
    (r'Care Guide, Tank Size & Compatibility', 'Pflegeanleitung, Aquariumgröße & Kompatibilität'),
    
    # URLs
    (r'href="/fish/', 'href="/de/fische/'),
    (r'href="/"', 'href="/de/"'),
    (r'href="/search/"', 'href="/de/suche/"'),
    (r'href="/quiz/"', 'href="/de/quiz/"'),
    (r'href="/compatibility/"', 'href="/de/kompatibilitaet/"'),
    (r'href="/setups/"', 'href="/de/einrichtungen/"'),
    (r'href="/faq/"', 'href="/de/faq/"'),
    (r'href="/articles/"', 'href="/de/artikel/"'),
    (r'href="/about/"', 'href="/de/ueber/"'),
    (r'href="../search/"', 'href="../suche/"'),
    (r'href="../quiz/"', 'href="../quiz/"'),
    (r'href="../compatibility/"', 'href="../kompatibilitaet/"'),
    (r'fishfinder\.guide/fish/', 'fishfinder.guide/de/fische/'),
    
    # Navigation
    (r'>Browse Fish<', '>Fische durchsuchen<'),
    (r'>Browse<', '>Durchsuchen<'),
    (r'>Quiz<', '>Quiz<'),
    (r'>Compatibility<', '>Kompatibilität<'),
    (r'>Find Your Fish<', '>Finde deinen Fisch<'),
    (r'>Browse Setups<', '>Einrichtungen ansehen<'),
    (r'>Home<', '>Startseite<'),
    (r'>Fish<', '>Fische<'),
    (r'>Articles<', '>Artikel<'),
    
    # Care Guide sections
    (r'>Care Guide<', '>Pflegeanleitung<'),
    (r'>Quick Facts<', '>Schnelle Fakten<'),
    (r'>Tank Requirements<', '>Aquariumanforderungen<'),
    (r'>Water Parameters<', '>Wasserwerte<'),
    (r'>Temperament<', '>Temperament<'),
    (r'>Diet<', '>Ernährung<'),
    (r'>Feeding<', '>Fütterung<'),
    (r'>Tank Mates<', '>Mitbewohner<'),
    (r'>Compatible Tank Mates<', '>Verträgliche Mitbewohner<'),
    (r'>Avoid<', '>Vermeiden<'),
    (r'>Best For<', '>Geeignet für<'),
    (r'>Not Ideal For<', '>Nicht geeignet für<'),
    (r'>Description<', '>Beschreibung<'),
    (r'>Overview<', '>Überblick<'),
    (r'>Care Level<', '>Pflegestufe<'),
    (r'>Difficulty<', '>Schwierigkeit<'),
    (r'>Breeding<', '>Zucht<'),
    (r'>Behavior<', '>Verhalten<'),
    (r'>Habitat<', '>Lebensraum<'),
    (r'>Origin<', '>Herkunft<'),
    (r'>Natural Habitat<', '>Natürlicher Lebensraum<'),
    
    # Stats labels
    (r'>Tank Size<', '>Aquariumgröße<'),
    (r'>Min Tank \((\d+)gal\)<', r'>Min. Aquarium (\1gal)<'),
    (r'>Adult Size \(([^)]+)\)<', r'>Erwachsenengröße (\1)<'),
    (r'>Minimum Tank<', '>Mindestaquarium<'),
    (r'>Temperature<', '>Temperatur<'),
    (r'>Size<', '>Größe<'),
    (r'>Adult Size<', '>Erwachsenengröße<'),
    (r'>Lifespan<', '>Lebenserwartung<'),
    (r'>pH Range<', '>pH-Bereich<'),
    (r'>Hardness<', '>Härte<'),
    (r'>Max Size<', '>Max. Größe<'),
    
    # Temperament values
    (r'>peaceful<', '>friedlich<'),
    (r'>Peaceful<', '>Friedlich<'),
    (r'>semi-aggressive<', '>semi-aggressiv<'),
    (r'>Semi-Aggressive<', '>Semi-Aggressiv<'),
    (r'>Semi-aggressive<', '>Semi-aggressiv<'),
    (r'>aggressive<', '>aggressiv<'),
    (r'>Aggressive<', '>Aggressiv<'),
    
    # Care levels
    (r'>Beginner<', '>Anfänger<'),
    (r'>beginner<', '>anfänger<'),
    (r'>Easy<', '>Einfach<'),
    (r'>easy<', '>einfach<'),
    (r'>Intermediate<', '>Fortgeschritten<'),
    (r'>intermediate<', '>fortgeschritten<'),
    (r'>Moderate<', '>Mittel<'),
    (r'>moderate<', '>mittel<'),
    (r'>Advanced<', '>Experte<'),
    (r'>advanced<', '>experte<'),
    (r'>Hard<', '>Schwer<'),
    (r'>hard<', '>schwer<'),
    
    # Schooling
    (r'>Schooling<', '>Schwarmfisch<'),
    (r'>schooling<', '>schwarmfisch<'),
    (r'>School Size<', '>Schwarmgröße<'),
    (r'>Solo<', '>Einzelhaltung<'),
    (r'>solo<', '>einzelhaltung<'),
    (r'>Yes<', '>Ja<'),
    (r'>No<', '>Nein<'),
    (r'>Can Keep Solo<', '>Einzelhaltung möglich<'),
    
    # Categories
    (r'>tetra<', '>salmler<'),
    (r'>Tetra<', '>Salmler<'),
    (r'>livebearer<', '>lebendgebärend<'),
    (r'>Livebearer<', '>Lebendgebärend<'),
    (r'>catfish<', '>wels<'),
    (r'>Catfish<', '>Wels<'),
    (r'>cichlid<', '>buntbarsch<'),
    (r'>Cichlid<', '>Buntbarsch<'),
    (r'>shrimp<', '>garnele<'),
    (r'>Shrimp<', '>Garnele<'),
    (r'>snail<', '>schnecke<'),
    (r'>Snail<', '>Schnecke<'),
    (r'>loach<', '>schmerle<'),
    (r'>Loach<', '>Schmerle<'),
    (r'>barb<', '>barbe<'),
    (r'>Barb<', '>Barbe<'),
    (r'>gourami<', '>gurami<'),
    (r'>Gourami<', '>Gurami<'),
    (r'>rasbora<', '>rasbora<'),
    (r'>Rasbora<', '>Rasbora<'),
    (r'>danio<', '>bärbling<'),
    (r'>Danio<', '>Bärbling<'),
    (r'>pleco<', '>wels<'),
    (r'>Pleco<', '>Wels<'),
    (r'>killifish<', '>killifisch<'),
    (r'>Killifish<', '>Killifisch<'),
    (r'>rainbow<', '>regenbogenfisch<'),
    (r'>Rainbow<', '>Regenbogenfisch<'),
    
    # Diet types
    (r'>Omnivore<', '>Allesfresser<'),
    (r'>omnivore<', '>allesfresser<'),
    (r'>Carnivore<', '>Fleischfresser<'),
    (r'>carnivore<', '>fleischfresser<'),
    (r'>Herbivore<', '>Pflanzenfresser<'),
    (r'>herbivore<', '>pflanzenfresser<'),
    (r'>Insectivore<', '>Insektenfresser<'),
    (r'>Algae Eater<', '>Algenfresser<'),
    (r'>Filter Feeder<', '>Filtrierer<'),
    
    # Other labels
    (r'>Compatibility Checker<', '>Kompatibilitätsprüfer<'),
    (r'>years<', '>Jahre<'),
    (r'>year<', '>Jahr<'),
    (r'(\d+) years', r'\1 Jahre'),
    (r'(\d+)yr<', r'\1J<'),
    (r'Temperature:', 'Temperatur:'),
    (r'Compatible With', 'Kompatibel mit'),
    (r'Avoid Keeping With', 'Nicht zusammen halten mit'),
    (r'Avoid Keeping', 'Nicht zusammen halten'),
    (r'>months<', '>Monate<'),
    (r'>inches<', '>Zoll<'),
    (r'>gallons<', '>Gallonen<'),
    
    # Best For phrases
    (r'Best for beginners', 'Ideal für Anfänger'),
    (r'Best for community tanks', 'Ideal für Gesellschaftsaquarien'),
    (r'Best for planted tanks', 'Ideal für Pflanzenaquarien'),
    (r'Great for beginners', 'Toll für Anfänger'),
    (r'Perfect for beginners', 'Perfekt für Anfänger'),
    (r'Ideal for beginners', 'Ideal für Anfänger'),
    (r'Easy to care for', 'Leicht zu pflegen'),
    (r'Hardy and resilient', 'Robust und widerstandsfähig'),
    (r'Low maintenance', 'Pflegeleicht'),
    (r'Peaceful community fish', 'Friedlicher Gesellschaftsfisch'),
    (r'Great cleanup crew', 'Tolles Aufräumteam'),
    (r'Algae eater', 'Algenfresser'),
    (r'Active swimmer', 'Aktiver Schwimmer'),
    (r'Colorful and vibrant', 'Farbenfroh und lebhaft'),
    (r'Beautiful fins', 'Schöne Flossen'),
    (r'Unique appearance', 'Einzigartiges Aussehen'),
    (r'Interesting behavior', 'Interessantes Verhalten'),
    
    # Not Ideal For phrases
    (r'Not for beginners', 'Nicht für Anfänger'),
    (r'Not ideal for beginners', 'Nicht ideal für Anfänger'),
    (r'Needs experienced keeper', 'Erfordert erfahrenen Halter'),
    (r'Requires large tank', 'Benötigt großes Aquarium'),
    (r'May eat small fish', 'Kann kleine Fische fressen'),
    (r'Can be aggressive', 'Kann aggressiv sein'),
    (r'Fin nipper', 'Flossenbeißer'),
    (r'Sensitive to water quality', 'Empfindlich bei Wasserqualität'),
    (r'Needs soft water', 'Benötigt weiches Wasser'),
    (r'Needs specific pH', 'Benötigt spezifischen pH-Wert'),
    
    # Section headings
    (r'>Tank Mate Compatibility<', '>Mitbewohner-Kompatibilität<'),
    (r'>Care Requirements<', '>Pflegeanforderungen<'),
    (r'>Care Tips<', '>Pflegetipps<'),
    (r'>Fish Quiz<', '>Fisch-Quiz<'),
    
    # Tank mates examples
    (r'>Larger Tetras<', '>Größere Salmler<'),
    (r'>Small Tetras<', '>Kleine Salmler<'),
    (r'>Small Fish<', '>Kleine Fische<'),
    (r'>Large Fish<', '>Große Fische<'),
    (r'>Fin Nippers<', '>Flossenbeißer<'),
    (r'>Aggressive Cichlids<', '>Aggressive Buntbarsche<'),
    (r'>Peaceful Catfish<', '>Friedliche Welse<'),
    (r'>Bottom Dwellers<', '>Bodenbewohner<'),
    (r'>Corydoras<', '>Panzerwelse<'),
    (r'>Plecos<', '>Saugwelse<'),
    (r'>Livebearers<', '>Lebendgebärende<'),
    (r'>Other Gouramis<', '>Andere Guramis<'),
    (r'>Gouramis<', '>Guramis<'),
    (r'>Compare<', '>Vergleichen<'),
    (r'>Not compatible<', '>Nicht kompatibel<'),
    (r'>Compatible<', '>Kompatibel<'),
    (r'>FAQ<', '>FAQ<'),
    (r'>Shrimp<', '>Garnelen<'),
    (r'>Snails<', '>Schnecken<'),
    (r'>Dwarf Shrimp<', '>Zwerggarnelen<'),
    (r'>Min School<', '>Min. Schwarm<'),
    (r'Check more combinations with our Compatibility Checker', 'Prüfe weitere Kombinationen mit unserem Kompatibilitätsprüfer'),
    (r'Find compatible tankmates for your', 'Finde verträgliche Mitbewohner für deinen'),
    
    # CTA section
    (r'Build Your Perfect Community Tank', 'Erstelle dein perfektes Gesellschaftsaquarium'),
    (r'Find compatible tankmates', 'Finde verträgliche Mitbewohner'),
    (r'Check compatibility', 'Kompatibilität prüfen'),
    (r'Take the quiz', 'Mach das Quiz'),
    (r'Find your fish', 'Finde deinen Fisch'),
    (r'Find Your Perfect Fish', 'Finde deinen perfekten Fisch'),
    (r'Browse all fish', 'Alle Fische durchsuchen'),
    (r'View all fish', 'Alle Fische ansehen'),
    
    # Footer
    (r'Made with', 'Erstellt mit'),
    (r'for fish lovers everywhere', 'für Fischliebhaber überall'),
    (r'for fish lovers', 'für Fischliebhaber'),
    
    # Common phrases
    (r'fish found', 'Fische gefunden'),
    (r'No fish found', 'Keine Fische gefunden'),
    (r'Loading', 'Laden'),
    (r'Search', 'Suchen'),
    (r'Filter', 'Filtern'),
    (r'Sort by', 'Sortieren nach'),
    (r'Clear all', 'Alle löschen'),
    (r'Reset', 'Zurücksetzen'),
    (r'Apply', 'Anwenden'),
    (r'Show more', 'Mehr anzeigen'),
    (r'Show less', 'Weniger anzeigen'),
    (r'Read more', 'Mehr lesen'),
    (r'Learn more', 'Mehr erfahren'),
    (r'View details', 'Details ansehen'),
    
    # Language switcher - update to show DE as active
    (r'<span class="font-bold text-cyan-600">EN</span>', '<a href="/" class="text-slate-500 hover:text-cyan-600 transition">EN</a>'),
    (r'<a href="/es/" class="text-slate-500 hover:text-cyan-600 transition">ES</a>', '<span class="font-bold text-cyan-600">DE</span>'),
]

def translate_content(content):
    """Apply all translations to content."""
    for pattern, replacement in TRANSLATIONS:
        content = re.sub(pattern, replacement, content)
    return content

def process_fish_page(fish_id):
    """Process a single fish page."""
    en_path = os.path.join(EN_FISH_DIR, fish_id, "index.html")
    de_path = os.path.join(DE_FISH_DIR, fish_id, "index.html")
    
    if not os.path.exists(en_path):
        print(f"  Skipping {fish_id} - no English page")
        return False
    
    # Read English content
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Translate
    content = translate_content(content)
    
    # Update canonical URL
    content = content.replace(
        f'fishfinder.guide/fish/{fish_id}/',
        f'fishfinder.guide/de/fische/{fish_id}/'
    )
    
    # Add/update hreflang tags
    if 'hreflang' not in content:
        hreflang = f'''    <link rel="alternate" hreflang="en" href="https://fishfinder.guide/fish/{fish_id}/">
    <link rel="alternate" hreflang="es" href="https://fishfinder.guide/es/peces/{fish_id}/">
    <link rel="alternate" hreflang="de" href="https://fishfinder.guide/de/fische/{fish_id}/">
'''
        content = content.replace('<link rel="canonical"', hreflang + '    <link rel="canonical"')
    else:
        # Add German hreflang if missing
        if 'hreflang="de"' not in content:
            content = content.replace(
                f'<link rel="alternate" hreflang="es" href="https://fishfinder.guide/es/peces/{fish_id}/">',
                f'''<link rel="alternate" hreflang="es" href="https://fishfinder.guide/es/peces/{fish_id}/">
    <link rel="alternate" hreflang="de" href="https://fishfinder.guide/de/fische/{fish_id}/">'''
            )
    
    # Create directory and write
    os.makedirs(os.path.dirname(de_path), exist_ok=True)
    with open(de_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Process all fish pages."""
    # Get list of fish from English directory
    fish_ids = [d for d in os.listdir(EN_FISH_DIR) 
                if os.path.isdir(os.path.join(EN_FISH_DIR, d))]
    
    print(f"Found {len(fish_ids)} fish to process")
    
    success = 0
    for fish_id in sorted(fish_ids):
        if process_fish_page(fish_id):
            success += 1
    
    print(f"\nDone! Created {success} German fish pages in {DE_FISH_DIR}/")

if __name__ == "__main__":
    main()
