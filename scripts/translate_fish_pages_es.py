#!/usr/bin/env python3
"""
Translate Spanish fish pages - replace English strings with Spanish
"""

import os
import re
import json

# Load fish data
fish_data_path = os.path.expanduser("~/clawd/aquarium-fish/data/fish.json")
with open(fish_data_path, 'r') as f:
    fish_list = json.load(f)

# Fish name translations (from fish-es.js)
fish_names_es = {
    "neon-tetra": "Tetra Neón",
    "betta-fish": "Pez Betta",
    "guppy": "Guppy",
    "corydoras-catfish": "Corydora",
    "angelfish": "Pez Ángel",
    "platy": "Platy",
    "molly": "Molly",
    "cherry-barb": "Barbo Cereza",
    "zebra-danio": "Danio Cebra",
    "dwarf-gourami": "Gurami Enano",
    "pleco-bristlenose": "Pleco Bristlenose",
    "cardinal-tetra": "Tetra Cardenal",
    "harlequin-rasbora": "Rasbora Arlequín",
    "german-blue-ram": "Cíclido Ramirezi",
    "kuhli-loach": "Locha Kuhli",
    "black-skirt-tetra": "Tetra Falda Negra",
    "rummy-nose-tetra": "Tetra Nariz Roja",
    "emperor-tetra": "Tetra Emperador",
    "congo-tetra": "Tetra Congo",
    "serpae-tetra": "Tetra Serpae",
    "glowlight-tetra": "Tetra Luminoso",
    "diamond-tetra": "Tetra Diamante",
    "flame-tetra": "Tetra Llama",
    "black-phantom-tetra": "Tetra Fantasma Negro",
    "lemon-tetra": "Tetra Limón",
    "bleeding-heart-tetra": "Tetra Corazón Sangrante",
    "buenos-aires-tetra": "Tetra Buenos Aires",
    "silvertip-tetra": "Tetra Punta Plateada",
    "red-eye-tetra": "Tetra Ojo Rojo",
    "x-ray-tetra": "Tetra Rayos X",
    "penguin-tetra": "Tetra Pingüino",
    "swordtail": "Pez Espada",
    "endler-livebearer": "Endler",
    "sailfin-molly": "Molly Vela",
    "balloon-molly": "Molly Globo",
    "otocinclus": "Otocinclus",
    "pictus-catfish": "Pez Gato Pictus",
    "glass-catfish": "Pez Gato de Cristal",
    "upside-down-catfish": "Pez Gato Invertido",
    "panda-cory": "Corydora Panda",
    "bronze-cory": "Corydora Bronce",
    "peppered-cory": "Corydora Pimienta",
    "sterbai-cory": "Corydora Sterbai",
    "pygmy-cory": "Corydora Pigmea",
    "julii-cory": "Corydora Julii",
    "discus": "Disco",
    "apistogramma-cacatuoides": "Cíclido Cacatúa",
    "apistogramma-borellii": "Apistogramma Borellii",
    "kribensis": "Kribensis",
    "oscar": "Óscar",
    "convict-cichlid": "Cíclido Convicto",
    "jack-dempsey": "Jack Dempsey",
    "electric-blue-acara": "Acara Azul Eléctrico",
    "firemouth-cichlid": "Cíclido Boca de Fuego",
    "severum": "Severum",
    "yellow-lab": "Labidochromis Amarillo",
    "peacock-cichlid": "Cíclido Pavo Real",
    "jewel-cichlid": "Cíclido Joya",
    "tiger-barb": "Barbo Tigre",
    "rosy-barb": "Barbo Rosado",
    "gold-barb": "Barbo Dorado",
    "denison-barb": "Barbo Denison",
    "odessa-barb": "Barbo Odessa",
    "checker-barb": "Barbo Ajedrez",
    "chili-rasbora": "Rasbora Chile",
    "celestial-pearl-danio": "Danio Perla Celestial",
    "emerald-eye-rasbora": "Rasbora Ojo Esmeralda",
    "scissortail-rasbora": "Rasbora Cola de Tijera",
    "lambchop-rasbora": "Rasbora Lambchop",
    "phoenix-rasbora": "Rasbora Fénix",
    "clown-loach": "Locha Payaso",
    "yoyo-loach": "Locha Yoyo",
    "hillstream-loach": "Locha de Torrente",
    "dojo-loach": "Locha Dojo",
    "zebra-loach": "Locha Cebra",
    "dwarf-chain-loach": "Locha Cadena Enana",
    "pearl-gourami": "Gurami Perla",
    "honey-gourami": "Gurami Miel",
    "moonlight-gourami": "Gurami Luz de Luna",
    "blue-gourami": "Gurami Azul",
    "kissing-gourami": "Gurami Besador",
    "sparkling-gourami": "Gurami Brillante",
    "paradise-fish": "Pez Paraíso",
    "cherry-shrimp": "Gamba Cereza",
    "amano-shrimp": "Gamba Amano",
    "ghost-shrimp": "Gamba Fantasma",
    "crystal-red-shrimp": "Gamba Cristal Roja",
    "blue-velvet-shrimp": "Gamba Terciopelo Azul",
    "bamboo-shrimp": "Gamba Bambú",
    "nerite-snail": "Caracol Nerita",
    "mystery-snail": "Caracol Misterio",
    "ramshorn-snail": "Caracol Cuerno de Carnero",
    "assassin-snail": "Caracol Asesino",
    "malaysian-trumpet-snail": "Caracol Trompeta Malayo",
    "rabbit-snail": "Caracol Conejo",
    "clown-killifish": "Killifish Payaso",
    "golden-wonder-killifish": "Killifish Dorado",
    "blue-notho": "Nothobranchius Azul",
    "least-killifish": "Killifish Mínimo",
    "boesemani-rainbow": "Arcoíris Boesemani",
    "neon-dwarf-rainbow": "Arcoíris Enano Neón",
    "turquoise-rainbow": "Arcoíris Turquesa",
    "madagascar-rainbow": "Arcoíris de Madagascar",
    "red-irian-rainbow": "Arcoíris Rojo de Irian",
    "celebes-rainbow": "Arcoíris de Célebes",
    "forktail-rainbow": "Arcoíris Cola Bifurcada",
    "gertrudae-rainbow": "Arcoíris Gertrudae",
    "white-cloud-mountain-minnow": "Neón Chino",
    "leopard-danio": "Danio Leopardo",
    "pearl-danio": "Danio Perla",
    "giant-danio": "Danio Gigante",
    "longfin-zebra-danio": "Danio Cebra Aleta Larga",
    "gold-ring-danio": "Danio Anillo Dorado",
    "siamese-algae-eater": "Comealgas Siamés",
    "flying-fox": "Zorro Volador",
    "red-tailed-shark": "Tiburón Cola Roja",
    "rainbow-shark": "Tiburón Arcoíris",
    "common-pleco": "Pleco Común",
    "rubber-lip-pleco": "Pleco Labio de Goma",
    "clown-pleco": "Pleco Payaso",
    "royal-pleco": "Pleco Real",
    "bala-shark": "Tiburón Bala",
    "tinfoil-barb": "Barbo Papel de Estaño",
    "ember-tetra": "Tetra Ember"
}

# Category translations
category_es = {
    "tetra": "Tetra",
    "livebearer": "Vivíparo", 
    "catfish": "Pez Gato",
    "cichlid": "Cíclido",
    "barb": "Barbo",
    "rasbora": "Rasbora",
    "loach": "Locha",
    "labyrinth": "Laberinto",
    "shrimp": "Gamba",
    "snail": "Caracol",
    "killifish": "Killifish",
    "rainbowfish": "Arcoíris",
    "danio": "Danio"
}

# Diet translations
diet_es = {
    "omnivore": "Omnívoro",
    "carnivore": "Carnívoro",
    "herbivore": "Herbívoro"
}

# Temperament translations
temperament_es = {
    "peaceful": "Pacífico",
    "semi-aggressive": "Semi-Agresivo",
    "aggressive": "Agresivo"
}

# Care level translations
care_es = {
    "easy": "Fácil",
    "moderate": "Moderado",
    "hard": "Difícil"
}

# String replacements (English -> Spanish)
replacements = [
    # Title and meta
    (r'Care Guide \| FishFinder', 'Guía de Cuidados | FishFinder'),
    (r'Complete (.+?) care guide\.', r'Guía completa de cuidados para \1.'),
    (r'Learn about tank size', 'Aprende sobre el tamaño del tanque'),
    (r'water parameters', 'parámetros del agua'),
    (r'compatible tankmates', 'compañeros de tanque compatibles'),
    (r'and expert care tips', 'y consejos de cuidados expertos'),
    
    # Schema
    (r'"headline": "(.+?): Care Guide, Tank Size & Compatibility"', r'"headline": "\1: Guía de Cuidados, Tamaño de Tanque y Compatibilidad"'),
    (r'"name": "Home"', '"name": "Inicio"'),
    (r'"name": "Fish"', '"name": "Peces"'),
    
    # Navigation
    (r'>Setups<', '>Configuraciones<'),
    (r'>Fish Quiz<', '>Test de Peces<'),
    (r'>FAQ<', '>Preguntas Frecuentes<'),
    
    # Section headers
    (r'>About (.+?)<', r'>Sobre \1<'),
    (r'>Care Requirements<', '>Requisitos de Cuidados<'),
    (r'>Tank Setup<', '>Configuración del Tanque<'),
    (r'>Diet & Feeding<', '>Dieta y Alimentación<'),
    (r'>Tank Mate Compatibility<', '>Compatibilidad con Compañeros<'),
    (r'>Compatible With<', '>Compatible Con<'),
    (r'>Avoid Keeping With<', '>Evitar Mantener Con<'),
    (r'>Care Tips<', '>Consejos de Cuidados<'),
    (r'>Expert Tips<', '>Consejos de Expertos<'),
    
    # Labels
    (r'>Minimum Tank<', '>Tanque Mínimo<'),
    (r'>Adult Size<', '>Tamaño Adulto<'),
    (r'>Min Tank Size<', '>Tamaño Mín. Tanque<'),
    (r'Minimum (\d+L \(\d+gal\)) tank required', r'Tanque mínimo de \1 requerido'),
    (r'>Temperature:<', '>Temperatura:<'),
    (r'>Category:<', '>Categoría:<'),
    (r'>Diet type:<', '>Tipo de dieta:<'),
    (r'>Feed 1-2 times daily<', '>Alimentar 1-2 veces al día<'),
    (r'>Varied diet recommended<', '>Dieta variada recomendada<'),
    (r'>Not compatible<', '>No compatible<'),
    (r' years<', ' años<'),
    (r' year<', ' año<'),
    
    # Quick Facts
    (r'>Puede Estar Solo<', '>Puede Estar Solo<'),  # Already Spanish
    
    # CTA section
    (r'>Crea Tu Tanque Comunitario Perfecto<', '>Crea Tu Tanque Comunitario Perfecto<'),  # Already Spanish
    (r'Encuentra compañeros compatibles for your (.+?)<', r'Encuentra compañeros compatibles para tu \1<'),
    (r'>Compatibility Checker<', '>Verificador de Compatibilidad<'),
    (r'>Browse Setups<', '>Explorar Configuraciones<'),
    (r'Check more combinations with our Compatibility Checker', 'Verifica más combinaciones con nuestro Verificador de Compatibilidad'),
    
    # Misc
    (r'>Corydoras<', '>Corydoras<'),
    (r'>Snails<', '>Caracoles<'),
    (r'>Other Bettas<', '>Otros Bettas<'),
    (r'>Guppies<', '>Guppies<'),
    (r'>Bright Fish<', '>Peces Brillantes<'),
]

def get_fish_name_es(fish_id, default_name):
    """Get Spanish fish name or return default"""
    return fish_names_es.get(fish_id, default_name)

def translate_fish_page(file_path, fish_id):
    """Translate a single fish page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get fish data
    fish = next((f for f in fish_list if f['id'] == fish_id), None)
    if not fish:
        print(f"  Warning: No fish data for {fish_id}")
        return
    
    english_name = fish['name']
    spanish_name = get_fish_name_es(fish_id, english_name)
    
    # Replace fish name in title and meta
    content = content.replace(
        f'<title>{english_name} Care Guide | FishFinder</title>',
        f'<title>{spanish_name} - Guía de Cuidados | FishFinder</title>'
    )
    
    # Apply all replacements
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Translate category
    if fish.get('category'):
        cat_en = fish['category']
        cat_es = category_es.get(cat_en, cat_en)
        content = content.replace(f'>Category: {cat_en.title()}<', f'>Categoría: {cat_es}<')
        content = content.replace(f'Category: {cat_en.title()}', f'Categoría: {cat_es}')
    
    # Translate diet
    if fish.get('diet'):
        diet_en = fish['diet']
        diet_es_val = diet_es.get(diet_en, diet_en)
        content = content.replace(f'>Diet type: {diet_en.title()}<', f'>Tipo de dieta: {diet_es_val}<')
        content = content.replace(f'Diet type: {diet_en.title()}', f'Tipo de dieta: {diet_es_val}')
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    es_peces_dir = os.path.expanduser("~/clawd/aquarium-fish/es/peces")
    
    if not os.path.exists(es_peces_dir):
        print(f"Directory not found: {es_peces_dir}")
        return
    
    fish_dirs = [d for d in os.listdir(es_peces_dir) if os.path.isdir(os.path.join(es_peces_dir, d))]
    
    print(f"Found {len(fish_dirs)} fish directories to process")
    
    for i, fish_id in enumerate(fish_dirs):
        file_path = os.path.join(es_peces_dir, fish_id, "index.html")
        if os.path.exists(file_path):
            print(f"[{i+1}/{len(fish_dirs)}] Translating {fish_id}...")
            translate_fish_page(file_path, fish_id)
        else:
            print(f"  Warning: No index.html for {fish_id}")
    
    print(f"\nDone! Translated {len(fish_dirs)} fish pages.")

if __name__ == "__main__":
    main()
