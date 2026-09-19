#!/usr/bin/env python3
"""Shared SEO/performance helpers for fishfinder.guide.

This module is the single source of truth for the pieces of markup that have to
stay identical between the static HTML already on disk and whatever
generate_fish_pages.py (plus the DE/ES/FR generators) emit next time they run:

  * the pinned, deferred Lucide loader
  * answer-first meta descriptions
  * FAQPage structured data
  * the "compatible tank mates" internal-linking block
  * image loading / alt-text attributes

scripts/seo_optimize.py applies all of it to the existing pages in place;
generate_fish_pages.py imports the same functions so regenerating a page does
not undo the work.
"""

import hashlib
import json
import os
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Lucide: pinned + deferred
# --------------------------------------------------------------------------

LUCIDE_VERSION = "0.544.0"
LUCIDE_SRC = f"https://unpkg.com/lucide@{LUCIDE_VERSION}/dist/umd/lucide.min.js"

# The loader is deferred, so it no longer blocks the parser. Inline callers used
# to run `lucide.createIcons()` during parse, which would now throw because the
# deferred bundle has not executed yet. `renderIcons()` bridges the two: it
# draws immediately when Lucide is already there (dynamically rendered cards)
# and otherwise waits for DOMContentLoaded, which always fires after deferred
# scripts have run.
ICON_HELPER = (
    '<script>function renderIcons(){if(window.lucide){window.lucide.createIcons();}'
    'else{document.addEventListener("DOMContentLoaded",function(){'
    'window.lucide&&window.lucide.createIcons();});}}</script>'
)
LUCIDE_TAG = f'<script src="{LUCIDE_SRC}" defer></script>'

_LUCIDE_SCRIPT_RE = re.compile(
    r'(?:<link rel="preconnect" href="https://unpkg\.com" crossorigin>\s*)?'
    r'(?:<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*)?'
    r'(?:<script>function renderIcons\(\)\{.*?\}</script>\s*)?'
    r'<script src="https://unpkg\.com/lucide[^"]*"[^>]*></script>',
    re.DOTALL,
)
# `window.lucide.createIcons()` inside the helper must survive the rewrite.
_CREATE_ICONS_RE = re.compile(r'(?<!window\.)\blucide\.createIcons\(\)')

# Preconnect to the CDNs the page actually uses, so the deferred bundle and the
# webfont start their handshakes during HTML parse instead of after it.
PRECONNECT_HINTS = [
    '<link rel="preconnect" href="https://unpkg.com" crossorigin>',
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
]


def fix_lucide(html):
    """Pin + defer the Lucide bundle and make every caller defer-safe."""
    if "unpkg.com/lucide" not in html:
        return html

    # Collapse whatever is there (unpinned tag, or an already-processed block)
    # down to the bare pinned tag, then re-add the helper exactly once.
    html = _LUCIDE_SCRIPT_RE.sub(lambda m: LUCIDE_TAG, html)
    html = _CREATE_ICONS_RE.sub("renderIcons()", html)

    prefix = ""
    for hint in PRECONNECT_HINTS:
        if hint not in html:
            prefix += hint + "\n    "
    prefix += ICON_HELPER + "\n"
    html = html.replace(LUCIDE_TAG, prefix + LUCIDE_TAG, 1)
    return html


# --------------------------------------------------------------------------
# Fish data
# --------------------------------------------------------------------------

def load_fish():
    with open(ROOT / "data" / "fish.json", encoding="utf-8") as fh:
        return json.load(fh)


def by_id(fish_list):
    return {f["id"]: f for f in fish_list}


def celsius(f_temp):
    return round((f_temp - 32) * 5 / 9)


def litres(gallons):
    return int(round(gallons * 3.785))


def centimetres(inches, decimal_comma=False):
    """Adult size in cm. DE/ES/FR write decimals with a comma."""
    cm = inches * 2.54
    text = f"{cm:.0f}" if cm >= 10 or abs(cm - round(cm)) < 0.05 else f"{cm:.1f}"
    return text.replace(".", ",") if decimal_comma else text


def inches_text(size):
    """1.0 -> '1 inch', 1.5 -> '1.5 inches'."""
    whole = abs(size - round(size)) < 0.05
    num = f"{round(size)}" if whole else f"{size:g}"
    unit = "inch" if whole and round(size) == 1 else "inches"
    return f"{num} {unit}"


# --------------------------------------------------------------------------
# Answer-first meta descriptions
# --------------------------------------------------------------------------

MAX_DESC = 160

_CARE_EN = {
    "easy": "perfect for beginners",
    "moderate": "best for aquarists with some experience",
    "hard": "an advanced-care species",
}
_CARE_DE = {
    "easy": "ideal für Einsteiger",
    "moderate": "etwas Erfahrung vorausgesetzt",
    "hard": "etwas für Fortgeschrittene",
}
_CARE_ES = {
    "easy": "perfecto para principiantes",
    "moderate": "requiere algo de experiencia",
    "hard": "para acuaristas avanzados",
}
_CARE_FR = {
    "easy": "parfait pour les débutants",
    "moderate": "demande un peu d'expérience",
    "hard": "réservé aux aquariophiles confirmés",
}

_TEMPERAMENT_EN = {
    "peaceful": "peaceful",
    "semi-aggressive": "semi-aggressive",
    "aggressive": "aggressive",
}
_TEMPERAMENT_DE = {
    "peaceful": "friedliche",
    "semi-aggressive": "halbaggressive",
    "aggressive": "aggressive",
}
_TEMPERAMENT_ES = {
    "peaceful": "pacífica",
    "semi-aggressive": "semiagresiva",
    "aggressive": "agresiva",
}
_TEMPERAMENT_FR = {
    "peaceful": "paisible",
    "semi-aggressive": "semi-agressive",
    "aggressive": "agressive",
}


def _assemble(parts, tail_options):
    """Join sentences, then append the longest tail that still fits."""
    head = " ".join(parts)
    for tail in tail_options:
        candidate = f"{head} {tail}".strip()
        if len(candidate) <= MAX_DESC:
            return candidate
    return head[:MAX_DESC].rstrip(" ,.;") + "."


def meta_description(fish, lang="en", name=None):
    """Answer-first, unique-per-fish meta description.

    Leads with the three facts searchers actually ask for (adult size, minimum
    tank, difficulty) instead of the old "Complete X care guide." boilerplate.
    Uniqueness is guaranteed by the name, and reinforced by the numbers.
    """
    name = name or fish["name"]
    tank_g = fish["min_tank_gallons"]
    tank_l = litres(tank_g)
    tmin, tmax = fish["temp_min"], fish["temp_max"]
    cmin, cmax = celsius(tmin), celsius(tmax)
    care = fish["care_level"].lower()
    schooling = fish.get("schooling")
    school = fish.get("school_size") or 6

    if lang == "de":
        parts = [
            f"{name} wird {centimetres(fish['size_inches'], True)} cm groß, "
            f"braucht mindestens {tank_l} Liter und ist {_CARE_DE.get(care, care)}."
        ]
        if schooling:
            parts.append(f"Schwarm ab {school} Tieren bei {cmin}-{cmax} °C.")
        else:
            parts.append(
                f"{_TEMPERAMENT_DE.get(fish['temperament'], fish['temperament']).capitalize()} "
                f"Art bei {cmin}-{cmax} °C."
            )
        tails = [
            "Pflege, Futter, Vergesellschaftung und Zucht im Überblick.",
            "Pflege, Futter und Vergesellschaftung.",
            "Komplette Pflegeanleitung.",
        ]
    elif lang == "es":
        parts = [
            f"{name} mide {centimetres(fish['size_inches'], True)} cm, "
            f"necesita {tank_l} litros y es {_CARE_ES.get(care, care)}."
        ]
        if schooling:
            parts.append(f"Banco de {school}+ ejemplares a {cmin}-{cmax} °C.")
        else:
            parts.append(
                f"Especie {_TEMPERAMENT_ES.get(fish['temperament'], fish['temperament'])} "
                f"a {cmin}-{cmax} °C."
            )
        tails = [
            "Guía completa: agua, alimentación, compañeros y cría.",
            "Guía: agua, alimentación y compañeros.",
            "Guía completa de cuidados.",
        ]
    elif lang == "fr":
        parts = [
            f"{name} atteint {centimetres(fish['size_inches'], True)} cm, "
            f"demande {tank_l} litres et est {_CARE_FR.get(care, care)}."
        ]
        if schooling:
            parts.append(f"Banc de {school}+ individus entre {cmin} et {cmax} °C.")
        else:
            parts.append(
                f"Espèce {_TEMPERAMENT_FR.get(fish['temperament'], fish['temperament'])} "
                f"entre {cmin} et {cmax} °C."
            )
        tails = [
            "Guide complet : eau, alimentation, cohabitation et reproduction.",
            "Guide : eau, alimentation et cohabitation.",
            "Guide d'entretien complet.",
        ]
    else:
        parts = [
            f"{name} grows to {inches_text(fish['size_inches'])}, needs a "
            f"{tank_g}-gallon tank, and is {_CARE_EN.get(care, care)}."
        ]
        if schooling:
            parts.append(f"Keep a school of {school}+ at {tmin}-{tmax}°F.")
        else:
            parts.append(
                f"A {_TEMPERAMENT_EN.get(fish['temperament'], fish['temperament'])} "
                f"species kept at {tmin}-{tmax}°F."
            )
        tails = [
            "Care guide with feeding, tank mates and breeding tips.",
            "Care guide with feeding and tank mates.",
            "Complete care guide.",
        ]

    return _assemble(parts, tails)


# --------------------------------------------------------------------------
# FAQPage structured data
# --------------------------------------------------------------------------

def _esc_json(text):
    return json.dumps(text, ensure_ascii=False)[1:-1]


def faq_entries(fish, lang="en", name=None):
    """Four Q&As built from the care data already shown on the page."""
    name = name or fish["name"]
    tank_g = fish["min_tank_gallons"]
    tank_l = litres(tank_g)
    tmin, tmax = fish["temp_min"], fish["temp_max"]
    cmin, cmax = celsius(tmin), celsius(tmax)
    ph = f"{fish['ph_min']}-{fish['ph_max']}"
    if lang in ("de", "es", "fr"):
        ph = ph.replace(".", ",")
    care = fish["care_level"].lower()
    size_in = inches_text(fish["size_inches"])
    size_cm = centimetres(fish["size_inches"], lang in ("de", "es", "fr"))
    life = fish["lifespan_years"]
    diet = fish["diet"].lower()
    tips = fish.get("care_tips", "").strip()
    school = fish.get("school_size") or 6
    schooling = fish.get("schooling")

    if lang == "de":
        school_txt = f" Haltung im Schwarm ab {school} Tieren." if schooling else ""
        return [
            (f"Wie groß muss das Becken für {name} sein?",
             f"{name} braucht mindestens {tank_l} Liter ({tank_g} Gallonen).{school_txt}"),
            (f"Welche Wasserwerte braucht {name}?",
             f"{name} fühlt sich bei {cmin}-{cmax} °C und einem pH-Wert von {ph} wohl."),
            (f"Ist {name} für Anfänger geeignet?",
             f"Der Pflegeaufwand gilt als {_CARE_DE.get(care, care)}. "
             f"Die Art wird etwa {life} Jahre alt und gilt als "
             f"{_TEMPERAMENT_DE.get(fish['temperament'], fish['temperament'])} Art."),
            (f"Wie groß wird {name} und was frisst er?",
             f"{name} wird bis zu {size_cm} cm groß. {tips}"),
        ]
    if lang == "es":
        school_txt = f" Manténlos en bancos de {school} o más." if schooling else ""
        return [
            (f"¿Qué tamaño de acuario necesita el {name}?",
             f"El {name} necesita un mínimo de {tank_l} litros ({tank_g} galones).{school_txt}"),
            (f"¿Qué parámetros de agua necesita el {name}?",
             f"El {name} prospera entre {cmin} y {cmax} °C con un pH de {ph}."),
            (f"¿Es fácil de cuidar el {name}?",
             f"Su cuidado se considera {_CARE_ES.get(care, care)}. "
             f"Vive unos {life} años y es una especie "
             f"{_TEMPERAMENT_ES.get(fish['temperament'], fish['temperament'])}."),
            (f"¿Cuánto mide y qué come el {name}?",
             f"El {name} alcanza unos {size_cm} cm. {tips}"),
        ]
    if lang == "fr":
        school_txt = f" À maintenir en banc de {school} individus minimum." if schooling else ""
        return [
            (f"Quelle taille d'aquarium faut-il pour le {name} ?",
             f"Le {name} demande au minimum {tank_l} litres ({tank_g} gallons).{school_txt}"),
            (f"Quels paramètres d'eau pour le {name} ?",
             f"Le {name} se plaît entre {cmin} et {cmax} °C avec un pH de {ph}."),
            (f"Le {name} est-il facile à maintenir ?",
             f"Son entretien est {_CARE_FR.get(care, care)}. "
             f"Il vit environ {life} ans et c'est une espèce "
             f"{_TEMPERAMENT_FR.get(fish['temperament'], fish['temperament'])}."),
            (f"Quelle taille atteint le {name} et que mange-t-il ?",
             f"Le {name} atteint environ {size_cm} cm. {tips}"),
        ]

    school_txt = f" They should be kept in schools of at least {school}." if schooling else ""
    return [
        (f"What size tank does a {name} need?",
         f"A {name} needs a minimum tank size of {tank_g} gallons ({tank_l} litres).{school_txt}"),
        (f"What water parameters does a {name} need?",
         f"{name} thrive in water between {tmin}-{tmax}°F ({cmin}-{cmax}°C) with a pH of {ph}."),
        (f"Are {name} easy to care for?",
         f"{name} are considered {care} to care for. They are {fish['temperament']} fish "
         f"with a lifespan of about {life} years."),
        (f"How big do {name} get and what do they eat?",
         f"{name} reach about {size_in} and are {diet}s. {tips}"),
    ]


def faq_schema(fish, lang="en", name=None, indent="    "):
    entries = faq_entries(fish, lang=lang, name=name)
    questions = ",\n".join(
        f'''        {{
            "@type": "Question",
            "name": "{_esc_json(q)}",
            "acceptedAnswer": {{
                "@type": "Answer",
                "text": "{_esc_json(a)}"
            }}
        }}''' for q, a in entries
    )
    return f'''<!-- FAQ Schema -->
{indent}<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{questions}
    ]
}}
{indent}</script>'''


# --------------------------------------------------------------------------
# Visible FAQ block (matches the FAQPage markup above)
# --------------------------------------------------------------------------

_FAQ_HEADING = {
    "en": "Frequently Asked Questions",
    "de": "Häufige Fragen",
    "es": "Preguntas frecuentes",
    "fr": "Questions fréquentes",
}

FAQ_MARKER = "<!-- fishfinder:faq -->"


def faq_section(fish, lang="en", name=None):
    entries = faq_entries(fish, lang=lang, name=name)
    items = "\n".join(
        f'''            <div class="border-b border-slate-100 last:border-0 pb-4 last:pb-0">
                <h3 class="font-semibold text-slate-900 mb-1">{_html_escape(q)}</h3>
                <p class="text-slate-600">{_html_escape(a)}</p>
            </div>''' for q, a in entries
    )
    return f'''{FAQ_MARKER}
    <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
        <h2 class="text-xl font-bold text-slate-900 mb-6">{_FAQ_HEADING.get(lang, _FAQ_HEADING["en"])}</h2>
        <div class="space-y-4">
{items}
        </div>
    </section>'''


def _html_escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------------------------------------------------------------------------
# Internal linking: computed tank mates + related species
# --------------------------------------------------------------------------

CATEGORY_PLURALS = {
    "barb": ["barbs", "barb"],
    "catfish": ["catfish", "corydoras", "corys", "plecos", "pleco"],
    "cichlid": ["cichlids", "cichlid"],
    "danio": ["danios", "danio"],
    "killifish": ["killifish", "killis"],
    "labyrinth": ["gouramis", "gourami", "bettas", "betta"],
    "livebearer": ["livebearers", "guppies", "mollies", "platies", "swordtails"],
    "loach": ["loaches", "loach"],
    "rainbowfish": ["rainbowfish", "rainbows"],
    "rasbora": ["rasboras", "rasbora"],
    "shrimp": ["shrimp", "shrimps"],
    "snail": ["snails", "snail"],
    "tetra": ["tetras", "tetra"],
}

FIN_NIPPERS = {"tiger-barb", "serpae-tetra", "buenos-aires-tetra", "black-skirt-tetra",
               "red-eye-tetra", "rosy-barb", "odessa-barb"}
LONG_FINNED = {"betta-fish", "angelfish", "guppy", "sailfin-molly", "balloon-molly",
               "longfin-zebra-danio", "swordtail", "moonlight-gourami", "pearl-gourami"}


def _descriptor_matches(term, fish):
    """Does a free-text avoid_with/compatible_with term describe this fish?"""
    t = term.lower().strip()
    size = fish["size_inches"]
    temperament = fish["temperament"].lower()

    if "fin nipper" in t:
        return fish["id"] in FIN_NIPPERS
    if "long-finned" in t or "long finned" in t:
        return fish["id"] in LONG_FINNED
    if "aggressive" in t:
        if not (temperament == "aggressive" or
                (temperament == "semi-aggressive" and "very" not in t)):
            return False
    if "large" in t or "larger" in t:
        if size < 6:
            return False
    if "small" in t or "micro" in t or "very small" in t:
        if size > 2.5:
            return False
    if "slow" in t and fish["id"] not in LONG_FINNED and temperament != "peaceful":
        return False
    if "peaceful" in t and temperament != "peaceful":
        return False
    if "cold water" in t and fish["temp_min"] > 68:
        return False
    if "goldfish" in t or "puffer" in t or "plant" in t or "substrate" in t or "water quality" in t:
        return False

    # A category word anywhere in the term makes it apply to that category.
    for plural in CATEGORY_PLURALS.get(fish["category"], []):
        if re.search(rf"\b{re.escape(plural)}\b", t):
            return True
    # Bare descriptors with no category word ("large fish", "aggressive fish").
    if re.search(r"\bfish\b", t) and any(
        w in t for w in ("large", "larger", "small", "aggressive", "peaceful", "slow",
                         "robust", "fast", "community", "micro", "bottom", "warm")
    ):
        return True
    # Direct name match, e.g. "cardinal tetras", "otocinclus".
    stem = fish["name"].lower().rstrip("s")
    return stem and (stem in t or fish["id"].replace("-", " ") in t)


def _avoids(a, b):
    return any(_descriptor_matches(term, b) for term in a.get("avoid_with", []))


def _overlap(lo1, hi1, lo2, hi2):
    return min(hi1, hi2) - max(lo1, lo2)


def tank_mates(fish, all_fish, limit=4):
    """Pick genuinely compatible species from the dataset.

    Requires overlapping temperature and pH ranges, mutually non-hostile
    temperaments, a tank the pair can realistically share, and that neither
    fish's avoid_with list describes the other.
    """
    candidates = []
    for other in all_fish:
        if other["id"] == fish["id"]:
            continue
        if _avoids(fish, other) or _avoids(other, fish):
            continue

        temp_overlap = _overlap(fish["temp_min"], fish["temp_max"],
                                other["temp_min"], other["temp_max"])
        ph_overlap = _overlap(fish["ph_min"], fish["ph_max"],
                              other["ph_min"], other["ph_max"])
        if temp_overlap < 4 or ph_overlap < 0.3:
            continue

        a_temp, b_temp = fish["temperament"].lower(), other["temperament"].lower()
        if a_temp == "peaceful" and b_temp == "aggressive":
            continue
        if b_temp == "peaceful" and a_temp == "aggressive":
            continue
        # Don't put bite-sized fish in with something much bigger.
        if other["size_inches"] * 2.5 < fish["size_inches"] and a_temp != "peaceful":
            continue
        if fish["size_inches"] * 2.5 < other["size_inches"] and b_temp != "peaceful":
            continue
        # The pair has to fit a tank the reader is plausibly already planning.
        if other["min_tank_gallons"] > fish["min_tank_gallons"] * 1.5 + 5:
            continue

        score = 0.0
        for term in fish.get("compatible_with", []):
            if _descriptor_matches(term, other):
                score += 3
        for term in other.get("compatible_with", []):
            if _descriptor_matches(term, fish):
                score += 3
        if other["care_level"] == fish["care_level"]:
            score += 2
        if b_temp == a_temp:
            score += 1
        if other["category"] != fish["category"]:
            score += 1.5  # variety beats six more tetras
        score += min(temp_overlap, 10) / 10
        score += min(ph_overlap, 2)

        candidates.append((score, other))

    candidates.sort(key=lambda pair: (-pair[0], pair[1]["name"]))

    picked, seen_categories = [], {}
    for score, other in candidates:
        cat = other["category"]
        if seen_categories.get(cat, 0) >= 2:
            continue
        seen_categories[cat] = seen_categories.get(cat, 0) + 1
        picked.append(other)
        if len(picked) == limit:
            break
    return picked


def similar_care(fish, all_fish, exclude_ids=(), limit=3):
    """Fish at the same difficulty and a comparable tank size."""
    exclude = set(exclude_ids) | {fish["id"]}
    scored = []
    for other in all_fish:
        if other["id"] in exclude or other["care_level"] != fish["care_level"]:
            continue
        if other["category"] == fish["category"]:
            continue
        # Same difficulty is not the same as compatible, but readers will read
        # it that way, so keep mutually hostile pairings out of the list.
        if _avoids(fish, other) or _avoids(other, fish):
            continue
        gap = abs(other["min_tank_gallons"] - fish["min_tank_gallons"])
        if gap > max(10, fish["min_tank_gallons"] * 0.5):
            continue
        scored.append((gap, other["name"], other))
    scored.sort(key=lambda t: (t[0], t[1]))
    return [other for _, _, other in scored[:limit]]


TANKMATE_MARKER = "<!-- fishfinder:tankmates -->"

_TANKMATE_STRINGS = {
    "en": {
        "heading": "Tank Mates for {name}",
        "lede": "Species from our database with overlapping water parameters, "
                "compatible temperaments and a realistic shared tank size.",
        "similar": "Similar Care Level",
        "similar_lede": "Other {care}-care species that suit a comparable setup.",
        "browse": "Browse all {category} species",
    },
    "de": {
        "heading": "Mitbewohner für {name}",
        "lede": "Arten aus unserer Datenbank mit passenden Wasserwerten, "
                "verträglichem Verhalten und realistischer Beckengröße.",
        "similar": "Ähnlicher Pflegeaufwand",
        "similar_lede": "Weitere Arten mit vergleichbarem Aufwand und Becken.",
        "browse": "Alle Arten ansehen",
    },
    "es": {
        "heading": "Compañeros de acuario para {name}",
        "lede": "Especies de nuestra base de datos con parámetros de agua "
                "compatibles, buen carácter y un acuario compartido realista.",
        "similar": "Nivel de cuidado similar",
        "similar_lede": "Otras especies con un nivel de cuidado y acuario parecidos.",
        "browse": "Ver todas las especies",
    },
    "fr": {
        "heading": "Colocataires pour {name}",
        "lede": "Espèces de notre base aux paramètres d'eau compatibles, "
                "au tempérament compatible et au volume réaliste.",
        "similar": "Niveau d'entretien similaire",
        "similar_lede": "D'autres espèces au niveau d'entretien et au volume comparables.",
        "browse": "Voir toutes les espèces",
    },
}

_CARE_LABEL = {
    "en": {"easy": "easy", "moderate": "moderate", "hard": "advanced"},
    "de": {"easy": "einfach", "moderate": "mittel", "hard": "anspruchsvoll"},
    "es": {"easy": "fácil", "moderate": "medio", "hard": "avanzado"},
    "fr": {"easy": "facile", "moderate": "moyen", "hard": "avancé"},
}

_LOCALE_FISH_PATH = {
    "en": "/fish/{id}/",
    "de": "/de/fische/{id}/",
    "es": "/es/peces/{id}/",
    "fr": "/fr/poissons/{id}/",
}
_LOCALE_SEARCH_PATH = {
    "en": "/search/",
    "de": "/de/suche/",
    "es": "/es/buscar/",
    "fr": "/fr/rechercher/",
}


def fish_url(fish_id, lang="en"):
    return _LOCALE_FISH_PATH.get(lang, _LOCALE_FISH_PATH["en"]).format(id=fish_id)


def search_url(lang="en", query=""):
    return _LOCALE_SEARCH_PATH.get(lang, _LOCALE_SEARCH_PATH["en"]) + query


def _fish_card(other, lang, image_dims, names=None):
    url = fish_url(other["id"], lang)
    label = (names or {}).get(other["id"], other["name"])
    w, h = image_dims.get(other["id"], (1536, 1024))
    care = _CARE_LABEL.get(lang, _CARE_LABEL["en"]).get(
        other["care_level"].lower(), other["care_level"])
    tank = (f'{litres(other["min_tank_gallons"])} L' if lang != "en"
            else f'{other["min_tank_gallons"]}+ gal')
    alt = image_alt(other, lang, label)
    return f'''            <a href="{url}" class="group flex gap-3 items-center bg-white rounded-xl border border-slate-200 p-3 hover:shadow-md hover:border-cyan-300 transition">
                <img src="/images/fish/{other["id"]}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async" class="w-14 h-14 rounded-lg object-cover bg-slate-100 shrink-0">
                <span class="min-w-0">
                    <span class="block font-semibold text-slate-900 truncate">{_html_escape(label)}</span>
                    <span class="block text-xs text-slate-500 italic truncate">{_html_escape(other["scientific"])}</span>
                    <span class="block text-xs text-slate-500 mt-1">{care} · {tank}</span>
                </span>
            </a>'''


def tankmate_section(fish, all_fish, lang="en", name=None, image_dims=None, names=None):
    """Internal-linking block: real tank mates + same-difficulty species.

    `names` maps fish id -> the name that locale's page actually uses for it,
    so a Spanish card links to /es/peces/... under its Spanish name.
    """
    image_dims = image_dims or {}
    name = name or fish["name"]
    strings = _TANKMATE_STRINGS.get(lang, _TANKMATE_STRINGS["en"])

    mates = tank_mates(fish, all_fish)
    if not mates:
        return ""
    similar = similar_care(fish, all_fish, exclude_ids=[m["id"] for m in mates])

    mate_cards = "\n".join(_fish_card(m, lang, image_dims, names) for m in mates)
    block = f'''{TANKMATE_MARKER}
    <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
        <h2 class="text-xl font-bold text-slate-900 mb-2">{_html_escape(strings["heading"].format(name=name))}</h2>
        <p class="text-slate-600 mb-6">{_html_escape(strings["lede"])}</p>
        <div class="grid sm:grid-cols-2 gap-3">
{mate_cards}
        </div>'''

    if similar:
        care_word = _CARE_LABEL.get(lang, _CARE_LABEL["en"]).get(
            fish["care_level"].lower(), fish["care_level"])
        similar_cards = "\n".join(_fish_card(s, lang, image_dims, names) for s in similar)
        block += f'''
        <h3 class="text-lg font-bold text-slate-900 mt-8 mb-2">{_html_escape(strings["similar"])}</h3>
        <p class="text-slate-600 mb-4">{_html_escape(strings["similar_lede"].format(care=care_word))}</p>
        <div class="grid sm:grid-cols-2 gap-3">
{similar_cards}
        </div>'''

    browse = strings["browse"].format(category=fish["category"])
    block += f'''
        <p class="mt-6">
            <a href="{search_url(lang, f'?category={fish["category"]}')}" class="inline-flex items-center gap-2 text-cyan-700 font-semibold hover:text-cyan-800">
                {_html_escape(browse)}
                <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </a>
        </p>
    </section>'''
    return block


# --------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------

_ALT_TEMPLATE = {
    "en": "{name} ({scientific}) in a planted freshwater aquarium",
    "de": "{name} ({scientific}) im bepflanzten Süßwasseraquarium",
    "es": "{name} ({scientific}) en un acuario de agua dulce plantado",
    "fr": "{name} ({scientific}) dans un aquarium d'eau douce planté",
}


def image_alt(fish, lang="en", name=None):
    name = name or fish["name"]
    scientific = fish["scientific"]
    template = _ALT_TEMPLATE.get(lang, _ALT_TEMPLATE["en"])
    if name.strip().lower() == scientific.strip().lower():
        # Some locales use the scientific name as the common name; don't
        # print it twice.
        template = template.replace(" ({scientific})", "")
    return template.format(name=name, scientific=scientific).replace('"', "&quot;")


def webp_dimensions(path):
    """Read intrinsic width/height from a .webp without a decoder dependency."""
    try:
        data = open(path, "rb").read(64)
    except OSError:
        return None
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    fourcc = data[12:16]
    try:
        if fourcc == b"VP8 ":
            w = struct.unpack("<H", data[26:28])[0] & 0x3FFF
            h = struct.unpack("<H", data[28:30])[0] & 0x3FFF
            return w, h
        if fourcc == b"VP8L":
            bits = struct.unpack("<I", data[21:25])[0]
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if fourcc == b"VP8X":
            w = data[24] | data[25] << 8 | data[26] << 16
            h = data[27] | data[28] << 8 | data[29] << 16
            return w + 1, h + 1
    except (struct.error, IndexError):
        return None
    return None


def load_image_dims():
    dims = {}
    image_dir = ROOT / "images" / "fish"
    if not image_dir.is_dir():
        return dims
    for entry in os.listdir(image_dir):
        if entry.endswith(".webp"):
            size = webp_dimensions(image_dir / entry)
            if size:
                dims[entry[:-5]] = size
    return dims


_IMG_RE = re.compile(
    r"""<img(?:\s+[\w:.-]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*\s*/?>""",
    re.IGNORECASE,
)
_SRC_RE = re.compile(r'src="([^"]*)"')
_ATTR_RE = re.compile(r'\s(\w[\w-]*)=')


def _slug_from_src(src):
    match = re.search(r"/([a-z0-9-]+)\.webp", src)
    return match.group(1) if match else None


def fix_images(html, fish_index, lang="en", image_dims=None, hero_slug=None, names=None):
    """Add loading/decoding/dimensions and upgrade alt text to something descriptive.

    The hero image on a fish page is the LCP element, so it stays eager and gets
    fetchpriority="high"; everything else becomes lazy.
    """
    image_dims = image_dims or {}

    def replace(match):
        tag = match.group(0)
        src_match = _SRC_RE.search(tag)
        if not src_match:
            return tag
        src = src_match.group(1)
        if "${" in src:  # JS template literal inside an inline script
            return tag

        slug = _slug_from_src(src)
        fish = fish_index.get(slug) if slug else None
        attrs = set(_ATTR_RE.findall(tag))
        is_hero = slug is not None and slug == hero_slug and "object-contain" in tag and "w-full" in tag

        additions = []
        if "loading" not in attrs:
            additions.append('loading="eager"' if is_hero else 'loading="lazy"')
        if "decoding" not in attrs:
            additions.append('decoding="async"')
        if is_hero and "fetchpriority" not in attrs:
            additions.append('fetchpriority="high"')
        if slug in image_dims and "width" not in attrs and "height" not in attrs:
            w, h = image_dims[slug]
            additions.append(f'width="{w}" height="{h}"')

        if additions:
            tag = tag[:-1].rstrip() + " " + " ".join(additions) + ">"

        if fish is not None:
            alt = image_alt(fish, lang, (names or {}).get(fish["id"]))
            tag = re.sub(r'alt="[^"]*"', f'alt="{alt}"', tag, count=1)
        return tag

    return _IMG_RE.sub(replace, html)


# --------------------------------------------------------------------------
# Cache-busting for the prebuilt stylesheet
# --------------------------------------------------------------------------

_CSS_HREF_RE = re.compile(r'(href=")(/css/tailwind\.css)(?:\?v=[0-9a-f]+)?(")')


def css_version():
    """Short content hash of the built stylesheet."""
    path = ROOT / "css" / "tailwind.css"
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def version_css_link(html, version):
    """Stamp /css/tailwind.css with its content hash.

    The stylesheet is rebuilt whenever new utility classes appear in the
    markup, and it ships from the same URL every time, so without this a
    returning visitor can get new HTML against a cached old stylesheet.
    """
    if not version:
        return html
    return _CSS_HREF_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}?v={version}{m.group(3)}", html)
