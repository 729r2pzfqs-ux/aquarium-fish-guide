#!/usr/bin/env python3
"""Convert fish pages to metric-first (with imperial in parentheses)"""
import os
import re
import json

# Load fish data
with open('/Users/juhaporraskorpi/clawd/aquarium-fish/data/fish.json') as f:
    fish_data = {fish['id']: fish for fish in json.load(f)}

def inches_to_cm(inches):
    return round(inches * 2.54)

def gallons_to_liters(gallons):
    return round(gallons * 3.785)

def f_to_c(f):
    return round((f - 32) * 5/9)

fish_dir = '/Users/juhaporraskorpi/clawd/aquarium-fish/fish'

for fish_id in os.listdir(fish_dir):
    fish_path = os.path.join(fish_dir, fish_id, 'index.html')
    if not os.path.exists(fish_path):
        continue
    
    fish = fish_data.get(fish_id)
    if not fish:
        print(f"No data for {fish_id}")
        continue
    
    with open(fish_path, 'r') as f:
        html = f.read()
    
    original = html
    
    # Size: X inches -> Xcm (X")
    size_in = fish['size_inches']
    size_cm = inches_to_cm(size_in)
    html = re.sub(
        rf'{size_in}\s*inch(es)?',
        f'{size_cm}cm ({size_in}")',
        html,
        flags=re.IGNORECASE
    )
    
    # Tank: X gallon(s) -> XL (Xgal)
    tank_gal = fish['min_tank_gallons']
    tank_l = gallons_to_liters(tank_gal)
    html = re.sub(
        rf'{tank_gal}[\s-]*gallons?',
        f'{tank_l}L ({tank_gal}gal)',
        html,
        flags=re.IGNORECASE
    )
    html = re.sub(
        rf'Minimum {tank_l}L \({tank_gal}gal\) tank',
        f'Minimum {tank_l}L ({tank_gal}gal) tank',
        html,
        flags=re.IGNORECASE
    )
    
    # Temperature: X-Y°F (A-B°C) -> A-B°C (X-Y°F)
    temp_min_f = fish['temp_min']
    temp_max_f = fish['temp_max']
    temp_min_c = f_to_c(temp_min_f)
    temp_max_c = f_to_c(temp_max_f)
    
    # Match pattern: 72-78°F (22-26°C)
    html = re.sub(
        rf'{temp_min_f}-{temp_max_f}°F\s*\({temp_min_c}-{temp_max_c}°C\)',
        f'{temp_min_c}-{temp_max_c}°C ({temp_min_f}-{temp_max_f}°F)',
        html
    )
    # Also match standalone F temps
    html = re.sub(
        rf'Temperature:\s*{temp_min_f}-{temp_max_f}°F',
        f'Temperature: {temp_min_c}-{temp_max_c}°C ({temp_min_f}-{temp_max_f}°F)',
        html
    )
    
    # Meta descriptions
    html = re.sub(
        rf'\({tank_gal} gallons\)',
        f'({tank_l}L/{tank_gal}gal)',
        html
    )
    
    if html != original:
        with open(fish_path, 'w') as f:
            f.write(html)
        print(f"Updated: {fish_id}")

print("Done!")
