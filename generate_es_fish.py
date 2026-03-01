#!/usr/bin/env python3
"""Generate Spanish fish pages from English ones."""
import os
import re
import shutil

# Directories
EN_FISH_DIR = "fish"
ES_FISH_DIR = "es/peces"

# Create output directory
os.makedirs(ES_FISH_DIR, exist_ok=True)

# Translation patterns (English -> Spanish)
TRANSLATIONS = [
    # Meta/HTML
    (r'lang="en"', 'lang="es"'),
    
    # URLs
    (r'href="/fish/', 'href="/es/peces/'),
    (r'href="/"', 'href="/es/"'),
    (r'href="/search/"', 'href="/es/buscar/"'),
    (r'href="/quiz/"', 'href="/es/test/"'),
    (r'href="/compatibility/"', 'href="/es/compatibilidad/"'),
    (r'href="/setups/"', 'href="/es/configuraciones/"'),
    (r'fishfinder\.guide/fish/', 'fishfinder.guide/es/peces/'),
    
    # Navigation
    (r'>Browse Fish<', '>Explorar Peces<'),
    (r'>Quiz<', '>Test<'),
    (r'>Compatibility<', '>Compatibilidad<'),
    (r'>Find Your Fish<', '>Encuentra Tu Pez<'),
    (r'>Browse Setups<', '>Ver Configuraciones<'),
    (r'>Home<', '>Inicio<'),
    (r'>Fish<', '>Peces<'),
    
    # Care Guide sections
    (r'>Care Guide<', '>Guía de Cuidados<'),
    (r'>Quick Facts<', '>Datos Rápidos<'),
    (r'>Tank Requirements<', '>Requisitos del Tanque<'),
    (r'>Water Parameters<', '>Parámetros del Agua<'),
    (r'>Temperament<', '>Temperamento<'),
    (r'>Diet<', '>Alimentación<'),
    (r'>Feeding<', '>Alimentación<'),
    (r'>Tank Mates<', '>Compañeros de Tanque<'),
    (r'>Compatible Tank Mates<', '>Compañeros Compatibles<'),
    (r'>Avoid<', '>Evitar<'),
    (r'>Best For<', '>Mejor Para<'),
    (r'>Not Ideal For<', '>No Ideal Para<'),
    (r'>Description<', '>Descripción<'),
    (r'>Overview<', '>Resumen<'),
    (r'>Care Level<', '>Nivel de Cuidados<'),
    (r'>Difficulty<', '>Dificultad<'),
    
    # Stats labels
    (r'>Tank Size<', '>Tamaño Tanque<'),
    (r'>Min Tank \((\d+)gal\)<', r'>Tanque Mín (\1gal)<'),
    (r'>Adult Size \(([^)]+)\)<', r'>Tamaño Adulto (\1)<'),
    (r'>Temperature<', '>Temperatura<'),
    (r'>Size<', '>Tamaño<'),
    (r'>Lifespan<', '>Esperanza de Vida<'),
    (r'>pH Range<', '>Rango pH<'),
    (r'>Minimum Tank<', '>Tanque Mínimo<'),
    (r'>Adult Size<', '>Tamaño Adulto<'),
    (r'>School Size<', '>Tamaño Cardumen<'),
    
    # Stats values - convert to metric
    (r'>5 Gallons<', '>19L<'),
    (r'>10 Gallons<', '>38L<'),
    (r'>15 Gallons<', '>57L<'),
    (r'>20 Gallons<', '>75L<'),
    (r'>30 Gallons<', '>114L<'),
    (r'>40 Gallons<', '>151L<'),
    (r'>50 Gallons<', '>189L<'),
    (r'>55 Gallons<', '>208L<'),
    (r'>75 Gallons<', '>284L<'),
    (r'>100 Gallons<', '>379L<'),
    (r'>1 inch<', '>3cm<'),
    (r'>2 inches<', '>5cm<'),
    (r'>3 inches<', '>8cm<'),
    (r'>4 inches<', '>10cm<'),
    (r'>5 inches<', '>13cm<'),
    (r'>6 inches<', '>15cm<'),
    (r'>8 inches<', '>20cm<'),
    (r'>10 inches<', '>25cm<'),
    (r'>12 inches<', '>30cm<'),
    (r'>18 inches<', '>46cm<'),
    (r'>24 inches<', '>61cm<'),
    (r'>(\d+) years<', r'>\1 años<'),
    (r'>(\d+) year<', r'>\1 año<'),
    (r'>5\+ fish<', '>5+ peces<'),
    (r'>6\+ fish<', '>6+ peces<'),
    (r'>8\+ fish<', '>8+ peces<'),
    (r'>10\+ fish<', '>10+ peces<'),
    
    # Temperament values
    (r'>peaceful<', '>pacífico<'),
    (r'>Peaceful<', '>Pacífico<'),
    (r'>semi-aggressive<', '>semi-agresivo<'),
    (r'>Semi-Aggressive<', '>Semi-Agresivo<'),
    (r'>aggressive<', '>agresivo<'),
    (r'>Aggressive<', '>Agresivo<'),
    
    # Care levels
    (r'>Beginner<', '>Principiante<'),
    (r'>beginner<', '>principiante<'),
    (r'>Easy<', '>Fácil<'),
    (r'>easy<', '>fácil<'),
    (r'>Intermediate<', '>Intermedio<'),
    (r'>intermediate<', '>intermedio<'),
    (r'>Moderate<', '>Moderado<'),
    (r'>moderate<', '>moderado<'),
    (r'>Advanced<', '>Avanzado<'),
    (r'>advanced<', '>avanzado<'),
    (r'>Hard<', '>Difícil<'),
    (r'>hard<', '>difícil<'),
    
    # Schooling
    (r'>Schooling<', '>Cardumen<'),
    (r'>schooling<', '>cardumen<'),
    (r'>Solo<', '>Solitario<'),
    (r'>solo<', '>solitario<'),
    (r'>Yes<', '>Sí<'),
    (r'>No<', '>No<'),
    
    # Categories
    (r'>tetra<', '>tetra<'),
    (r'>Tetra<', '>Tetra<'),
    (r'>livebearer<', '>vivíparo<'),
    (r'>Livebearer<', '>Vivíparo<'),
    (r'>catfish<', '>pez gato<'),
    (r'>Catfish<', '>Pez Gato<'),
    (r'>cichlid<', '>cíclido<'),
    (r'>Cichlid<', '>Cíclido<'),
    (r'>shrimp<', '>gamba<'),
    (r'>Shrimp<', '>Gamba<'),
    (r'>snail<', '>caracol<'),
    (r'>Snail<', '>Caracol<'),
    
    # Other labels
    (r'>Compatibility Checker<', '>Verificador de Compatibilidad<'),
    (r'>Can Keep Solo<', '>Puede Estar Solo<'),
    (r'>years<', '>años<'),
    (r'>year<', '>año<'),
    
    # CTA section
    (r'Build Your Perfect Community Tank', 'Crea Tu Tanque Comunitario Perfecto'),
    (r'Find compatible tankmates', 'Encuentra compañeros compatibles'),
    
    # Footer
    (r'Made with', 'Hecho con'),
    (r'for fish lovers everywhere', 'para amantes de los peces'),
]

def translate_content(content):
    """Apply all translations to content."""
    for pattern, replacement in TRANSLATIONS:
        content = re.sub(pattern, replacement, content)
    return content

def process_fish_page(fish_id):
    """Process a single fish page."""
    en_path = os.path.join(EN_FISH_DIR, fish_id, "index.html")
    es_path = os.path.join(ES_FISH_DIR, fish_id, "index.html")
    
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
        f'fishfinder.guide/es/peces/{fish_id}/'
    )
    
    # Add hreflang tags if not present
    if 'hreflang' not in content:
        hreflang = f'''    <link rel="alternate" hreflang="en" href="https://fishfinder.guide/fish/{fish_id}/">
    <link rel="alternate" hreflang="es" href="https://fishfinder.guide/es/peces/{fish_id}/">
'''
        content = content.replace('<link rel="canonical"', hreflang + '    <link rel="canonical"')
    
    # Create directory and write
    os.makedirs(os.path.dirname(es_path), exist_ok=True)
    with open(es_path, 'w', encoding='utf-8') as f:
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
    
    print(f"\nDone! Created {success} Spanish fish pages in {ES_FISH_DIR}/")

if __name__ == "__main__":
    main()
