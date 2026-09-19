#!/usr/bin/env python3
"""Build the /articles/ section.

Run from the repo root:  python3 scripts/build_articles.py

Articles defined here are rendered through scripts/article_template.py and
written to articles/<slug>/index.html, and the articles index is rebuilt to
list every article (hand-written ones included).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import article_template as T
import seo_lib as S
from article_template import (bullets, callout, cards, esc, fish_link, p,
                              species_table, steps, stocking_plan, table)

ROOT = S.ROOT
UPDATED = "September 2026"
TODAY = "2026-09-19"


# --------------------------------------------------------------------------
# Articles already published by hand. Listed so the new ones can link to them
# and so the index page can be rebuilt from one source.
# --------------------------------------------------------------------------

EXISTING = [
    {
        "slug": "aquarium-cycling-guide",
        "kicker": "Beginner's Guide",
        "card_title": "How to Cycle an Aquarium",
        "card_blurb": "The nitrogen cycle, fishless cycling, and how to tell "
                      "when a tank is ready for fish.",
        "read_time": "10 min read",
        "featured": True,
    },
    {
        "slug": "best-fish-for-beginners",
        "kicker": "Species Guide",
        "card_title": "15 Best Fish for Beginners",
        "card_blurb": "Hardy, forgiving species that survive the mistakes "
                      "every first-time fishkeeper makes.",
        "read_time": "12 min read",
    },
    {
        "slug": "10-gallon-stocking-ideas",
        "kicker": "Stocking Guide",
        "card_title": "10 Gallon Tank Stocking Ideas",
        "card_blurb": "Eight complete combinations for a 10 gallon (38 L) "
                      "tank, with exact numbers.",
        "read_time": "9 min read",
    },
]


# --------------------------------------------------------------------------
# New articles
# --------------------------------------------------------------------------

def _water_parameters():
    return {
        "slug": "aquarium-water-parameters",
        "kicker": "Water Chemistry",
        "icon": "droplets",
        "title": "Aquarium Water Parameters: The Numbers That Actually Matter (2026)",
        "h1": "Aquarium Water Parameters: The Numbers That Actually Matter",
        "card_title": "Aquarium Water Parameters",
        "card_blurb": "Which numbers to test, what the targets are, and how to "
                      "pick fish that suit the water you already have.",
        "description": "Ammonia, nitrite, nitrate, pH, hardness and temperature "
                       "targets for a freshwater tank — plus which species suit "
                       "soft, hard, cool or warm water.",
        "lede": "Six numbers describe almost everything about your water. Three "
                "of them must stay at a fixed value forever; the other three "
                "just need to stay <em>stable</em> and suit your fish.",
        "read_time": "11 min read",
        "toc": [
            ("test-what", "What to test, and how often"),
            ("waste", "Ammonia, nitrite and nitrate"),
            ("ph", "pH: stability beats perfection"),
            ("hardness", "Hardness (GH and KH)"),
            ("temperature", "Temperature"),
            ("match-fish", "Match the fish to your water"),
        ],
        "sections": [
            {
                "id": "test-what",
                "h2": "What to Test, and How Often",
                "html": (
                    p("You need six readings. Three are pollution measurements "
                      "that tell you whether the tank is safe. Three describe "
                      "the water itself and tell you which fish belong in it.") +
                    table(
                        ["Reading", "Target", "How often"],
                        [["Ammonia (NH<sub>3</sub>)", "<strong>0 ppm</strong>",
                          "Weekly, and daily in a new tank"],
                         ["Nitrite (NO<sub>2</sub><sup>-</sup>)", "<strong>0 ppm</strong>",
                          "Weekly, and daily in a new tank"],
                         ["Nitrate (NO<sub>3</sub><sup>-</sup>)", "Under 20-40 ppm",
                          "Weekly"],
                         ["pH", "Stable, anywhere your fish tolerate", "Weekly"],
                         ["GH (general hardness)", "Matched to your species", "Once, then after water source changes"],
                         ["KH (carbonate hardness)", "3+ dKH to hold pH steady", "Monthly"]],
                        note="Temperature is the seventh, and the one you set "
                             "rather than measure — see below.") +
                    callout("warn", "Test strips give you the wrong answer",
                            "Strips drift badly with age and humidity, and they "
                            "are least accurate exactly where it matters: near "
                            "zero. A liquid reagent kit costs more once and "
                            "lasts hundreds of tests.")
                ),
            },
            {
                "id": "waste",
                "h2": "Ammonia, Nitrite and Nitrate",
                "html": (
                    p("Fish excrete ammonia, and uneaten food and dead plant "
                      "matter release more. In a cycled tank, bacteria convert "
                      "it in two steps.") +
                    cards([
                        ("💀", "Ammonia", "Toxic at any detectable level. Burns "
                         "gills and skin. Must read <strong>0</strong>.", "red"),
                        ("⚠️", "Nitrite", "Also toxic — it stops blood carrying "
                         "oxygen. Must read <strong>0</strong>.", "orange"),
                        ("✅", "Nitrate", "The safe end product. Removed by water "
                         "changes and living plants.", "green"),
                    ]) +
                    p("Any reading above zero for ammonia or nitrite is an "
                      "emergency: change 50% of the water with dechlorinated "
                      "water matched for temperature, stop feeding for a day, "
                      "and find the cause. Usually it is a tank stocked before "
                      "it finished cycling, a filter that was cleaned too "
                      "thoroughly, or a dead fish behind a decoration.") +
                    p("Nitrate is different. It accumulates steadily and is "
                      "your cue for water changes. If nitrate sits above 40 ppm "
                      "you are either overstocked, overfeeding, or changing "
                      "water too rarely — in that order of likelihood.") +
                    callout("note", "Nitrate is also a tap-water problem",
                            "In some areas tap water arrives at 20-40 ppm "
                            "nitrate on its own. Test your tap before blaming "
                            "the tank; if it is high, water changes alone will "
                            "not bring the number down.")
                ),
            },
            {
                "id": "ph",
                "h2": "pH: Stability Beats Perfection",
                "html": (
                    p("pH measures how acidic or alkaline the water is, on a "
                      "logarithmic scale — pH 6 is ten times more acidic than "
                      "pH 7. Almost every commonly sold freshwater fish is "
                      "farm-bred and adapts to a wide range, so the number "
                      "itself matters far less than whether it moves.") +
                    p("A tank that sits at a steady pH 7.8 will keep fish that "
                      "'want' pH 6.5 perfectly healthy. A tank that swings "
                      "between 6.5 and 7.8 every week will not.") +
                    bullets([
                        "Chasing a number with pH-adjusting chemicals is the "
                        "most common way beginners <em>cause</em> a swing. Don't.",
                        "Low KH is the real culprit behind unstable pH. If KH "
                        "is under about 3 dKH, the water has little buffering "
                        "and pH will drop as the tank ages.",
                        "Driftwood, peat and botanicals lower pH slowly and "
                        "gently; crushed coral and aragonite raise it. Both "
                        "are safer than bottled adjusters.",
                    ]) +
                    p("The species with the narrowest tolerance in our database "
                      "are the soft-water specialists: " +
                      fish_link("chili-rasbora") + " and " +
                      fish_link("phoenix-rasbora") + " go down to pH 4.0, while "
                      + fish_link("peacock-cichlid") + " starts at pH 7.8. "
                      "Those two groups genuinely cannot share a tank.")
                ),
            },
            {
                "id": "hardness",
                "h2": "Hardness (GH and KH)",
                "html": (
                    p("GH is the amount of calcium and magnesium in the water. "
                      "KH is the amount of carbonate, which resists pH change. "
                      "Your water company publishes both, usually as "
                      "'water hardness' in mg/L CaCO<sub>3</sub>; divide by "
                      "17.9 to get degrees (dGH/dKH).") +
                    table(
                        ["Water", "GH", "Suits"],
                        [["Soft", "0-6 dGH",
                          "Tetras, rasboras, dwarf cichlids, most wild-caught species"],
                         ["Medium", "6-12 dGH",
                          "Almost everything sold in shops; the easiest range to keep"],
                         ["Hard", "12+ dGH",
                          "Livebearers, rift-lake cichlids, snails and shrimp"]]) +
                    callout("win", "Hard water is not a problem, it's a filter",
                            "Hard water keeps " + fish_link("molly") + ", " +
                            fish_link("guppy") + ", " + fish_link("swordtail") +
                            " and every snail in better condition than soft "
                            "water does — snail and shrimp shells need the "
                            "calcium. Pick fish that want what comes out of "
                            "your tap and you will never fight your water again.")
                ),
            },
            {
                "id": "temperature",
                "h2": "Temperature",
                "html": (
                    p("Temperature drives metabolism, oxygen levels and disease "
                      "resistance. Warmer water holds less oxygen and speeds "
                      "everything up, including the progress of an infection.") +
                    p("Most tropical community fish are comfortable at "
                      "24-26°C (75-79°F). The exceptions matter, because a "
                      "heater set for one group is lethal over time for the "
                      "other:") +
                    species_table([
                        "white-cloud-mountain-minnow", "peppered-cory",
                        "hillstream-loach", "gold-barb", "zebra-danio",
                        "german-blue-ram", "kuhli-loach", "discus",
                    ], note="The first five are subtropical and are slowly "
                            "worn out by a heated tropical tank. The last three "
                            "need the top of the range.") +
                    callout("warn", "\"Warm water fish\" is a real incompatibility",
                            "A " + fish_link("white-cloud-mountain-minnow") +
                            " tops out at 22°C (72°F). A " +
                            fish_link("german-blue-ram") + " starts at 26°C "
                            "(78°F). There is no temperature that suits both, "
                            "however peaceful they are.")
                ),
            },
            {
                "id": "match-fish",
                "h2": "Match the Fish to Your Water",
                "html": (
                    p("The shortcut that saves the most trouble: test your tap "
                      "water once for GH, KH and pH, then choose species that "
                      "already live in those conditions. Every species page on "
                      "this site lists its temperature and pH range, and the "
                      "browser lets you filter by them.") +
                    steps([
                        ("Test your tap, not your tank",
                         "Fill a glass, let it stand overnight to let gases "
                         "equalise, then test pH, GH and KH."),
                        ("Write down the range",
                         "For example: pH 7.6, 10 dGH, 6 dKH — moderately hard, "
                         "slightly alkaline, well buffered."),
                        ("Shortlist species that overlap it",
                         'Use the <a href="/search/" class="text-cyan-600 '
                         'font-medium hover:underline">species browser</a> and '
                         "keep anything whose pH range includes your number."),
                        ("Check the shortlist against each other",
                         'Run the combination through the <a href="/compatibility/" '
                         'class="text-cyan-600 font-medium hover:underline">'
                         "compatibility checker</a> before you buy."),
                    ])
                ),
            },
        ],
        "faq": [
            ("What are the ideal water parameters for a freshwater aquarium?",
             "Ammonia 0 ppm, nitrite 0 ppm, nitrate under 20-40 ppm, KH at "
             "least 3 dKH, and a pH and temperature that stay stable within "
             "the range your species tolerate. Most community tropical fish "
             "are comfortable at 24-26°C (75-79°F)."),
            ("Should I use chemicals to adjust my aquarium pH?",
             "Usually not. pH adjusters wear off between doses and create the "
             "swings that actually harm fish. If your pH is unstable, raise KH "
             "instead; if it is simply not the number you wanted, choose fish "
             "that suit it."),
            ("How often should I test aquarium water?",
             "Weekly for an established tank, and daily for ammonia and nitrite "
             "while a new tank is cycling or after adding a group of fish. Use "
             "a liquid reagent kit rather than test strips."),
            ("What nitrate level is too high?",
             "Above 40 ppm is a sign the tank needs more frequent or larger "
             "water changes, less food, or fewer fish. Sensitive species such "
             "as discus and shrimp do better kept under 20 ppm."),
        ],
        "cta": {
            "heading": "Find fish that suit your water",
            "text": "Filter the species database by temperature, pH and tank "
                    "size instead of guessing at the shop.",
            "buttons": [("/search/", "Browse Species", "search"),
                        ("/quiz/", "Take the Quiz", "target")],
        },
        "related": ["aquarium-cycling-guide", "fish-tank-mates-guide"],
    }


def _how_many_fish():
    return {
        "slug": "how-many-fish-in-a-tank",
        "kicker": "Stocking Guide",
        "icon": "scale",
        "title": "How Many Fish Can I Put in My Tank? A Practical Stocking Guide (2026)",
        "h1": "How Many Fish Can I Put in My Tank?",
        "card_title": "How Many Fish in a Tank?",
        "card_blurb": "Why the inch-per-gallon rule fails, and what to use "
                      "instead when planning a stocking list.",
        "description": "The inch-per-gallon rule gets tanks overstocked. Here's "
                       "how to plan stocking by adult size, bioload, swimming "
                       "level and school size — with worked examples.",
        "lede": "The old \"one inch of fish per gallon\" rule has killed more "
                "fish than almost any other piece of aquarium advice. Here is "
                "what experienced keepers use instead.",
        "read_time": "10 min read",
        "toc": [
            ("why-rule-fails", "Why the inch-per-gallon rule fails"),
            ("four-questions", "The four questions that actually decide it"),
            ("by-tank-size", "Realistic stocking by tank size"),
            ("worked-example", "A worked example"),
            ("adding-fish", "Adding fish without crashing the cycle"),
            ("overstocked", "Signs a tank is overstocked"),
        ],
        "sections": [
            {
                "id": "why-rule-fails",
                "h2": "Why the Inch-Per-Gallon Rule Fails",
                "html": (
                    p("The rule says a 20 gallon tank holds 20 inches of fish. "
                      "It fails for three reasons, and each one is enough on "
                      "its own.") +
                    cards([
                        ("📏", "Fish aren't lines",
                         "A 10 inch " + fish_link("oscar") + " has many times "
                         "the mass — and waste output — of ten 1 inch "
                         + fish_link("chili-rasbora") + ". Length scales badly.",
                         "red"),
                        ("🫧", "Waste isn't proportional",
                         "A messy eater like a pleco produces far more waste "
                         "per inch than a small schooling fish. Diet matters "
                         "as much as size.", "orange"),
                        ("🏊", "Behaviour isn't counted",
                         "A territorial cichlid needs floor area, not volume. "
                         "A schooling tetra needs company. Neither shows up in "
                         "an inch count.", "cyan"),
                    ]) +
                    callout("stop", "The rule's worst outcome",
                            "Applied literally, it says a 30 gallon tank can "
                            "hold a 30 inch fish. It cannot — a fish that size "
                            "cannot even turn around.")
                ),
            },
            {
                "id": "four-questions",
                "h2": "The Four Questions That Actually Decide It",
                "html": (
                    steps([
                        ("What is the adult size?",
                         "Not the shop size. A " + fish_link("common-pleco") +
                         " is sold at 5 cm and reaches 45 cm. Every species "
                         "page on this site lists adult size and the minimum "
                         "tank that follows from it."),
                        ("Does the species need a group?",
                         "Schooling fish kept in twos and threes are stressed, "
                         "pale and short-lived. If a species needs six, six is "
                         "the smallest unit you can stock — plan around that "
                         "number, not around single fish."),
                        ("Which level does it swim at?",
                         "Top, middle and bottom dwellers barely compete. A "
                         "tank with a school mid-water, a group of corydoras "
                         "on the floor and a gourami at the surface feels "
                         "far less crowded than the same fish count all in "
                         "one layer."),
                        ("Can your filter and your routine keep up?",
                         "Stocking is a question about waste, not space. A "
                         "heavily planted tank with an oversized filter and "
                         "weekly water changes supports more than a bare tank "
                         "with a stock filter and monthly changes."),
                    ]) +
                    callout("note", "The honest version of the rule",
                            "Start with the minimum tank size for the largest "
                            "species you want, add its group, then fill the "
                            "remaining swimming levels with smaller species — "
                            "and stop one group earlier than you think you "
                            "should.")
                ),
            },
            {
                "id": "by-tank-size",
                "h2": "Realistic Stocking by Tank Size",
                "html": (
                    p("These are conservative, well-tested ceilings for a "
                      "filtered, cycled, moderately planted tank with weekly "
                      "water changes.") +
                    table(
                        ["Tank", "Realistic stocking", "Example"],
                        [["5 gal / 19 L",
                          "One centrepiece fish <em>or</em> one nano school, plus invertebrates",
                          "1 " + fish_link("betta-fish") + " + 6 "
                          + fish_link("cherry-shrimp")],
                         ["10 gal / 38 L",
                          "One school of 6-8 small fish plus a small bottom group",
                          "8 " + fish_link("neon-tetra") + " + 6 "
                          + fish_link("pygmy-cory")],
                         ["20 gal / 76 L",
                          "Two schools plus a centrepiece or a cleanup crew",
                          "8 " + fish_link("harlequin-rasbora") + " + 6 "
                          + fish_link("bronze-cory") + " + 1 "
                          + fish_link("honey-gourami")],
                         ["29-30 gal / 110 L",
                          "Three groups, or one medium centrepiece species",
                          "A " + fish_link("kribensis") + " pair plus two "
                          "mid-water schools"],
                         ["55 gal / 208 L",
                          "A community of four or five groups, or one large species",
                          "A " + fish_link("discus") + " group, or a mixed "
                          "tetra and corydoras community"],
                         ["75+ gal / 284+ L",
                          "Large cichlids, or a big-school display",
                          "1 " + fish_link("oscar") + ", or 30+ "
                          + fish_link("rummy-nose-tetra")]]) +
                    callout("warn", "Tank shape matters as much as volume",
                            "Two tanks can hold 20 gallons and suit completely "
                            "different fish. Footprint — length × width — is "
                            "what territorial and bottom-dwelling fish "
                            "actually use. A tall, narrow 20 gallon is a poor "
                            "home for corydoras and a fine one for angelfish.")
                ),
            },
            {
                "id": "worked-example",
                "h2": "A Worked Example",
                "html": (
                    p("Planning a 20 gallon (76 L) community, step by step.") +
                    steps([
                        ("Pick the centrepiece first",
                         "One " + fish_link("honey-gourami") + " — 5 cm adult, "
                         "peaceful, occupies the top third of the tank. That "
                         "sets the temperature and pH window for everything "
                         "else."),
                        ("Add the mid-water school",
                         "8 " + fish_link("harlequin-rasbora") + ". They need "
                         "at least eight, share the gourami's water "
                         "parameters, and are too large to be eaten."),
                        ("Add the bottom group",
                         "6 " + fish_link("bronze-cory") + ". Different level, "
                         "different food, no competition with the other two."),
                        ("Stop, and check",
                         "That is 15 fish and roughly 60% of what the tank "
                         "could technically hold. The remaining headroom is "
                         "what absorbs a missed water change, a growth spurt "
                         "or a batch of fry."),
                    ]) +
                    callout("win", "Leave headroom on purpose",
                            "An aquarium stocked to its theoretical limit has "
                            "no margin. The same tank at two-thirds capacity "
                            "tolerates a holiday, a filter failure or an "
                            "unexpected spawn without a crisis.")
                ),
            },
            {
                "id": "adding-fish",
                "h2": "Adding Fish Without Crashing the Cycle",
                "html": (
                    p("Your bacteria colony is sized to the waste it currently "
                      "processes. Double the bioload overnight and ammonia "
                      "appears before the colony can catch up.") +
                    bullets([
                        "Add one group at a time, and wait two weeks between "
                        "groups.",
                        "Test ammonia and nitrite daily for the first week "
                        "after each addition.",
                        "Add the largest or messiest species last, when the "
                        "filter is most established.",
                        "Never add fish in the week before you go away.",
                    ]) +
                    p('If ammonia or nitrite appears, treat it as described in '
                      'the <a href="/articles/aquarium-cycling-guide/" '
                      'class="text-cyan-600 font-medium hover:underline">'
                      'cycling guide</a>: large water change, stop feeding, '
                      'find the cause.')
                ),
            },
            {
                "id": "overstocked",
                "h2": "Signs a Tank Is Overstocked",
                "html": (
                    p("Overstocking rarely announces itself. It shows up as a "
                      "tank that is slightly harder to keep than it should be.") +
                    bullets([
                        "Nitrate climbs back above 40 ppm within a week of a "
                        "water change.",
                        "Fish gather near the surface or the filter outflow, "
                        "gasping — a sign of low oxygen.",
                        "Algae returns faster than you can remove it despite "
                        "modest lighting.",
                        "Fins are nipped, or one fish is constantly chased.",
                        "You need to clean the filter more than once a month "
                        "to keep the flow up.",
                    ]) +
                    callout("note", "The fix is rarely a bigger filter",
                            "A bigger filter processes waste faster but does "
                            "not create swimming space or reduce aggression. "
                            "If the tank is crowded, rehome a group or upgrade "
                            "the tank.")
                ),
            },
        ],
        "faq": [
            ("How many fish can I put in a 10 gallon tank?",
             "One school of six to eight small fish under 4 cm, plus a small "
             "bottom-dwelling group or a few invertebrates. For example eight "
             "neon tetras and six pygmy corydoras. A 10 gallon tank is too "
             "small for any fish that exceeds about 5 cm as an adult."),
            ("Is the one inch per gallon rule accurate?",
             "No. It ignores body mass, waste output, territory and school "
             "size, and it breaks down completely for large fish — it would "
             "suggest a 30 inch fish fits a 30 gallon tank. Plan around adult "
             "size, group requirements and swimming level instead."),
            ("How long should I wait between adding fish?",
             "About two weeks per group. That gives the filter bacteria time "
             "to grow into the extra waste, and it lets you spot disease in "
             "one new group before adding another."),
            ("Can I keep just one schooling fish?",
             "No. Schooling species such as tetras, rasboras, danios and "
             "corydoras are stressed when kept below their group size — "
             "usually six. They hide, lose colour and die early. Stock them in "
             "full groups or choose a species that lives alone."),
        ],
        "cta": {
            "heading": "Check your stocking list before you buy",
            "text": "Add the species you're considering and see whether they "
                    "actually work together.",
            "buttons": [("/compatibility/", "Compatibility Checker", "check-circle"),
                        ("/setups/", "Browse Ready-Made Setups", "layout-grid")],
        },
        "related": ["10-gallon-stocking-ideas", "20-gallon-stocking-ideas"],
    }


def _twenty_gallon():
    return {
        "slug": "20-gallon-stocking-ideas",
        "kicker": "Stocking Guide",
        "icon": "layout-grid",
        "title": "20 Gallon Tank Stocking Ideas: 7 Complete Combinations (2026)",
        "h1": "20 Gallon Tank Stocking Ideas: 7 Complete Combinations",
        "card_title": "20 Gallon Stocking Ideas",
        "card_blurb": "Seven full stocking lists for a 20 gallon (76 L) tank, "
                      "with exact numbers and why each one works.",
        "description": "Seven complete stocking plans for a 20 gallon (76 L) "
                       "aquarium — community, species-only, soft water, hard "
                       "water and cool water — with exact fish counts.",
        "lede": "A 20 gallon tank is the first size where you can build a real "
                "community: two or three groups at different levels, with room "
                "to spare. Here are seven combinations that work.",
        "read_time": "10 min read",
        "toc": [
            ("why-20", "Why 20 gallons is the sweet spot"),
            ("ground-rules", "Ground rules for all seven"),
            ("plans", "The seven stocking plans"),
            ("avoid", "What not to put in a 20 gallon"),
        ],
        "sections": [
            {
                "id": "why-20",
                "h2": "Why 20 Gallons Is the Sweet Spot",
                "html": (
                    p("Twenty gallons (76 litres) is where fishkeeping gets "
                      "easier rather than harder. The extra water dilutes "
                      "mistakes, the temperature is more stable, and the "
                      "footprint — typically 60 × 30 cm — is finally enough "
                      "for a proper school plus a bottom group.") +
                    bullets([
                        "Water parameters move slowly, so a missed water "
                        "change is not a crisis.",
                        "There is room for two or three distinct groups "
                        "instead of one.",
                        "Most dwarf cichlids become possible for the first "
                        "time.",
                        "Standard 20 gallon tanks, hoods, lights and filters "
                        "are cheap and widely available.",
                    ])
                ),
            },
            {
                "id": "ground-rules",
                "h2": "Ground Rules for All Seven",
                "html": (
                    p("Each plan below assumes the tank is fully cycled, "
                      "filtered, and gets a 25% water change weekly. Stock one "
                      "group at a time, two weeks apart.") +
                    callout("warn", "Check the temperature column",
                            "Every plan keeps all its species inside one "
                            "temperature and pH window. Swapping a species "
                            "between plans usually breaks that — check the "
                            "ranges on each species page first.")
                ),
            },
            {
                "id": "plans",
                "h2": "The Seven Stocking Plans",
                "html": (
                    stocking_plan(
                        "1. The classic community", "20 gal / 76 L · 24-26°C · pH 6.5-7.5",
                        [(8, "harlequin-rasbora"), (6, "bronze-cory"), (1, "honey-gourami")],
                        "Three levels, three temperaments, no overlap. The "
                        "gourami holds the surface, the rasboras the middle, "
                        "the corydoras the floor. The most forgiving plan here.") +
                    stocking_plan(
                        "2. Soft-water blackwater", "20 gal / 76 L · 25-27°C · pH 5.5-7.0",
                        [(10, "cardinal-tetra"), (6, "sterbai-cory"), (1, "apistogramma-borellii")],
                        "Built for naturally soft water, with driftwood and "
                        "leaf litter. The dwarf cichlid pairs off and claims a "
                        "cave; the cardinals stay high and out of its way.") +
                    stocking_plan(
                        "3. Hard-water livebearers", "20 gal / 76 L · 24-26°C · pH 7.5-8.5",
                        [(6, "guppy"), (4, "platy"), (4, "nerite-snail")],
                        "If your tap water is hard, this is the plan that "
                        "stops fighting it. Keep two or three females per male "
                        "to spread out breeding attention — and expect fry.") +
                    stocking_plan(
                        "4. Cool water, no heater", "20 gal / 76 L · 18-22°C · pH 6.5-7.5",
                        [(10, "white-cloud-mountain-minnow"), (6, "peppered-cory"),
                         (1, "hillstream-loach")],
                        "A genuinely unheated tank for a cool room. All three "
                        "species are subtropical and are shortened by tropical "
                        "temperatures rather than helped by them.") +
                    stocking_plan(
                        "5. The planted nano school", "20 gal / 76 L · 24-26°C · pH 6.0-7.5",
                        [(12, "chili-rasbora"), (8, "cherry-shrimp"), (6, "otocinclus")],
                        "Everything here is under 5 cm, which makes the tank "
                        "look far larger than it is. Needs dense planting and "
                        "an established tank — otocinclus starve in a new one.") +
                    stocking_plan(
                        "6. Centrepiece cichlid pair", "20 gal / 76 L · 25-27°C · pH 6.0-7.5",
                        [(2, "kribensis"), (8, "lemon-tetra")],
                        "A kribensis pair is the most rewarding fish you can "
                        "keep in this size. The tetras are dither fish — their "
                        "calm swimming tells the cichlids no predator is "
                        "around. Expect the pair to claim the bottom when "
                        "breeding.") +
                    stocking_plan(
                        "7. Species-only betta community", "20 gal / 76 L · 25-27°C · pH 6.5-7.5",
                        [(1, "betta-fish"), (8, "lambchop-rasbora"), (6, "pygmy-cory")],
                        "A betta in 20 gallons has room to avoid tankmates, "
                        "which is what makes this work where a 5 gallon "
                        "version does not. Choose a short-finned betta and "
                        "avoid anything brightly coloured or long-finned.") +
                    callout("note", "Counts are minimums, not maximums",
                            "Where a plan says eight, eight is the smallest "
                            "group that keeps the fish comfortable. Adding a "
                            "few more of the same species is almost always "
                            "better than adding a different species.")
                ),
            },
            {
                "id": "avoid",
                "h2": "What Not to Put in a 20 Gallon",
                "html": (
                    p("These are the species most often sold for tanks this "
                      "size and most often outgrow them.") +
                    species_table([
                        "common-pleco", "bala-shark", "clown-loach",
                        "oscar", "tinfoil-barb", "red-tailed-shark",
                    ], note="Every one of these is commonly sold at 5-8 cm. "
                            "The minimum tank column is what they actually "
                            "need as adults.") +
                    callout("stop", "Goldfish are not a 20 gallon fish either",
                            "A single fancy goldfish needs about 75 litres to "
                            "itself and produces far more waste than any "
                            "tropical fish of the same length. Common goldfish "
                            "belong in ponds.")
                ),
            },
        ],
        "faq": [
            ("How many fish can a 20 gallon tank hold?",
             "Typically two or three groups — for example eight small "
             "mid-water schooling fish, six bottom-dwelling corydoras and one "
             "centrepiece fish, around 15 fish in total. The limit depends on "
             "adult size and waste output, not fish count alone."),
            ("What is the best community setup for a 20 gallon tank?",
             "Eight harlequin rasboras, six bronze corydoras and one honey "
             "gourami. The three species occupy different levels, share the "
             "same water parameters and are all peaceful and beginner-friendly."),
            ("Can I keep a betta in a 20 gallon community tank?",
             "Yes, and it works better than a smaller tank because the betta "
             "can avoid its tankmates. Choose a short-finned betta, keep it "
             "with small peaceful species such as rasboras and corydoras, and "
             "avoid brightly coloured or long-finned fish it might mistake for "
             "a rival."),
            ("Do I need a heater for a 20 gallon tank?",
             "For most tropical species, yes. The cool-water plan above is the "
             "exception: white clouds, peppered corydoras and hillstream "
             "loaches are subtropical and do best at 18-22°C without a heater, "
             "provided the room stays in that range."),
        ],
        "cta": {
            "heading": "Build your own 20 gallon plan",
            "text": "Pick the species you like and check them against each "
                    "other before you buy.",
            "buttons": [("/compatibility/", "Compatibility Checker", "check-circle"),
                        ("/search/?tank_size=20", "Browse 20 Gallon Species", "search")],
        },
        "related": ["10-gallon-stocking-ideas", "how-many-fish-in-a-tank"],
    }


def _algae():
    return {
        "slug": "aquarium-algae-control",
        "kicker": "Maintenance",
        "icon": "sparkles",
        "title": "Aquarium Algae: How to Identify It and Actually Get Rid of It (2026)",
        "h1": "Aquarium Algae: How to Identify It and Get Rid of It",
        "card_title": "Aquarium Algae Control",
        "card_blurb": "Identify the algae you have, fix the cause, and pick "
                      "the cleanup crew that eats that particular type.",
        "description": "Identify green spot, hair, diatom, black beard and blue-"
                       "green algae, fix the underlying cause, and choose "
                       "algae eaters that actually eat the type you have.",
        "lede": "Algae is not a cleanliness problem — it is a symptom. Every "
                "type tells you something specific about light, nutrients or "
                "circulation, and the fix is different for each.",
        "read_time": "9 min read",
        "toc": [
            ("why", "Why algae appears"),
            ("identify", "Identify what you have"),
            ("fix", "Fix the cause first"),
            ("crew", "Choosing a cleanup crew"),
            ("mistakes", "What doesn't work"),
        ],
        "sections": [
            {
                "id": "why",
                "h2": "Why Algae Appears",
                "html": (
                    p("Algae grows when light and nutrients are available and "
                      "nothing else is using them. That is why a new tank, a "
                      "tank by a window, and an overfed tank all get algae for "
                      "what looks like the same reason but isn't.") +
                    cards([
                        ("💡", "Too much light",
                         "More than 8 hours a day, or direct sun. The single "
                         "most common cause.", "orange"),
                        ("🍽️", "Excess nutrients",
                         "Overfeeding and infrequent water changes leave "
                         "nitrate and phosphate for algae to use.", "red"),
                        ("🌱", "No competition",
                         "Growing plants outcompete algae for the same "
                         "nutrients. A bare tank has no competitor.", "green"),
                    ]) +
                    callout("note", "New tanks get algae. That's normal.",
                            "Almost every tank goes through a brown diatom "
                            "phase in its first two months while the biology "
                            "settles. It passes on its own.")
                ),
            },
            {
                "id": "identify",
                "h2": "Identify What You Have",
                "html": (
                    table(
                        ["Looks like", "Type", "What it's telling you"],
                        [["Brown dust on glass and plants, wipes off easily",
                          "<strong>Diatoms</strong>",
                          "A new tank finding its balance, or silicates in the "
                          "water. Usually resolves in weeks."],
                         ["Hard green dots on the glass, needs a blade",
                          "<strong>Green spot algae</strong>",
                          "Light is high and phosphate is low. Common in "
                          "planted tanks."],
                         ["Soft green threads on plants and decor",
                          "<strong>Hair / thread algae</strong>",
                          "Too much light for the nutrients available. Often "
                          "follows a lighting upgrade."],
                         ["Dark tufts on leaf edges and hardscape, very tough",
                          "<strong>Black beard algae</strong>",
                          "Unstable CO<sub>2</sub> and poor circulation. The "
                          "hardest type to remove."],
                         ["Green water, tank looks like pea soup",
                          "<strong>Free-floating algae</strong>",
                          "An ammonia spike plus strong light. Water changes "
                          "alone make it worse."],
                         ["Blue-green slimy sheets, smells earthy",
                          "<strong>Cyanobacteria</strong>",
                          "Not algae at all — a bacterium. Low flow and "
                          "organic build-up in the substrate."]]) +
                    callout("warn", "Cyanobacteria is the one to act on quickly",
                            "It spreads across the substrate in days, "
                            "suffocates plants, and no fish or shrimp will eat "
                            "it. Improve flow, siphon it out physically, and "
                            "blackout the tank for three days.")
                ),
            },
            {
                "id": "fix",
                "h2": "Fix the Cause First",
                "html": (
                    p("Adding algae eaters to a tank whose lighting is wrong "
                      "just gives you hungry fish and the same algae. Work "
                      "through these in order.") +
                    steps([
                        ("Cut the photoperiod to 6-8 hours",
                         "Use a timer. Consistency matters more than "
                         "duration — a fixed 7 hours beats a variable 5 to 10."),
                        ("Move the tank out of direct sunlight",
                         "Even an hour of direct sun a day will outgrow "
                         "anything you do to the light fixture."),
                        ("Feed less",
                         "Feed what the fish finish in about a minute, once a "
                         "day. Uneaten food is pure algae fertiliser."),
                        ("Change water on schedule",
                         "25% weekly removes the nitrate and phosphate algae "
                         "depends on."),
                        ("Add fast-growing plants",
                         "Floating plants and stem plants consume the same "
                         "nutrients and shade the tank at the same time. The "
                         "most effective long-term fix there is."),
                        ("Only then, add a cleanup crew",
                         "With the cause addressed, algae eaters keep the "
                         "remaining growth in check instead of fighting a "
                         "losing battle."),
                    ])
                ),
            },
            {
                "id": "crew",
                "h2": "Choosing a Cleanup Crew",
                "html": (
                    p("Algae eaters are specialists. Pick the one that eats "
                      "the type you actually have, and check it fits your "
                      "tank.") +
                    species_table([
                        "otocinclus", "amano-shrimp", "nerite-snail",
                        "siamese-algae-eater", "pleco-bristlenose",
                        "cherry-shrimp", "rubber-lip-pleco",
                    ]) +
                    bullets([
                        fish_link("otocinclus") + " — soft green film and "
                        "diatoms on leaves. Needs an established tank with "
                        "existing algae, and a group of at least six.",
                        fish_link("amano-shrimp") + " — hair algae, the best "
                        "in the trade at it. Effective from about five "
                        "individuals.",
                        fish_link("nerite-snail") + " — green spot algae on "
                        "glass, which almost nothing else will touch. Lays "
                        "harmless white eggs that won't hatch in freshwater.",
                        fish_link("siamese-algae-eater") + " — one of the very "
                        "few animals that eats black beard algae, but it "
                        "reaches 15 cm and needs a 30 gallon tank.",
                        fish_link("pleco-bristlenose") + " — general green film "
                        "on glass and wood. Stays at 12 cm, unlike the common "
                        "pleco it is often confused with.",
                    ]) +
                    callout("stop", "The two to avoid",
                            "The " + fish_link("common-pleco") + " is sold as "
                            "an algae eater and reaches 45 cm, at which point "
                            "it stops eating algae and produces enormous "
                            "amounts of waste. Chinese algae eaters become "
                            "aggressive and start rasping at other fish.")
                ),
            },
            {
                "id": "mistakes",
                "h2": "What Doesn't Work",
                "html": (
                    bullets([
                        "<strong>Turning the lights off entirely for weeks.</strong> "
                        "It kills your plants first, which removes the only "
                        "real competitor algae has. A three-day blackout for "
                        "cyanobacteria is the exception.",
                        "<strong>Algaecides as a first resort.</strong> They "
                        "kill algae faster than the tank can process the dead "
                        "matter, causing an ammonia spike, and many are toxic "
                        "to shrimp and snails.",
                        "<strong>Scrubbing everything weekly.</strong> Physical "
                        "removal helps, but if the cause is untouched the "
                        "algae returns in days and you have only stressed the "
                        "tank.",
                        "<strong>Replacing all the water at once.</strong> A "
                        "large sudden change shocks fish and can restart the "
                        "cycle without touching the underlying nutrient load.",
                    ]) +
                    callout("win", "The realistic goal",
                            "A completely algae-free aquarium is not the "
                            "target and is not achievable. A tank with a "
                            "little algae on the back glass and none on the "
                            "plants is a healthy, normal aquarium.")
                ),
            },
        ],
        "faq": [
            ("How do I get rid of algae in my aquarium?",
             "Reduce lighting to 6-8 hours a day on a timer, move the tank out "
             "of direct sunlight, feed less, change 25% of the water weekly, "
             "and add fast-growing plants. Add algae eaters such as otocinclus, "
             "amano shrimp or nerite snails only after the cause is addressed."),
            ("What is the best algae eater for a freshwater tank?",
             "It depends on the algae. Nerite snails handle green spot algae on "
             "glass, amano shrimp handle hair algae, otocinclus handle soft "
             "green film on plants, and siamese algae eaters are one of the few "
             "species that eat black beard algae."),
            ("Why does my new aquarium have brown algae?",
             "Brown dust on the glass and plants is diatoms, and almost every "
             "new tank gets it in the first two months while the biology "
             "settles. It usually disappears on its own; otocinclus and nerite "
             "snails will clear it faster."),
            ("Is blue-green algae dangerous?",
             "Blue-green algae is cyanobacteria, not algae. It spreads quickly, "
             "smothers plants and has a distinctive earthy smell, and no fish "
             "or invertebrate will eat it. Increase water flow, siphon it out "
             "physically and black the tank out for three days."),
        ],
        "cta": {
            "heading": "Find the right cleanup crew",
            "text": "Check any algae eater against the fish you already keep "
                    "before adding it.",
            "buttons": [("/compatibility/", "Compatibility Checker", "check-circle"),
                        ("/search/?category=shrimp", "Browse Invertebrates", "search")],
        },
        "related": ["aquarium-water-parameters", "aquarium-cycling-guide"],
    }


def _tank_mates():
    return {
        "slug": "fish-tank-mates-guide",
        "kicker": "Compatibility",
        "icon": "users",
        "title": "How to Choose Aquarium Tank Mates That Actually Get Along (2026)",
        "h1": "How to Choose Tank Mates That Actually Get Along",
        "card_title": "Choosing Tank Mates",
        "card_blurb": "The five checks that decide whether two species can "
                      "share a tank — in the order that matters.",
        "description": "Water parameters, adult size, temperament, swimming "
                       "level and group size — the five checks that decide "
                       "whether two aquarium species can live together.",
        "lede": "Most compatibility failures are not fights. They are slow "
                "mismatches — a temperature one species tolerates and the other "
                "is worn down by, or a fish that grew large enough to swallow "
                "its neighbour.",
        "read_time": "9 min read",
        "toc": [
            ("five-checks", "The five checks, in order"),
            ("parameters", "1. Water parameters must overlap"),
            ("size", "2. Adult size, not shop size"),
            ("temperament", "3. Temperament and fin nipping"),
            ("levels", "4. Swimming levels and territory"),
            ("groups", "5. Group sizes"),
            ("combos", "Combinations that reliably fail"),
        ],
        "sections": [
            {
                "id": "five-checks",
                "h2": "The Five Checks, in Order",
                "html": (
                    p("Run every candidate pairing through these in sequence. "
                      "If a pair fails an early check, nothing later can "
                      "rescue it.") +
                    bullets([
                        "<strong>Water parameters</strong> — temperature and pH "
                        "ranges must genuinely overlap.",
                        "<strong>Adult size</strong> — if one fits in the "
                        "other's mouth, it eventually will be.",
                        "<strong>Temperament</strong> — aggression, fin nipping "
                        "and speed at feeding time.",
                        "<strong>Swimming level</strong> — crowding is about "
                        "the layer fish share, not the tank volume.",
                        "<strong>Group size</strong> — a schooling fish in the "
                        "wrong numbers behaves like a different species.",
                    ]) +
                    callout("note", "This is the order the site uses",
                            "The tank mate suggestions on every species page "
                            "are computed with exactly these rules: "
                            "overlapping temperature and pH ranges, compatible "
                            "temperaments, a tank the pair can realistically "
                            "share, and neither species in the other's "
                            "incompatible list.")
                ),
            },
            {
                "id": "parameters",
                "h2": "1. Water Parameters Must Overlap",
                "html": (
                    p("This is the check people skip, because two peaceful "
                      "fish look like they should get along. Temperature is "
                      "the usual dealbreaker.") +
                    species_table(["white-cloud-mountain-minnow", "german-blue-ram",
                                   "peppered-cory", "discus"],
                                  note="A white cloud stops at 22°C and a ram "
                                       "starts at 26°C. There is no setting "
                                       "that suits both.") +
                    p("A useful rule: the overlap needs to be at least 2-3°C "
                      "wide, not just touching at one end. Fish kept at the "
                      "extreme edge of their range are permanently stressed "
                      "even though nothing looks wrong.") +
                    callout("warn", "\"Tolerates\" is not \"thrives in\"",
                            "Published ranges are survival ranges. A fish "
                            "living at the last degree of its tolerance has no "
                            "reserve left for disease or a heater failure.")
                ),
            },
            {
                "id": "size",
                "h2": "2. Adult Size, Not Shop Size",
                "html": (
                    p("Fish are sold as juveniles. An " + fish_link("oscar") +
                      " is sold at 5 cm and reaches 35 cm; an "
                      + fish_link("angelfish") + " is sold the size of a coin "
                      "and reaches 15 cm tall, at which point neon tetras "
                      "become food.") +
                    p("The working rule is the mouth test: if the smaller fish "
                      "fits in the larger one's mouth at adult size, it will "
                      "eventually be eaten — regardless of how peaceful the "
                      "larger species is described as being.") +
                    bullets([
                        "Look up adult size before buying, not after.",
                        "Assume roughly a 3:1 size ratio is the maximum for "
                        "peaceful species sharing a tank.",
                        "Remember that predation is not aggression. A peaceful "
                        "angelfish eating a neon tetra is behaving normally.",
                    ])
                ),
            },
            {
                "id": "temperament",
                "h2": "3. Temperament and Fin Nipping",
                "html": (
                    p("Three distinct problems get filed under 'aggression', "
                      "and they need different solutions.") +
                    cards([
                        ("⚔️", "Territorial aggression",
                         "Cichlids defending a breeding site. Fixed by "
                         "footprint, line of sight breaks and hiding places.",
                         "red"),
                        ("✂️", "Fin nipping",
                         "Barbs and some tetras nipping trailing fins. Fixed "
                         "by larger groups — a school of ten nips each other "
                         "instead.", "orange"),
                        ("🍽️", "Feeding competition",
                         "Fast fish stripping the tank before slow ones eat. "
                         "Fixed by feeding in two places and using sinking "
                         "food.", "cyan"),
                    ]) +
                    p("Long-finned fish are the usual victims. A "
                      + fish_link("betta-fish") + ", "
                      + fish_link("guppy") + " or "
                      + fish_link("sailfin-molly") + " should not share a tank "
                      "with " + fish_link("tiger-barb") + " or "
                      + fish_link("serpae-tetra") + ", both of which are "
                      "persistent nippers.")
                ),
            },
            {
                "id": "levels",
                "h2": "4. Swimming Levels and Territory",
                "html": (
                    p("Fish do not use a tank evenly. Stocking across three "
                      "layers rather than one is the difference between a tank "
                      "that looks full and one that feels crowded to its "
                      "occupants.") +
                    table(
                        ["Level", "Typical species", "What they need"],
                        [["Top", "Gouramis, hatchetfish, killifish",
                          "Surface access, floating plants, a lid"],
                         ["Middle", "Tetras, rasboras, danios, barbs",
                          "Open swimming length, especially for danios"],
                         ["Bottom", "Corydoras, loaches, plecos",
                          "Soft sand or smooth gravel, and floor area"]]) +
                    callout("warn", "Substrate matters for bottom dwellers",
                            "Corydoras and kuhli loaches sift substrate with "
                            "delicate barbels. Sharp gravel wears the barbels "
                            "away and leads to infection — sand or smooth, "
                            "rounded gravel only.")
                ),
            },
            {
                "id": "groups",
                "h2": "5. Group Sizes",
                "html": (
                    p("A schooling fish kept alone or in pairs is not a "
                      "smaller version of a school — it is a stressed animal. "
                      "It hides, loses colour, eats poorly, and in nippy "
                      "species it redirects that behaviour onto its tank "
                      "mates.") +
                    bullets([
                        "Six is the practical minimum for most schooling "
                        "species; ten is noticeably better.",
                        "Tiny species such as " + fish_link("chili-rasbora") +
                        " want ten or more before they behave naturally.",
                        "Nipping species such as " + fish_link("tiger-barb") +
                        " become far less trouble in groups of eight or more, "
                        "because the behaviour stays within the group.",
                        "Plan stocking in whole groups. Six corydoras is one "
                        "stocking decision, not six.",
                    ])
                ),
            },
            {
                "id": "combos",
                "h2": "Combinations That Reliably Fail",
                "html": (
                    table(
                        ["Combination", "Why it fails"],
                        [["Betta + guppies",
                          "The betta reads bright, long-finned males as rival "
                          "bettas."],
                         ["Tiger barbs + any long-finned fish",
                          "Persistent fin nipping, even in adequate groups."],
                         ["Angelfish + neon tetras",
                          "Fine for months, then the angelfish is large enough "
                          "to eat them."],
                         ["Goldfish + tropical fish",
                          "Goldfish want 18-22°C; tropical species want 24-27°C."],
                         ["Shrimp + most cichlids",
                          "Shrimp are food. Only the smallest, most peaceful "
                          "dwarf cichlids are an exception."],
                         ["African rift-lake cichlids + South American cichlids",
                          "Incompatible hardness and pH, and very different "
                          "aggression styles."],
                         ["Two male bettas",
                          "They will fight until one dies. This is not "
                          "avoidable with tank size or decor."]]) +
                    p('Every species page on this site lists both its computed '
                      'tank mates and the groups to avoid. For a specific '
                      'combination, the <a href="/compatibility/" '
                      'class="text-cyan-600 font-medium hover:underline">'
                      'compatibility checker</a> will test a whole stocking '
                      'list at once.')
                ),
            },
        ],
        "faq": [
            ("How do I know if two fish are compatible?",
             "Check five things in order: their temperature and pH ranges must "
             "overlap by at least 2-3°C, neither should fit in the other's "
             "mouth at adult size, their temperaments must match, they should "
             "prefer different swimming levels, and each must be kept in its "
             "own required group size."),
            ("Can a betta live with other fish?",
             "Often, in a tank of 20 gallons or more with small, peaceful, "
             "short-finned species such as rasboras and corydoras. Avoid "
             "brightly coloured or long-finned fish such as guppies, which a "
             "betta may attack as rivals, and never keep two males together."),
            ("Why is my peaceful fish eating its tank mates?",
             "Because predation is not aggression. Any fish will eat something "
             "that fits in its mouth, so a peaceful species that grows large — "
             "an angelfish, for instance — will eventually eat neon tetras it "
             "lived alongside as a juvenile."),
            ("How many fish make a school?",
             "Six is the practical minimum for most schooling species and ten "
             "is better. Very small species such as chili rasboras need ten or "
             "more before they school naturally, and nippy species such as "
             "tiger barbs are much better behaved in groups of eight or more."),
        ],
        "cta": {
            "heading": "Test your combination",
            "text": "Add every species you're planning and check the whole "
                    "list at once.",
            "buttons": [("/compatibility/", "Compatibility Checker", "check-circle"),
                        ("/search/", "Browse Species", "search")],
        },
        "related": ["how-many-fish-in-a-tank", "aquarium-water-parameters"],
    }


def _five_gallon():
    return {
        "slug": "5-gallon-tank-stocking",
        "kicker": "Stocking Guide",
        "icon": "box",
        "title": "5 Gallon Tank Stocking: What Actually Works in a Nano Aquarium (2026)",
        "h1": "5 Gallon Tank Stocking: What Actually Works",
        "card_title": "5 Gallon Tank Stocking",
        "card_blurb": "Honest options for a 5 gallon (19 L) nano tank, and the "
                      "popular choices that don't belong in one.",
        "description": "Realistic stocking for a 5 gallon (19 L) aquarium: five "
                       "workable setups, the species that fit, and the popular "
                       "choices that need a bigger tank.",
        "lede": "A 5 gallon tank is a real aquarium, not a starter toy — but it "
                "is unforgiving. Small water volumes swing fast, so the stocking "
                "has to be modest and the maintenance consistent.",
        "read_time": "8 min read",
        "toc": [
            ("reality", "The reality of nano tanks"),
            ("what-fits", "What actually fits"),
            ("setups", "Five setups that work"),
            ("not-suitable", "What doesn't belong in 5 gallons"),
            ("maintenance", "Maintenance is the trade-off"),
        ],
        "sections": [
            {
                "id": "reality",
                "h2": "The Reality of Nano Tanks",
                "html": (
                    p("Nineteen litres of water dilutes nothing. An ammonia "
                      "spike that a 200 litre tank absorbs unnoticed becomes "
                      "lethal here in a day, and a room that warms by 3°C "
                      "takes the tank with it.") +
                    bullets([
                        "Parameters change quickly, so testing and water "
                        "changes matter more, not less.",
                        "A heater and a gentle filter are not optional.",
                        "One fish dying unnoticed can foul the whole tank.",
                        "Stocking has essentially no headroom — plan it once "
                        "and stick to it.",
                    ]) +
                    callout("win", "The upside is real too",
                            "A 5 gallon tank costs little to plant heavily, "
                            "water changes take five minutes, and a densely "
                            "planted nano with one small species is genuinely "
                            "beautiful. It is a good tank for someone who "
                            "wants to do one thing carefully.")
                ),
            },
            {
                "id": "what-fits",
                "h2": "What Actually Fits",
                "html": (
                    p("These are the species in our database whose minimum "
                      "tank size is 5 gallons or less.") +
                    species_table([
                        "betta-fish", "chili-rasbora", "phoenix-rasbora",
                        "cherry-shrimp", "blue-velvet-shrimp", "least-killifish",
                        "clown-killifish", "nerite-snail", "ramshorn-snail",
                        "malaysian-trumpet-snail",
                    ], note="Note the group sizes: most of these are schooling "
                            "species, so the group — not the individual — is "
                            "the unit you stock.") +
                    callout("note", "One species, done properly",
                            "The most successful 5 gallon tanks hold a single "
                            "species plus a cleanup crew. There is not enough "
                            "water for two groups to have separate territories.")
                ),
            },
            {
                "id": "setups",
                "h2": "Five Setups That Work",
                "html": (
                    stocking_plan(
                        "1. The betta tank", "5 gal / 19 L · 25-27°C · pH 6.5-7.5",
                        [(1, "betta-fish"), (1, "nerite-snail")],
                        "The classic, and it works — provided it is heated, "
                        "filtered and planted. The snail handles glass algae "
                        "without competing for space.") +
                    stocking_plan(
                        "2. Nano school", "5 gal / 19 L · 25-27°C · pH 5.0-7.0",
                        [(10, "chili-rasbora"), (1, "nerite-snail")],
                        "Ten chili rasboras occupy the same space as one "
                        "betta and behave completely differently — a tight "
                        "school in a dark, heavily planted tank. Needs soft, "
                        "acidic water.") +
                    stocking_plan(
                        "3. Shrimp colony", "5 gal / 19 L · 20-25°C · pH 6.5-8.0",
                        [(10, "cherry-shrimp")],
                        "The most self-sustaining option here. A mature, "
                        "planted tank with no fish lets the colony breed and "
                        "the population finds its own level. Excellent in hard "
                        "water.") +
                    stocking_plan(
                        "4. Cool-water micro livebearers", "5 gal / 19 L · 20-24°C · pH 7.0-8.0",
                        [(8, "least-killifish"), (3, "ramshorn-snail")],
                        "The least killifish is one of the smallest livebearers "
                        "in the world at 2 cm and needs no heater in a normal "
                        "room. It breeds readily and the fry survive alongside "
                        "the adults.") +
                    stocking_plan(
                        "5. Surface specialists", "5 gal / 19 L · 23-26°C · pH 6.0-7.5",
                        [(6, "clown-killifish"), (1, "malaysian-trumpet-snail")],
                        "Clown killifish hang just under the surface and "
                        "barely use the rest of the tank, which suits a small "
                        "footprint. They jump, so a tight lid is essential.")
                ),
            },
            {
                "id": "not-suitable",
                "h2": "What Doesn't Belong in 5 Gallons",
                "html": (
                    p("These are the species most often sold for nano tanks "
                      "and most often suffer in them.") +
                    species_table([
                        "neon-tetra", "guppy", "corydoras-catfish",
                        "dwarf-gourami", "platy", "zebra-danio",
                    ], note="Every one needs at least 10 gallons — usually "
                            "because it is a schooling species whose full "
                            "group will not fit, not because the individual "
                            "fish is large.") +
                    callout("stop", "Goldfish and 5 gallon tanks",
                            "A goldfish in a 5 gallon tank is the single most "
                            "common fishkeeping mistake. Fancy goldfish need "
                            "around 75 litres each and produce more waste than "
                            "any tropical fish of comparable size; common "
                            "goldfish belong in ponds.") +
                    callout("warn", "\"It'll grow to its tank\" is a myth",
                            "Fish do not stop growing to fit a small tank. "
                            "Their skeletons keep developing while stunted "
                            "organs do not, which shortens their lives.")
                ),
            },
            {
                "id": "maintenance",
                "h2": "Maintenance Is the Trade-Off",
                "html": (
                    p("A nano tank is less work per change and more work per "
                      "week. The routine that keeps one stable:") +
                    steps([
                        ("Weekly 25% water change",
                         "About 5 litres, temperature-matched and "
                         "dechlorinated. Takes five minutes."),
                        ("Test weekly",
                         "Ammonia and nitrite should read zero; nitrate under "
                         "20 ppm. In this volume a problem shows up in the "
                         "numbers before it shows up in the fish."),
                        ("Feed sparingly, once a day",
                         "What the fish finish in under a minute. Uneaten food "
                         "has a disproportionate effect in a small volume."),
                        ("Keep the heater and lid in place",
                         "A stable temperature matters more here than in any "
                         "larger tank, and most nano species jump."),
                        ("Plant heavily",
                         "Plants consume ammonia and nitrate directly and give "
                         "small fish the cover they need to behave normally."),
                    ])
                ),
            },
        ],
        "faq": [
            ("What fish can live in a 5 gallon tank?",
             "A single betta, a school of ten chili or phoenix rasboras, a "
             "cherry shrimp colony, eight least killifish, or six clown "
             "killifish. Add a nerite or trumpet snail as a cleanup crew. A 5 "
             "gallon tank suits one species group, not a community."),
            ("Can neon tetras live in a 5 gallon tank?",
             "No. Neon tetras need a group of at least six and a minimum of 10 "
             "gallons; the limit is the school, not the individual fish. Chili "
             "rasboras are the closest nano alternative."),
            ("Does a 5 gallon tank need a filter and heater?",
             "Yes to both for almost every species. Small volumes lose heat "
             "and accumulate waste quickly, so a gentle filter and a small "
             "adjustable heater are what make the tank stable. The least "
             "killifish setup is the one exception on temperature."),
            ("How often should I change the water in a 5 gallon tank?",
             "25% weekly — about 5 litres. Small tanks need changes at least "
             "as often as large ones, because there is no volume to dilute "
             "waste between them."),
        ],
        "cta": {
            "heading": "Planning a nano tank?",
            "text": "Filter the species database by tank size to see every "
                    "option that fits.",
            "buttons": [("/search/?tank_size=5", "Browse Nano Species", "search"),
                        ("/quiz/", "Take the Quiz", "target")],
        },
        "related": ["10-gallon-stocking-ideas", "how-many-fish-in-a-tank"],
    }


NEW_ARTICLES = [
    _water_parameters(),
    _how_many_fish(),
    _twenty_gallon(),
    _algae(),
    _tank_mates(),
    _five_gallon(),
]

for _article in NEW_ARTICLES:
    _article.setdefault("published", TODAY)
    _article.setdefault("modified", TODAY)
    _article.setdefault("updated_label", UPDATED)


# --------------------------------------------------------------------------
# Articles index
# --------------------------------------------------------------------------

def index_entries():
    """Every article, newest-written first, for the /articles/ listing."""
    entries = []
    for a in NEW_ARTICLES:
        entries.append({
            "slug": a["slug"], "kicker": a["kicker"],
            "card_title": a["card_title"], "card_blurb": a["card_blurb"],
            "read_time": a["read_time"], "h1": a["h1"],
        })
    for a in EXISTING:
        entries.append(dict(a))
    return entries


def render_index(entries):
    featured = next((e for e in entries if e.get("featured")), entries[0])
    rest = [e for e in entries if e["slug"] != featured["slug"]]

    cards_html = ""
    for e in rest:
        cards_html += f'''
                <a href="/articles/{e['slug']}/" class="flex flex-col bg-white rounded-2xl p-6 border border-slate-100 hover:shadow-lg hover:border-cyan-200 transition">
                    <span class="text-sm text-cyan-600 font-medium">{T.esc(e['kicker'])}</span>
                    <h3 class="text-lg font-bold text-slate-800 mt-2">{T.esc(e['card_title'])}</h3>
                    <p class="text-slate-600 text-sm mt-2 flex-1">{T.esc(e['card_blurb'])}</p>
                    <span class="text-xs text-slate-400 mt-4">{T.esc(e['read_time'])}</span>
                </a>'''

    listing = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id={T.GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{T.GA_ID}');</script>

    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#06b6d4">

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aquarium Guides &amp; Articles | FishFinder</title>
    <meta name="description" content="{len(entries)} in-depth freshwater aquarium guides: cycling, water parameters, stocking by tank size, algae control and choosing tank mates.">
    <link rel="canonical" href="{T.SITE}/articles/">

    <meta property="og:type" content="website">
    <meta property="og:url" content="{T.SITE}/articles/">
    <meta property="og:title" content="Aquarium Guides &amp; Articles">
    <meta property="og:description" content="In-depth freshwater aquarium guides: cycling, water parameters, stocking, algae and compatibility.">
    <meta property="og:site_name" content="FishFinder">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Aquarium Guides &amp; Articles | FishFinder">
    <meta name="twitter:description" content="In-depth freshwater aquarium guides for every stage of the hobby.">

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "Aquarium Guides & Articles",
      "url": "{T.SITE}/articles/",
      "description": "In-depth freshwater aquarium guides covering cycling, water chemistry, stocking and compatibility.",
      "hasPart": [
{",".join(f'''
        {{
          "@type": "Article",
          "headline": {T.json.dumps(e['h1'] if 'h1' in e else e['card_title'], ensure_ascii=False)},
          "url": "{T.SITE}/articles/{e['slug']}/"
        }}''' for e in entries)}
      ]
    }}
    </script>

    <link rel="stylesheet" href="/css/tailwind.css">
{S.LUCIDE_TAG}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{T.AHREFS_KEY}" async></script>
</head>
<body class="bg-slate-50 min-h-screen text-slate-800">
{T._HEADER}
    <main class="max-w-4xl mx-auto px-4 py-12">
        <nav class="text-sm text-slate-500 mb-8">
            <a href="/" class="hover:text-cyan-600">Home</a>
            <span class="mx-2">›</span>
            <span class="text-slate-700">Articles</span>
        </nav>

        <div class="mb-10">
            <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 mb-4">Aquarium Guides</h1>
            <p class="text-xl text-slate-600">Practical, specific guides to setting up and stocking a freshwater tank — grounded in the {len(T.FISH)} species in our database.</p>
        </div>

        <a href="/articles/{featured['slug']}/" class="block bg-gradient-to-r from-cyan-500 to-teal-600 rounded-3xl p-8 md:p-10 text-white hover:shadow-xl transition mb-12">
            <span class="text-sm font-medium text-cyan-100">Start here · {T.esc(featured['kicker'])}</span>
            <h2 class="text-2xl md:text-3xl font-bold mb-3 mt-2">{T.esc(featured['card_title'])}</h2>
            <p class="text-cyan-50">{T.esc(featured['card_blurb'])}</p>
            <span class="inline-flex items-center gap-2 mt-6 font-semibold">
                Read the guide
                <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </span>
        </a>

        <h2 class="text-xl font-bold text-slate-900 mb-6">All Articles</h2>
        <div class="grid md:grid-cols-2 gap-6">{cards_html}
        </div>

        <section class="bg-white rounded-3xl border border-slate-100 p-8 text-center mt-12">
            <h2 class="text-2xl font-bold text-slate-900 mb-3">Need help choosing fish?</h2>
            <p class="text-slate-600 mb-6">Answer a few questions about your tank and we'll suggest species that fit it.</p>
            <a href="/quiz/" class="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-teal-600 text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg transition">
                <i data-lucide="target" class="w-5 h-5"></i>
                Take the Quiz
            </a>
        </section>
    </main>

{T._FOOTER}
    <script>
        renderIcons();
    </script>
</body>
</html>'''
    return S.enhance_page(listing, fish_index=T.FISH_BY_ID,
                          image_dims=S.load_image_dims(),
                          css_ver=S.css_version())


def update_sitemap():
    """Add any new article URL to sitemap.xml, leaving the rest untouched.

    The sitemap carries 531 URLs with hreflang alternates across four
    locales, so it is edited in place rather than regenerated. The new
    articles are English-only for now.
    """
    path = ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    added = []
    block = ""
    for article in NEW_ARTICLES:
        url = f"{T.SITE}/articles/{article['slug']}/"
        if f"<loc>{url}</loc>" in xml:
            continue
        added.append(article["slug"])
        block += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{article['modified']}</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="{url}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>
    <priority>0.7</priority>
  </url>
"""
    if block:
        xml = xml.replace("</urlset>", block + "</urlset>", 1)
        path.write_text(xml, encoding="utf-8")
    return added


def main():
    entries = index_entries()
    by_slug = {e["slug"]: e for e in entries}

    for article in NEW_ARTICLES:
        for slug in article["related"]:
            if slug not in by_slug:
                raise SystemExit(f"{article['slug']}: unknown related slug {slug!r}")

        html = T.render(article, by_slug)
        out = ROOT / "articles" / article["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"✓ {article['slug']}")

    (ROOT / "articles" / "index.html").write_text(
        render_index(entries), encoding="utf-8")
    print(f"✓ articles index ({len(entries)} articles)")

    added = update_sitemap()
    print(f"✓ sitemap.xml: {len(added)} new URL(s)"
          + (f" ({', '.join(added)})" if added else ""))


if __name__ == "__main__":
    main()
