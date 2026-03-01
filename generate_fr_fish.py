#!/usr/bin/env python3
"""Generate French fish pages from English ones."""
import os
import re
import shutil

# Directories
EN_FISH_DIR = "fish"
FR_FISH_DIR = "fr/poissons"

# Create output directory
os.makedirs(FR_FISH_DIR, exist_ok=True)

# Translation patterns (English -> French)
TRANSLATIONS = [
    # Fish name translations (titles)
    (r'Bristlenose Pleco', 'Ancistrus'),
    (r'>Common Pleco<', '>Pléco commun<'),
    (r'>Clown Pleco<', '>Pléco clown<'),
    (r'>Rubber Lip Pleco<', '>Pléco à lèvres caoutchouteuses<'),
    (r'>Zebra Pleco<', '>Pléco zèbre<'),
    (r'>Neon Tetra<', '>Néon bleu<'),
    (r'>Cardinal Tetra<', '>Néon cardinalis<'),
    (r'>Rummy Nose Tetra<', '>Nez rouge<'),
    (r'>Ember Tetra<', '>Tétra braise<'),
    (r'>Black Neon Tetra<', '>Néon noir<'),
    (r'>Guppy<', '>Guppy<'),
    (r'>Betta Fish<', '>Combattant<'),
    (r'>Goldfish<', '>Poisson rouge<'),
    (r'>Angelfish<', '>Scalaire<'),
    (r'>Discus<', '>Discus<'),
    (r'>Oscar<', '>Oscar<'),
    (r'>Corydoras Catfish<', '>Corydoras<'),
    (r'>Bronze Cory<', '>Corydoras bronze<'),
    (r'>Panda Cory<', '>Corydoras panda<'),
    (r'>Peppered Cory<', '>Corydoras poivré<'),
    (r'>Julii Cory<', '>Corydoras julii<'),
    (r'>Pygmy Cory<', '>Corydoras pygmée<'),
    (r'>Sterbai Cory<', '>Corydoras sterbai<'),
    (r'>Cherry Barb<', '>Barbus cerise<'),
    (r'>Tiger Barb<', '>Barbus de Sumatra<'),
    (r'>Rosy Barb<', '>Barbus rosé<'),
    (r'>Zebra Danio<', '>Danio zébré<'),
    (r'>Pearl Danio<', '>Danio perle<'),
    (r'>Celestial Pearl Danio<', '>Danio margaritatus<'),
    (r'>Harlequin Rasbora<', '>Rasbora arlequin<'),
    (r'>Chili Rasbora<', '>Rasbora chili<'),
    (r'>Dwarf Gourami<', '>Gourami nain<'),
    (r'>Pearl Gourami<', '>Gourami perlé<'),
    (r'>Honey Gourami<', '>Gourami miel<'),
    (r'>Blue Gourami<', '>Gourami bleu<'),
    (r'>Molly<', '>Molly<'),
    (r'>Platy<', '>Platy<'),
    (r'>Swordtail<', '>Xipho<'),
    (r'>Endler<', '>Endler<'),
    (r'>Siamese Fighting Fish<', '>Combattant<'),
    (r'>Kuhli Loach<', '>Loche coolie<'),
    (r'>Clown Loach<', '>Loche clown<'),
    (r'>Yoyo Loach<', '>Loche yoyo<'),
    (r'>Hillstream Loach<', '>Loche de torrent<'),
    (r'>Otocinclus<', '>Otocinclus<'),
    (r'>Amano Shrimp<', '>Crevette Amano<'),
    (r'>Cherry Shrimp<', '>Crevette cerise<'),
    (r'>Ghost Shrimp<', '>Crevette fantôme<'),
    (r'>Nerite Snail<', '>Escargot nérite<'),
    (r'>Mystery Snail<', '>Ampullaire<'),
    (r'>Assassin Snail<', '>Escargot assassin<'),
    (r'>Ram Cichlid<', '>Ramirezi<'),
    (r'>German Blue Ram<', '>Ramirezi bleu allemand<'),
    (r'>Bolivian Ram<', '>Ramirezi bolivien<'),
    (r'>Apistogramma<', '>Apistogramma<'),
    (r'>Kribensis<', '>Pelvicachromis<'),
    (r'>Electric Blue Acara<', '>Acara bleu électrique<'),
    (r'>Firemouth Cichlid<', '>Cichlidé à gorge de feu<'),
    (r'>Convict Cichlid<', '>Cichlidé zèbre<'),
    (r'>Jack Dempsey<', '>Jack Dempsey<'),
    (r'>Green Terror<', '>Terreur verte<'),
    (r'>Flowerhorn<', '>Flowerhorn<'),
    (r'>African Cichlid<', '>Cichlidé africain<'),
    (r'>Yellow Lab<', '>Labidochromis jaune<'),
    (r'>Red Zebra<', '>Zèbre rouge<'),
    (r'>Rainbow Fish<', '>Poisson arc-en-ciel<'),
    (r'>Boesemani Rainbow<', '>Arc-en-ciel de Boeseman<'),
    (r'>White Cloud Mountain Minnow<', '>Vairon de Chine<'),
    (r'>Killifish<', '>Killi<'),
    (r'>Rainbowfish<', '>Poisson arc-en-ciel<'),
    
    # Meta/HTML
    (r'lang="en"', 'lang="fr"'),
    
    # Title and meta tags
    (r'Care Guide \| FishFinder', "Guide d'entretien | FishFinder"),
    (r'Care Guide, Tank Size & Compatibility', "Guide d'entretien, taille d'aquarium et compatibilité"),
    
    # Meta descriptions
    (r'Complete (.+?) care guide\. Learn about tank size', r"Guide complet d'entretien \1. Découvrez la taille d'aquarium"),
    (r'water parameters', "paramètres d'eau"),
    (r'compatible tankmates', 'colocataires compatibles'),
    (r'expert care tips', "conseils d'experts"),
    
    # Navigation
    (r'>Fish</a>', '>Poissons</a>'),
    (r'>Quiz</a>', '>Quiz</a>'),
    (r'>Compare</a>', '>Comparer</a>'),
    (r'>Search</a>', '>Rechercher</a>'),
    (r'>Breeds</a>', '>Races</a>'),
    (r'href="/fish/"', 'href="/fr/poissons/"'),
    (r'href="/quiz/"', 'href="/fr/quiz/"'),
    (r'href="/compare/"', 'href="/fr/comparer/"'),
    (r'href="/search/"', 'href="/fr/rechercher/"'),
    (r'href="/"', 'href="/fr/"'),
    
    # Breadcrumb
    (r'>Home<', '>Accueil<'),
    (r'>Fish<', '>Poissons<'),
    (r'aria-label="Breadcrumb"', 'aria-label="Fil d\'Ariane"'),
    
    # Quick Facts section
    (r'>Quick Facts<', '>Fiche rapide<'),
    (r'>Tank Size<', ">Taille d'aquarium<"),
    (r'>Temperature<', '>Température<'),
    (r'>pH Range<', '>Plage de pH<'),
    (r'>Care Level<', '>Niveau de soin<'),
    (r'>Temperament<', '>Tempérament<'),
    (r'>Diet<', '>Régime<'),
    (r'>Size<', '>Taille<'),
    (r'>Lifespan<', '>Espérance de vie<'),
    (r'>Origin<', '>Origine<'),
    
    # Care levels
    (r'>Easy<', '>Facile<'),
    (r'>Moderate<', '>Modéré<'),
    (r'>Difficult<', '>Difficile<'),
    (r'>Beginner<', '>Débutant<'),
    (r'>Intermediate<', '>Intermédiaire<'),
    (r'>Advanced<', '>Avancé<'),
    (r'>Expert<', '>Expert<'),
    
    # Temperament
    (r'>Peaceful<', '>Paisible<'),
    (r'>Semi-aggressive<', '>Semi-agressif<'),
    (r'>Aggressive<', '>Agressif<'),
    (r'>Community<', '>Communautaire<'),
    (r'>Shy<', '>Timide<'),
    (r'>Active<', '>Actif<'),
    (r'>Schooling<', '>Grégaire<'),
    
    # Diet
    (r'>Omnivore<', '>Omnivore<'),
    (r'>Carnivore<', '>Carnivore<'),
    (r'>Herbivore<', '>Herbivore<'),
    (r'>Algae Eater<', ">Mangeur d'algues<"),
    (r'>Scavenger<', '>Nettoyeur<'),
    
    # Units - gallons to liters (be careful with boundaries)
    (r'>(\d+)\s*gal<', lambda m: f'>{int(m.group(1)) * 3.785:.0f}L<'),
    (r'>(\d+)\s*gallons<', lambda m: f'>{int(m.group(1)) * 3.785:.0f} litres<'),
    
    # Units - inches to cm (only in content, not classes)
    (r'>(\d+(?:\.\d+)?)"<', lambda m: f'>{float(m.group(1)) * 2.54:.1f}cm<'),
    (r'>(\d+(?:\.\d+)?)\s*inches<', lambda m: f'>{float(m.group(1)) * 2.54:.1f}cm<'),
    
    # Section headers
    (r'>Overview<', '>Présentation<'),
    (r'>Description<', '>Description<'),
    (r'>Tank Requirements<', ">Exigences de l'aquarium<"),
    (r'>Water Parameters<', ">Paramètres de l'eau<"),
    (r'>Tank Mates<', '>Colocataires<'),
    (r'>Compatible Tank Mates<', '>Colocataires compatibles<'),
    (r'>Feeding<', '>Alimentation<'),
    (r'>Feeding & Diet<', '>Alimentation et régime<'),
    (r'>Breeding<', '>Reproduction<'),
    (r'>Care Tips<', ">Conseils d'entretien<"),
    (r'>Health<', '>Santé<'),
    (r'>Behavior<', '>Comportement<'),
    
    # Tank mates section
    (r'>Good Tank Mates<', '>Bons colocataires<'),
    (r'>Bad Tank Mates<', '>Mauvais colocataires<'),
    (r'>Avoid<', '>À éviter<'),
    (r'>Best With<', '>Idéal avec<'),
    (r'>Can Live With<', '>Peut vivre avec<'),
    (r'>Not Compatible<', '>Non compatible<'),
    
    # Common fish categories
    (r'African Cichlids', 'Cichlidés africains'),
    (r'South American Cichlids', 'Cichlidés sud-américains'),
    (r'Central American Cichlids', 'Cichlidés d\'Amérique centrale'),
    (r'Dwarf Cichlids', 'Cichlidés nains'),
    (r'Livebearers', 'Vivipares'),
    (r'Livebearer', 'Vivipare'),
    (r'Catfish', 'Poisson-chat'),
    (r'Corydoras', 'Corydoras'),
    (r'Tetras', 'Tétras'),
    (r'Tetra', 'Tétra'),
    (r'Barbs', 'Barbus'),
    (r'Barb', 'Barbus'),
    (r'Rasboras', 'Rasboras'),
    (r'Rasbora', 'Rasbora'),
    (r'Danios', 'Danios'),
    (r'Danio', 'Danio'),
    (r'Gouramis', 'Gouramis'),
    (r'Gourami', 'Gourami'),
    (r'Loaches', 'Loches'),
    (r'Loach', 'Loche'),
    (r'Plecos', 'Plécos'),
    (r' pleco ', ' pléco '),
    (r' pleco\.', ' pléco.'),
    (r'Shrimp', 'Crevettes'),
    (r'Snails', 'Escargots'),
    (r'Snail', 'Escargot'),
    
    # Common phrases in descriptions
    (r'is a popular', 'est un'),
    (r'are popular', 'sont des'),
    (r'beginner-friendly', 'adapté aux débutants'),
    (r'easy to care for', 'facile à entretenir'),
    (r'low maintenance', 'peu exigeant'),
    (r'peaceful community fish', 'poisson communautaire paisible'),
    (r'community tank', 'aquarium communautaire'),
    (r'planted tank', 'aquarium planté'),
    (r'heavily planted', 'densément planté'),
    (r'live plants', 'plantes vivantes'),
    (r'hiding spots', 'cachettes'),
    (r'hiding places', 'cachettes'),
    (r'driftwood', 'bois flotté'),
    (r'rocks and caves', 'roches et grottes'),
    (r'sandy substrate', 'substrat sablonneux'),
    (r'gravel substrate', 'substrat de gravier'),
    (r'fine substrate', 'substrat fin'),
    (r'water flow', "courant d'eau"),
    (r'low flow', 'faible courant'),
    (r'moderate flow', 'courant modéré'),
    (r'strong flow', 'fort courant'),
    (r'water quality', "qualité de l'eau"),
    (r'water changes', "changements d'eau"),
    (r'weekly water changes', "changements d'eau hebdomadaires"),
    (r'regular water changes', "changements d'eau réguliers"),
    (r'clean water', 'eau propre'),
    (r'soft water', 'eau douce'),
    (r'hard water', 'eau dure'),
    (r'acidic water', 'eau acide'),
    (r'alkaline water', 'eau alcaline'),
    (r'neutral pH', 'pH neutre'),
    
    # Feeding phrases
    (r'high-quality', 'de haute qualité'),
    (r'flake food', 'nourriture en flocons'),
    (r'pellet food', 'nourriture en granulés'),
    (r'frozen food', 'nourriture congelée'),
    (r'live food', 'nourriture vivante'),
    (r'algae wafers', "pastilles d'algues"),
    (r'bloodworms', 'vers de vase'),
    (r'brine shrimp', 'artémias'),
    (r'daphnia', 'daphnies'),
    (r'blanched vegetables', 'légumes blanchis'),
    (r'Feed 1-2 times daily', 'Nourrir 1-2 fois par jour'),
    (r'Feed 2-3 times daily', 'Nourrir 2-3 fois par jour'),
    (r'varied diet', 'régime varié'),
    (r'balanced diet', 'régime équilibré'),
    
    # Breeding phrases
    (r'easy to breed', 'facile à reproduire'),
    (r'difficult to breed', 'difficile à reproduire'),
    (r'egg layer', 'ovipare'),
    (r'egg layers', 'ovipares'),
    (r'live bearer', 'vivipare'),
    (r'live-bearer', 'vivipare'),
    (r'bubble nest', 'nid de bulles'),
    (r'breeding tank', 'aquarium de reproduction'),
    (r'spawning', 'ponte'),
    (r'fry', 'alevins'),
    
    # Care tips
    (r'Keep in groups', 'Maintenir en groupe'),
    (r'Keep in schools', 'Maintenir en banc'),
    (r'school of', 'banc de'),
    (r'group of', 'groupe de'),
    (r'at least 6', 'au moins 6'),
    (r'at least 5', 'au moins 5'),
    (r'single specimen', 'spécimen unique'),
    (r'pairs', 'couples'),
    (r'Provide plenty of', 'Fournir beaucoup de'),
    (r'Requires', 'Nécessite'),
    (r'Needs', 'A besoin de'),
    (r'Prefers', 'Préfère'),
    (r'Thrives in', 'Prospère dans'),
    (r'Does well in', 'Se porte bien dans'),
    (r'sensitive to', 'sensible à'),
    (r'prone to', 'sujet à'),
    
    # Behavior descriptions
    (r'bottom dweller', 'poisson de fond'),
    (r'bottom-dwelling', 'vivant au fond'),
    (r'mid-level', 'niveau intermédiaire'),
    (r'mid-water', 'pleine eau'),
    (r'surface dweller', 'poisson de surface'),
    (r'top-dwelling', 'vivant en surface'),
    (r'active swimmer', 'nageur actif'),
    (r'slow swimmer', 'nageur lent'),
    (r'territorial', 'territorial'),
    (r'fin nipper', 'mordeur de nageoires'),
    (r'fin nipping', 'mordillement de nageoires'),
    (r'jumper', 'sauteur'),
    (r'may jump', 'peut sauter'),
    (r'tight-fitting lid', 'couvercle bien ajusté'),
    (r'nocturnal', 'nocturne'),
    (r'diurnal', 'diurne'),
    
    # Size descriptions
    (r'small fish', 'petit poisson'),
    (r'medium-sized', 'de taille moyenne'),
    (r'large fish', 'gros poisson'),
    (r'nano fish', 'nano poisson'),
    (r'dwarf', 'nain'),
    (r'giant', 'géant'),
    (r'grows up to', "grandit jusqu'à"),
    (r'can reach', 'peut atteindre'),
    (r'maximum size', 'taille maximale'),
    (r'adult size', 'taille adulte'),
    
    # Lifespan
    (r'(\d+)-(\d+) years', r'\1-\2 ans'),
    (r'(\d+) years', r'\1 ans'),
    (r'lifespan of', 'durée de vie de'),
    (r'can live', 'peut vivre'),
    (r'up to (\d+) years', r"jusqu'à \1 ans"),
    
    # Health
    (r'hardy', 'robuste'),
    (r'sensitive', 'sensible'),
    (r'disease-resistant', 'résistant aux maladies'),
    (r'ich', 'ichtyophthiriose'),
    (r'fin rot', 'pourriture des nageoires'),
    (r'dropsy', 'hydropisie'),
    (r'quarantine', 'quarantaine'),
    
    # Colors (only in content context, not CSS)
    (r'>colorful<', '>coloré<'),
    (r'>vibrant<', '>vif<'),
    (r'>iridescent<', '>iridescent<'),
    (r' colorful ', ' coloré '),
    (r' vibrant ', ' vif '),
    (r' striped ', ' rayé '),
    (r' spotted ', ' tacheté '),
    
    # Common descriptive phrases
    (r'one of the most popular', "l'un des plus populaires"),
    (r'perfect for beginners', 'parfait pour les débutants'),
    (r'great for beginners', 'idéal pour les débutants'),
    (r'ideal for', 'idéal pour'),
    (r'perfect for', 'parfait pour'),
    (r'suitable for', 'adapté pour'),
    (r'not suitable for', 'non adapté pour'),
    (r'best kept', 'à maintenir de préférence'),
    (r'should be kept', 'devrait être maintenu'),
    (r'must be kept', 'doit être maintenu'),
    (r'can be kept', 'peut être maintenu'),
    (r'native to', 'originaire de'),
    (r'found in', 'trouvé dans'),
    (r'South America', 'Amérique du Sud'),
    (r'Central America', 'Amérique centrale'),
    (r'Southeast Asia', 'Asie du Sud-Est'),
    (r'Africa', 'Afrique'),
    (r'Amazon', 'Amazone'),
    
    # Additional phrases
    (r'King of the aquarium', "Roi de l'aquarium"),
    (r'Perfect for nano tanks', 'Parfait pour les nano aquariums'),
    (r'nano tank', 'nano aquarium'),
    (r'aquarium hobby', "hobby de l'aquariophilie"),
    (r'aquarium fish', "poisson d'aquarium"),
    (r'freshwater fish', "poisson d'eau douce"),
    (r'tropical fish', 'poisson tropical'),
    (r'coldwater fish', "poisson d'eau froide"),
    (r'disc-shaped', 'en forme de disque'),
    (r'torpedo-shaped', 'en forme de torpille'),
    (r'elongated', 'allongé'),
    (r'compressed', 'comprimé'),
    (r'labyrinth fish', 'poisson à labyrinthe'),
    (r'labyrinth organ', 'organe labyrinthe'),
    (r'can breathe air', "peut respirer l'air"),
    (r'surface breather', 'respirateur de surface'),
    (r'Needs high oxygen', "A besoin d'un fort taux d'oxygène"),
    (r'high oxygen', "fort taux d'oxygène"),
    (r'oxygenated water', 'eau bien oxygénée'),
    (r'Good cleanup crew', 'Bon équipier de nettoyage'),
    (r'cleanup crew', 'équipe de nettoyage'),
    (r'algae control', "contrôle des algues"),
    (r'eats algae', 'mange les algues'),
    (r'algae eater', "mangeur d'algues"),
    (r'scavenger', 'nettoyeur'),
    (r'substrate sifter', 'fouilleur de substrat'),
    
    # Category labels
    (r'>Category:', '>Catégorie :'),
    (r'Category: Livebearer', 'Catégorie : Vivipare'),
    (r'Category: Catfish', 'Catégorie : Poisson-chat'),
    (r'Category: Cichlid', 'Catégorie : Cichlidé'),
    (r'Category: Tetra', 'Catégorie : Tétra'),
    (r'Category: Barb', 'Catégorie : Barbus'),
    (r'Category: Rasbora', 'Catégorie : Rasbora'),
    (r'Category: Danio', 'Catégorie : Danio'),
    (r'Category: Gourami', 'Catégorie : Gourami'),
    (r'Category: Loach', 'Catégorie : Loche'),
    (r'Category: Pleco', 'Catégorie : Pléco'),
    (r'Category: Shrimp', 'Catégorie : Crevette'),
    (r'Category: Snail', 'Catégorie : Escargot'),
    (r'Category: Betta', 'Catégorie : Combattant'),
    (r'Category: Goldfish', 'Catégorie : Poisson rouge'),
    (r'Category: Rainbowfish', 'Catégorie : Arc-en-ciel'),
    
    # Language switcher
    (r'<a href="/fish/', '<a href="/fr/poissons/'),
    (r'<a href="/de/fische/', '<a href="/de/fische/'),
    (r'<a href="/es/peces/', '<a href="/es/peces/'),
    
    # Footer
    (r'>About</a>', '>À propos</a>'),
    (r'>Contact</a>', '>Contact</a>'),
    (r'>Privacy Policy</a>', '>Politique de confidentialité</a>'),
    (r'All rights reserved', 'Tous droits réservés'),
    
    # Misc UI
    (r'>Learn More<', '>En savoir plus<'),
    (r'>Read More<', '>Lire la suite<'),
    (r'>View All<', '>Voir tout<'),
    (r'>Back to<', '>Retour à<'),
    (r'>Share<', '>Partager<'),
    (r'>Print<', '>Imprimer<'),
    (r'>Related Fish<', '>Poissons similaires<'),
    (r'>Similar Fish<', '>Poissons similaires<'),
    (r'>See Also<', '>Voir aussi<'),
    
    # Common standalone words (careful with boundaries)
    (r' the ', ' le '),
    (r' and ', ' et '),
    (r' or ', ' ou '),
    (r' with ', ' avec '),
    (r' from ', ' de '),
    (r' this ', ' ce '),
    (r' that ', ' ce '),
    (r' these ', ' ces '),
    (r' their ', ' leur '),
    (r' other ', ' autre '),
    (r' more ', ' plus '),
    (r' very ', ' très '),
    (r' also ', ' aussi '),
    (r' but ', ' mais '),
]

def translate_content(content):
    """Apply all translations to content."""
    for pattern, replacement in TRANSLATIONS:
        if callable(replacement):
            content = re.sub(pattern, replacement, content)
        else:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE if pattern[0].islower() else 0)
    return content

def process_fish_page(fish_slug):
    """Process a single fish page."""
    en_path = os.path.join(EN_FISH_DIR, fish_slug, "index.html")
    fr_path = os.path.join(FR_FISH_DIR, fish_slug, "index.html")
    
    if not os.path.exists(en_path):
        return False
    
    # Read English content
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply translations
    content = translate_content(content)
    
    # Create French directory and write file
    os.makedirs(os.path.dirname(fr_path), exist_ok=True)
    with open(fr_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Generate all French fish pages."""
    # Get all fish directories
    fish_dirs = [d for d in os.listdir(EN_FISH_DIR) 
                 if os.path.isdir(os.path.join(EN_FISH_DIR, d))]
    
    count = 0
    for fish_slug in sorted(fish_dirs):
        if process_fish_page(fish_slug):
            count += 1
            print(f"✓ {fish_slug}")
    
    print(f"\nDone! Created {count} French fish pages in {FR_FISH_DIR}/")

if __name__ == "__main__":
    main()
