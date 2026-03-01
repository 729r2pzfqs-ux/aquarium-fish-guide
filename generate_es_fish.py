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
    
    # Title and meta
    (r'Care Guide \| FishFinder', 'Guía de Cuidado | FishFinder'),
    (r'Care Guide, Tank Size & Compatibility', 'Guía de Cuidado, Tamaño del Tanque y Compatibilidad'),
    (r'Complete (.+?) care guide\. Learn about tank size', r'Guía completa de cuidado del \1. Aprende sobre tamaño del tanque'),
    (r'water parameters', 'parámetros del agua'),
    (r'compatible tankmates', 'compañeros de tanque compatibles'),
    (r'expert care tips', 'consejos de cuidado expertos'),
    (r', and ', ', y '),
    (r' and ', ' y '),
    (r'\(10 gallons\)', '(38L)'),
    (r'\(20 gallons\)', '(75L)'),
    (r'\(30 gallons\)', '(114L)'),
    (r'\(5 gallons\)', '(19L)'),
    
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
    
    # Section headings
    (r'>About ([^<]+)<', r'>Sobre \1<'),
    (r'>Care Requirements<', '>Requisitos de Cuidado<'),
    (r'>Care Tips<', '>Consejos de Cuidado<'),
    (r'Tank Setup', 'Configuración del Tanque'),
    (r'Diet & Feeding', 'Dieta y Alimentación'),
    
    # Care notes
    (r'Minimum 5-gallon tank required', 'Se requiere tanque mínimo de 19L'),
    (r'Minimum 10-gallon tank required', 'Se requiere tanque mínimo de 38L'),
    (r'Minimum 20-gallon tank required', 'Se requiere tanque mínimo de 75L'),
    (r'Minimum 30-gallon tank required', 'Se requiere tanque mínimo de 114L'),
    (r'Minimum 40-gallon tank required', 'Se requiere tanque mínimo de 151L'),
    (r'Minimum 50-gallon tank required', 'Se requiere tanque mínimo de 189L'),
    (r'Feed 1-2 times daily', 'Alimentar 1-2 veces al día'),
    (r'Feed 2-3 times daily', 'Alimentar 2-3 veces al día'),
    
    # Categories
    (r'Category: Livebearer', 'Categoría: Vivíparo'),
    (r'Category: Cichlid', 'Categoría: Cíclido'),
    (r'Category: Tetra', 'Categoría: Tetra'),
    (r'Category: Catfish', 'Categoría: Pez Gato'),
    (r'Category: Shrimp', 'Categoría: Gamba'),
    (r'Category: Snail', 'Categoría: Caracol'),
    (r'Category: Loach', 'Categoría: Locha'),
    (r'Category: Barb', 'Categoría: Barbo'),
    (r'Category: Gourami', 'Categoría: Gurami'),
    (r'Category: Betta', 'Categoría: Betta'),
    (r'Category: Pleco', 'Categoría: Pleco'),
    (r'Category: Corydoras', 'Categoría: Corydora'),
    
    # Fish descriptions
    (r'Colorful and active', 'Colorido y activo'),
    (r'livebearers', 'vivíparos'),
    (r'Livebearers', 'Vivíparos'),
    (r'Breed readily in home aquariums', 'Se reproducen fácilmente en acuarios domésticos'),
    (r'Many color varieties', 'Muchas variedades de color'),
    (r'Easy to breed', 'Fácil de criar'),
    (r'Hardy species', 'Especie resistente'),
    (r'Beginner friendly', 'Apto para principiantes'),
    (r'Low maintenance', 'Bajo mantenimiento'),
    (r'Active swimmers', 'Nadadores activos'),
    (r'Peaceful community fish', 'Pez comunitario pacífico'),
    (r'A centerpiece fish', 'Un pez central'),
    (r'for larger tanks', 'para tanques grandes'),
    (r'Elegant cichlids', 'Cíclidos elegantes'),
    (r'with tall, triangular bodies', 'con cuerpos altos y triangulares'),
    
    # More care notes
    (r'Tall tank needed', 'Se necesita tanque alto'),
    (r'may eat small fish', 'puede comer peces pequeños'),
    (r'can be territorial when breeding', 'puede ser territorial al criar'),
    (r'Varied diet recommended', 'Se recomienda dieta variada'),
    (r'Weekly water changes', 'Cambios de agua semanales'),
    (r'Stable water parameters', 'Parámetros de agua estables'),
    (r'Provide hiding spots', 'Proporcionar escondites'),
    (r'Keep in groups', 'Mantener en grupos'),
    (r'Keep in schools', 'Mantener en cardúmenes'),
    
    # More UI
    (r'>Compare<', '>Comparar<'),
    (r'>Fish Quiz<', '>Test de Peces<'),
    (r'>Tank Mate Compatibility<', '>Compatibilidad de Compañeros<'),
    (r'>Min School<', '>Cardumen Mín<'),
    (r'>Not compatible<', '>No compatible<'),
    (r'Compare with Others', 'Comparar con Otros'),
    (r'Compatibility Checker', 'Verificador de Compatibilidad'),
    
    # Tank mates
    (r'>Fin Nippers<', '>Mordedores de Aletas<'),
    (r'>Large Cichlids<', '>Cíclidos Grandes<'),
    (r'>Small Fish<', '>Peces Pequeños<'),
    (r'>Large Fish<', '>Peces Grandes<'),
    (r'>Aggressive Fish<', '>Peces Agresivos<'),
    (r'>Bottom Dwellers<', '>Habitantes del Fondo<'),
    (r'>Peaceful Catfish<', '>Peces Gato Pacíficos<'),
    (r'>Other Livebearers<', '>Otros Vivíparos<'),
    (r'>Dwarf Shrimp<', '>Gambas Enanas<'),
    
    # Common fish names (keep recognizable but can translate)
    (r'>Tetras<', '>Tetras<'),
    (r'>Mollies<', '>Mollies<'),
    (r'>Platies<', '>Platys<'),
    (r'>Corydoras<', '>Corydoras<'),
    (r'>Gouramis<', '>Guramis<'),
    (r'>Rasboras<', '>Rasboras<'),
    
    # More sections
    (r'Avoid Keeping With', 'Evitar Mantener Con'),
    (r'Expert Tips', 'Consejos de Expertos'),
    (r'Diet type: Omnivore', 'Tipo de dieta: Omnívoro'),
    (r'Diet type: Carnivore', 'Tipo de dieta: Carnívoro'),
    (r'Diet type: Herbivore', 'Tipo de dieta: Herbívoro'),
    (r'for your ([^<]+)', r'para tu \1'),
    (r' for your ', ' para tu '),
    
    # Guppy specific
    (r'Keep more females than males', 'Mantener más hembras que machos'),
    (r'prolific breeders', 'criadores prolíficos'),
    (r'easy for beginners', 'fácil para principiantes'),
    
    # General care tips
    (r'Provide plenty of plants', 'Proporcionar muchas plantas'),
    (r'needs hiding spots', 'necesita escondites'),
    (r'Regular water changes', 'Cambios de agua regulares'),
    (r'Avoid overfeeding', 'Evitar sobrealimentar'),
    (r'Monitor water quality', 'Monitorear calidad del agua'),
    
    # Fish descriptions
    (r'One of the most peaceful', 'Uno de los más pacíficos'),
    (r'Bright yellow coloration', 'Coloración amarilla brillante'),
    (r'Bright coloration', 'Coloración brillante'),
    (r'>Other Mbuna<', '>Otros Mbuna<'),
    (r'>African Cichlids<', '>Cíclidos Africanos<'),
    (r'>South American Cichlids<', '>Cíclidos Sudamericanos<'),
    (r'>Central American Cichlids<', '>Cíclidos Centroamericanos<'),
    (r'>Peaceful Community Fish<', '>Peces Comunitarios Pacíficos<'),
    (r'>Peaceful Fish<', '>Peces Pacíficos<'),
    (r'>Community Fish<', '>Peces Comunitarios<'),
    (r'>Aggressive Fish<', '>Peces Agresivos<'),
    (r'>Semi-Aggressive Fish<', '>Peces Semi-Agresivos<'),
    (r'>Small Peaceful Fish<', '>Peces Pacíficos Pequeños<'),
    (r'>Larger Tetras<', '>Tetras Más Grandes<'),
    (r'>Small Tetras<', '>Tetras Pequeños<'),
    (r'>Other Livebearers<', '>Otros Vivíparos<'),
    (r'>Other Gouramis<', '>Otros Guramis<'),
    (r'>Other Cichlids<', '>Otros Cíclidos<'),
    (r'>Dwarf Cichlids<', '>Cíclidos Enanos<'),
    (r'>Peaceful Catfish<', '>Peces Gato Pacíficos<'),
    (r'>Larger Fish<', '>Peces Más Grandes<'),
    (r'>Smaller Fish<', '>Peces Más Pequeños<'),
    (r'>Invertebrates<', '>Invertebrados<'),
    (r'>Snails<', '>Caracoles<'),
    (r'>Shrimp<', '>Gambas<'),
    (r'Hard alkaline water required', 'Se requiere agua dura alcalina'),
    (r'keep with other Mbuna', 'mantener con otros Mbuna'),
    (r'overstocking reduces aggression', 'el exceso de población reduce la agresión'),
    (r'Hardy and colorful', 'Resistente y colorido'),
    (r'Popular aquarium fish', 'Pez de acuario popular'),
    (r'Easy to keep', 'Fácil de mantener'),
    (r'Striking appearance', 'Apariencia llamativa'),
    (r'Beautiful finnage', 'Hermoso aletaje'),
    (r'Interesting behavior', 'Comportamiento interesante'),
    (r'Great algae eater', 'Excelente comedor de algas'),
    (r'Excellent scavenger', 'Excelente carroñero'),
    (r'Nocturnal species', 'Especie nocturna'),
    (r'Shy species', 'Especie tímida'),
    (r'Bold and active', 'Audaz y activo'),
    
    # More fish descriptions
    (r'Hardy and common', 'Resistente y común'),
    (r'Also called', 'También llamado'),
    (r'Can be territorial', 'Puede ser territorial'),
    (r'Three-spot Gourami', 'Gurami de Tres Puntos'),
    (r'common gourami', 'gurami común'),
    (r'Hardy and peaceful', 'Resistente y pacífico'),
    (r'Hardy and active', 'Resistente y activo'),
    (r'Shy and peaceful', 'Tímido y pacífico'),
    (r'Active and colorful', 'Activo y colorido'),
    (r'Peaceful schooling fish', 'Pez de cardumen pacífico'),
    (r'Popular beginner fish', 'Pez popular para principiantes'),
    (r'Classic aquarium fish', 'Pez de acuario clásico'),
    (r'Great community fish', 'Excelente pez comunitario'),
    (r'Excellent algae eater', 'Excelente comedor de algas'),
    (r'Loves planted tanks', 'Ama los tanques plantados'),
    (r'Needs warm water', 'Necesita agua cálida'),
    (r'Prefers soft water', 'Prefiere agua blanda'),
    (r'Requires good filtration', 'Requiere buena filtración'),
    
    # Common description phrases
    (r'Very energetic', 'Muy enérgico'),
    (r'Very peaceful', 'Muy pacífico'),
    (r'Very social', 'Muy social'),
    (r'Very hardy', 'Muy resistente'),
    (r'Very active', 'Muy activo'),
    (r'Very aggressive', 'Muy agresivo'),
    (r'Very popular', 'Muy popular'),
    (r'Great snail controller', 'Gran controlador de caracoles'),
    (r'Great tank cleaners', 'Grandes limpiadores de tanque'),
    (r'Great with', 'Genial con'),
    (r'Excellent snail control', 'Excelente control de caracoles'),
    (r'Excellent tank cleaners', 'Excelentes limpiadores de tanque'),
    (r'Keep in large groups', 'Mantener en grupos grandes'),
    (r'Keep in groups', 'Mantener en grupos'),
    (r'Keep in schools', 'Mantener en cardúmenes'),
    (r'known for', 'conocido por'),
    (r'fin nipping', 'mordisqueo de aletas'),
    (r'to curb aggression', 'para reducir la agresión'),
    (r'Prefers slightly cooler water', 'Prefiere agua ligeramente más fría'),
    (r'Prefers cooler water', 'Prefiere agua más fría'),
    (r'Prefers warmer water', 'Prefiere agua más cálida'),
    (r'Males are more colorful', 'Los machos son más coloridos'),
    (r'Males develop', 'Los machos desarrollan'),
    (r'Males have', 'Los machos tienen'),
    (r'Females develop', 'Las hembras desarrollan'),
    (r'Females have', 'Las hembras tienen'),
    (r'bottom-dwellers', 'habitantes del fondo'),
    (r'bottom dwellers', 'habitantes del fondo'),
    (r'armored', 'acorazado'),
    (r'schooler', 'pez de cardumen'),
    (r'schooling', 'cardumen'),
    (r'Peaceful', 'Pacífico'),
    (r'peaceful', 'pacífico'),
    (r'Active', 'Activo'),
    (r'active', 'activo'),
    (r'Hardy', 'Resistente'),
    (r'hardy', 'resistente'),
    (r'Unique', 'Único'),
    (r'unique', 'único'),
    (r'Beautiful', 'Hermoso'),
    (r'beautiful', 'hermoso'),
    (r'Colorful', 'Colorido'),
    (r'colorful', 'colorido'),
    (r'Elegant', 'Elegante'),
    (r'elegant', 'elegante'),
    (r'Stunning', 'Impresionante'),
    (r'stunning', 'impresionante'),
    (r'Distinctive', 'Distintivo'),
    (r'distinctive', 'distintivo'),
    (r'Popular', 'Popular'),
    (r'popular', 'popular'),
    (r'Adorable', 'Adorable'),
    (r'adorable', 'adorable'),
    (r'Attractive', 'Atractivo'),
    (r'attractive', 'atractivo'),
    (r'Delicate', 'Delicado'),
    (r'delicate', 'delicado'),
    (r'Brilliant', 'Brillante'),
    (r'brilliant', 'brillante'),
    (r'dwarf cichlid', 'cíclido enano'),
    (r'labyrinth fish', 'pez laberinto'),
    (r'with vibrant colors', 'con colores vibrantes'),
    (r'than females', 'que las hembras'),
    (r'extended fins', 'aletas extendidas'),
    (r'displays', 'muestra'),
    (r'breeding', 'reproducción'),
    (r'breeds', 'se reproduce'),
    (r'Breeds prolifically', 'Se reproduce prolíficamente'),
    (r'internal organs', 'órganos internos'),
    (r'transparent body', 'cuerpo transparente'),
    (r'completely transparent', 'completamente transparente'),
    (r'iridescent', 'iridiscente'),
    (r'coloration', 'coloración'),
    (r'variety is popular', 'variedad es popular'),
    (r'intensifies', 'se intensifica'),
    (r'during breeding', 'durante la reproducción'),
    (r'indicates health', 'indica salud'),
    (r'swims at', 'nada en'),
    (r'upward angle', 'ángulo ascendente'),
    (r'runs along', 'recorre'),
    (r'showing', 'mostrando'),
    (r'named after', 'nombrado en honor a'),
    (r'famous aquascaper', 'famoso aquascaper'),
    (r'won\'t reproduce in freshwater', 'no se reproduce en agua dulce'),
    (r'Many patterns', 'Muchos patrones'),
    (r'stays small', 'permanece pequeño'),
    (r'bristles on their nose', 'cerdas en la nariz'),
    (r'on their nose', 'en la nariz'),
    (r'including black beard algae', 'incluyendo alga barba negra'),
    (r'confused with', 'confundido con'),
    (r'Fine leopard spots', 'Finas manchas de leopardo'),
    (r'spotted', 'manchado'),
    (r'striped', 'rayado'),
    (r'long barbels', 'barbillas largas'),
    (r'panda-like markings', 'marcas similares a un panda'),
    (r'tolerates warmer water', 'tolera agua más cálida'),
    (r'from Lake', 'del Lago'),
    (r'in Papua New Guinea', 'en Papúa Nueva Guinea'),
    (r'turquoise-blue', 'azul turquesa'),
    (r'fiery red', 'rojo ardiente'),
    (r'flaring gills', 'branquias abiertas'),
    (r'copper', 'cobre'),
    (r'coppery', 'cobrizo'),
    (r'silvery', 'plateado'),
    (r'fin tips', 'puntas de aletas'),
    (r'wedge marking', 'marca en cuña'),
    (r'heart-shaped spot', 'mancha en forma de corazón'),
    (r'glowing', 'brillante'),
    (r'smoky grey', 'gris ahumado'),
    (r'black markings', 'marcas negras'),
    (r'black stripe', 'raya negra'),
    (r'red nose', 'nariz roja'),
    (r'from Madagascar', 'de Madagascar'),
    (r'Yellow body', 'Cuerpo amarillo'),
    (r'West African', 'Africano occidental'),
    (r'bright pink belly', 'vientre rosa brillante'),
    (r'dorsal fin', 'aleta dorsal'),
    
    # More common phrases
    (r'One of the most', 'Uno de los más'),
    (r'aquarium fish', 'peces de acuario'),
    (r'blue and red', 'azul y rojo'),
    (r'Must be kept in schools', 'Debe mantenerse en cardúmenes'),
    (r'Must be kept', 'Debe mantenerse'),
    (r'great for', 'genial para'),
    (r'unheated tanks', 'tanques sin calefacción'),
    (r'coldwater fish', 'pez de agua fría'),
    (r'Tiny algae eaters', 'Pequeños comedores de algas'),
    (r'Very gentle', 'Muy gentil'),
    (r'gentle', 'gentil'),
    (r'coloring', 'coloración'),
    (r'that are great', 'que son geniales'),
    (r'that are', 'que son'),
    (r'with black', 'con negro'),
    (r'with red', 'con rojo'),
    (r'with blue', 'con azul'),
    (r'with yellow', 'con amarillo'),
    (r'with white', 'con blanco'),
    (r'with orange', 'con naranja'),
    (r'blue', 'azul'),
    (r'red', 'rojo'),
    (r'yellow', 'amarillo'),
    (r'orange', 'naranja'),
    (r'green', 'verde'),
    (r'black', 'negro'),
    (r'white', 'blanco'),
    (r'pink', 'rosa'),
    (r'purple', 'púrpura'),
    (r'silver', 'plata'),
    (r'gold', 'dorado'),
    (r'body', 'cuerpo'),
    (r'eyes', 'ojos'),
    (r'tail', 'cola'),
    (r'fins', 'aletas'),
    (r'pattern', 'patrón'),
    (r'stripe', 'raya'),
    (r'spot', 'mancha'),
    (r'spots', 'manchas'),
    
    # Even more phrases
    (r'Predatory snail', 'Caracol depredador'),
    (r'that eats pest snails', 'que come caracoles plaga'),
    (r'pest snails', 'caracoles plaga'),
    (r'Not a shark but', 'No es un tiburón sino'),
    (r'a large cyprinid', 'un gran ciprínido'),
    (r'Often bought small', 'A menudo comprado pequeño'),
    (r'gets massive', 'se vuelve enorme'),
    (r'Round-bodied', 'De cuerpo redondo'),
    (r'molly variant', 'variante de molly'),
    (r'Slower swimmer', 'Nadador más lento'),
    (r'due to', 'debido a'),
    (r'body shape', 'forma del cuerpo'),
    (r'Filter feeding', 'Alimentación por filtro'),
    (r'that fans water', 'que abanica el agua'),
    (r'for particles', 'para partículas'),
    (r'Fascinating behavior', 'Comportamiento fascinante'),
    (r'fascinating', 'fascinante'),
    (r'display to each other', 'se muestran entre sí'),
    (r'harmlessly', 'inofensivamente'),
    (r'larger tetra', 'tetra más grande'),
    (r'Vibrant', 'Vibrante'),
    (r'vibrant', 'vibrante'),
    (r'color variety', 'variedad de color'),
    (r'cherry shrimp', 'gamba cereza'),
    (r'Same easy care', 'Mismo cuidado fácil'),
    (r'Same care', 'Mismo cuidado'),
    (r'easy care', 'cuidado fácil'),
    (r'long fin rays', 'radios de aleta largos'),
    (r'tetra with', 'tetra con'),
    (r'shrimp with', 'gamba con'),
    (r'fish with', 'pez con'),
    (r'with', 'con'),
    (r'brown', 'marrón'),
    (r'larger', 'más grande'),
    (r'smaller', 'más pequeño'),
    (r'longer', 'más largo'),
    (r'shorter', 'más corto'),
    
    # More specific phrases
    (r'two-toned', 'bicolor'),
    (r'rainbow fish', 'pez arcoíris'),
    (r'Blue front half', 'Mitad frontal azul'),
    (r'orange-yellow rear', 'parte trasera naranja-amarilla'),
    (r'front half', 'mitad frontal'),
    (r'rear half', 'mitad trasera'),
    (r'will eat plants', 'comerá plantas'),
    (r'Very adaptable', 'Muy adaptable'),
    (r'adaptable', 'adaptable'),
    (r'can be nippy', 'puede morder'),
    (r'slightly nippy', 'ligeramente mordedor'),
    (r'nippy', 'mordedor'),
    (r'slow tankmates', 'compañeros lentos'),
    (r'tankmates', 'compañeros de tanque'),
    (r'flowing fins', 'aletas fluidas'),
    (r'flowing', 'fluido'),
    
    # Even more phrases
    (r'micro fish', 'micro pez'),
    (r'Perfect for nano tanks', 'Perfecto para nano tanques'),
    (r'Perfect for', 'Perfecto para'),
    (r'nano tanks', 'nano tanques'),
    (r'Primarily eats wood', 'Principalmente come madera'),
    (r'rather than algae', 'en lugar de algas'),
    (r'Gets very large', 'Se vuelve muy grande'),
    (r'despite small sale size', 'a pesar del pequeño tamaño de venta'),
    (r'Not suitable for most tanks', 'No apto para la mayoría de tanques'),
    (r'Not suitable for', 'No apto para'),
    (r'most tanks', 'la mayoría de tanques'),
    (r'that breeds prolifically', 'que se reproduce prolíficamente'),
    (r'breeds prolifically', 'se reproduce prolíficamente'),
    (r'when breeding', 'durante la reproducción'),
    (r'torpedo-shaped', 'en forma de torpedo'),
    (r'needing space', 'necesitando espacio'),
    (r'swimmer', 'nadador'),
    (r'Sparkling scales', 'Escamas brillantes'),
    (r'that shimmer', 'que brillan'),
    (r'like diamonds', 'como diamantes'),
    (r'Adults are truly', 'Los adultos son realmente'),
    (r'King of the aquarium', 'Rey del acuario'),
    (r'disc-shaped', 'en forma de disco'),
    (r'requiring expert care', 'requiriendo cuidado experto'),
    (r'expert care', 'cuidado experto'),
    (r'Tiny', 'Pequeño'),
    (r'tiny', 'pequeño'),
    (r'Small', 'Pequeño'),
    (r'small', 'pequeño'),
    (r'Large', 'Grande'),
    (r'large', 'grande'),
    (r'barb with', 'barbo con'),
    (r'barb', 'barbo'),
    (r'pleco', 'pleco'),
    (r'cichlid', 'cíclido'),
    (r'cichlids', 'cíclidos'),
    (r'rasbora', 'rasbora'),
    
    # Final batch
    (r'Burrowing snail', 'Caracol excavador'),
    (r'that aerates substrate', 'que airea el sustrato'),
    (r'aerates substrate', 'airea el sustrato'),
    (r'substrate', 'sustrato'),
    (r'Flat-bodied', 'De cuerpo plano'),
    (r'Flat-coiled', 'Enrollado plano'),
    (r'loach adapted for', 'locha adaptada para'),
    (r'fast-flowing water', 'agua de flujo rápido'),
    (r'Needs high oxygen', 'Necesita alto oxígeno'),
    (r'high oxygen', 'alto oxígeno'),
    (r'that breed prolifically', 'que se reproducen prolíficamente'),
    (r'Good cleanup crew', 'Buen equipo de limpieza'),
    (r'cleanup crew', 'equipo de limpieza'),
    (r'confused with', 'confundido con'),
    (r'More territorial', 'Más territorial'),
    (r'less effective at', 'menos efectivo en'),
    (r'Pearlescent', 'Perlado'),
    (r'pearlescent', 'perlado'),
    (r'sheen', 'brillo'),
    (r'iridescent', 'iridiscente'),
    (r'danio with', 'danio con'),
    (r'danio', 'danio'),
    (r'cory that swims', 'cory que nada'),
    (r'cory', 'cory'),
    (r'mid-water', 'a media agua'),
    (r'more than other species', 'más que otras especies'),
    (r'other species', 'otras especies'),
    (r'in groups', 'en grupos'),
    (r'loach', 'locha'),
    (r'snail', 'caracol'),
    (r'snails', 'caracoles'),
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
