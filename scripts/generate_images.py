#!/usr/bin/env python3
"""
Batch generate aquarium fish images using Replicate API (Flux 1.1 Pro - highest quality)
"""

import os
import json
import requests
import time
import sys

API_URL = "https://api.replicate.com/v1/models/black-forest-labs/flux-1.1-pro/predictions"

def load_fish():
    """Load fish from JSON data"""
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, "..", "data", "fish.json")
    with open(data_path, 'r') as f:
        return json.load(f)

def generate_prompt(fish):
    """Generate the image prompt for a fish"""
    name = fish['name']
    scientific = fish.get('scientific', '')
    category = fish.get('category', 'fish')
    
    # Customize based on fish type
    if category == 'shrimp':
        subject = f"a {name} shrimp ({scientific})"
        style = "showing its translucent body and detailed features"
    elif category == 'snail':
        subject = f"a {name} snail ({scientific})"
        style = "showing its shell pattern and body"
    elif category == 'crayfish':
        subject = f"a {name} crayfish ({scientific})"
        style = "showing its claws and segmented body"
    else:
        subject = f"a {name} fish ({scientific})"
        style = "showing its natural coloration and fin details"
    
    return f"""Ultra realistic photograph of {subject}, {style}.
The subject is swimming naturally in a beautifully planted freshwater aquarium with soft lighting.
Crystal clear water, natural aquatic plants in the background slightly blurred.
The fish/creature is in sharp focus, centered, showing its best features and natural colors.
Professional aquarium photography style, shallow depth of field, 4:5 portrait composition.
No artificial decorations, no hands, no text, no watermarks.
The colors should be vibrant and true to species."""

def wait_for_prediction(prediction_url, headers, max_wait=60):
    """Poll until prediction is complete"""
    start = time.time()
    while time.time() - start < max_wait:
        try:
            response = requests.get(prediction_url, headers=headers, timeout=30)
            data = response.json()
            status = data.get('status')
            
            if status == 'succeeded':
                return data.get('output')
            elif status == 'failed':
                error_msg = data.get('error') or 'unknown error'
                print(f" (failed: {error_msg})", end="")
                return None
            elif status == 'canceled':
                print(f" (canceled)", end="")
                return None
            
            time.sleep(2)
        except Exception as e:
            print(f" (poll error: {e})", end="")
            time.sleep(2)
    
    print(f" (timeout)", end="")
    return None

def generate_image(fish, output_dir, api_token):
    """Generate a single fish image"""
    slug = fish['id']
    output_path = os.path.join(output_dir, f"{slug}.png")
    
    if os.path.exists(output_path):
        print(f"⏭️  Skipping {fish['name']} (already exists)")
        return True, "skipped"
    
    prompt = generate_prompt(fish)
    print(f"🐟 Generating {fish['name']}...", end="", flush=True)
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "prompt": prompt,
            "aspect_ratio": "4:5",
            "output_format": "png",
            "output_quality": 100,
            "safety_tolerance": 2,
            "prompt_upsampling": True
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        data = response.json()
        
        if data.get('error'):
            print(f"\n❌ API error: {data['error']}")
            return False, data['error']
        
        prediction_id = data.get('id')
        if not prediction_id:
            print(f"\n❌ No prediction ID returned")
            return False, "no_id"
        
        prediction_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        output = wait_for_prediction(prediction_url, headers)
        
        if output:
            img_url = str(output)
            img_response = requests.get(img_url, timeout=60)
            
            os.makedirs(output_dir, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"\n✅ Saved {slug}.png ({len(img_response.content) // 1024}KB)")
            return True, "generated"
        else:
            print(f"\n❌ No output for {fish['name']}")
            return False, "no_output"
            
    except Exception as e:
        print(f"\n❌ Error generating {fish['name']}: {e}")
        return False, str(e)

def main():
    print("🐠 AquariumFishGuide Image Generator (Flux 1.1 Pro)")
    print("="*60)
    
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        print("❌ Error: REPLICATE_API_TOKEN not set")
        return 1
    
    fish_list = load_fish()
    print(f"📦 {len(fish_list)} fish to generate\n")
    
    script_dir = os.path.dirname(__file__)
    output_dir = os.path.join(script_dir, "..", "images", "fish")
    
    success = 0
    skipped = 0
    failed = []
    
    for i, fish in enumerate(fish_list, 1):
        print(f"[{i}/{len(fish_list)}] ", end="")
        result, status = generate_image(fish, output_dir, api_token)
        
        if result:
            if status == "skipped":
                skipped += 1
            else:
                success += 1
        else:
            failed.append(fish['name'])
        
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"✅ Generated: {success}")
    print(f"⏭️  Skipped: {skipped}")
    if failed:
        print(f"❌ Failed ({len(failed)}): {', '.join(failed[:10])}")
        if len(failed) > 10:
            print(f"   ... and {len(failed) - 10} more")
    print(f"📁 Output: {output_dir}")
    print(f"💰 Estimated cost: ${success * 0.04:.2f}")
    
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())
