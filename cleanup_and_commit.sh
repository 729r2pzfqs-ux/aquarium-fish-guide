#!/bin/bash
# Cleanup script: removes corrupted directories and commits all fixes
# Run from the aquarium-fish-guide directory

set -e
cd "$(dirname "$0")"

echo "Removing stale git lock..."
rm -f .git/index.lock

echo "Removing corrupted directories..."
rm -rf fish/convict-cichtyophthirioselid
rm -rf fish/firemouth-cichtyophthirioselid
rm -rf de/fische/hillstream-schmerle
rm -rf de/fische/odessa-barbe
rm -rf de/fische/rabbit-schnecke
rm -rf de/fische/ramshorn-schnecke
rm -rf de/fische/tinfoil-barbe
rm -rf es/peces/hillstream-locha
rm -rf es/peces/mystery-caracol

echo "Staging all changes..."
git add -A

echo "Committing..."
git \
  -c user.name="729r2pzfqs-ux" \
  -c user.email="729r2pzfqs-ux@users.noreply.github.com" \
  commit -m "Fix mixed-language slug corruption in translated fish pages

Root cause: regex translation patterns (e.g. barb→Barbe, loach→Schmerle,
ich→ichtyophthiriose) in the DE/ES/FR generators matched inside URLs,
corrupting fish ID slugs in href/src attributes, meta tags, and JSON-LD.

Fix: protect URL-bearing HTML attributes, <link>, <meta>, and JSON-LD
blocks from regex translation by replacing them with placeholders before
translation and restoring them after.

Also removes 9 corrupted directories left from previous runs:
- fish/convict-cichtyophthirioselid, fish/firemouth-cichtyophthirioselid
- de/fische/{hillstream-schmerle,odessa-barbe,rabbit-schnecke,
  ramshorn-schnecke,tinfoil-barbe}
- es/peces/{hillstream-locha,mystery-caracol}"

echo ""
echo "Done! Committed. Do NOT push."
