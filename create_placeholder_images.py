#!/usr/bin/env python
"""
Generate placeholder images for Chad Battles

This script creates placeholder images for all the various assets in the game:
- Chad classes
- Waifus
- Items
- Elixirs

The images are simple color blocks with text, which can be replaced with actual
artwork later.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random
import colorsys

# Constants
OUTPUT_DIR = "app/static/img"
IMAGE_SIZE = (200, 200)
CHAD_CLASSES = [
    "Meme Overlord",
    "Crypto Knight",
    "Alpha Chad",
    "Sigma Grindset",
    "Ratio King",
    "Normie Chad",
    "Gigachad",  # Already exists but creating placeholder for consistency
]
WAIFU_TYPES = [
    "Common",
    "Uncommon",
    "Rare",
    "Epic",
    "Legendary",
]
ITEM_TYPES = [
    "Weapon",
    "Armor",
    "Accessory",
    "Consumable",
]
ELIXIR_TYPES = [
    "Strength",
    "Intelligence",
    "Speed",
    "Luck",
    "Meme",
]

def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB tuple (0-255)"""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def generate_color(seed):
    """Generate a consistent color based on a seed string"""
    # Hash the string to get a number
    hash_value = sum(ord(c) for c in seed)
    # Use the hash to generate HSV values
    hue = (hash_value % 360) / 360.0
    saturation = 0.7
    value = 0.9
    return hsv_to_rgb(hue, saturation, value)

def create_placeholder_image(name, category, output_path):
    """Create a placeholder image with the name text"""
    # Create a blank image with a background color based on the name
    bg_color = generate_color(name)
    img = Image.new('RGB', IMAGE_SIZE, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add a border
    border_width = 5
    draw.rectangle(
        [(border_width, border_width), 
         (IMAGE_SIZE[0] - border_width, IMAGE_SIZE[1] - border_width)],
        outline=(255, 255, 255)
    )
    
    # Try to load a font, use default if not available
    try:
        # Use different font sizes based on text length
        text_length = len(name)
        if text_length > 15:
            font_size = 18
        elif text_length > 10:
            font_size = 24
        else:
            font_size = 30
            
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Add category text at top
    draw.text((IMAGE_SIZE[0] // 2, 20), category, 
              fill=(255, 255, 255), font=font, anchor="mt")
    
    # Add the name in the center
    draw.text((IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2), name, 
              fill=(255, 255, 255), font=font, anchor="mm")
    
    # Save the image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Created {output_path}")

def create_chad_images():
    """Create placeholder images for all Chad classes"""
    chad_dir = os.path.join(OUTPUT_DIR, "chad")
    os.makedirs(chad_dir, exist_ok=True)
    
    for chad_class in CHAD_CLASSES:
        filename = chad_class.lower().replace(' ', '-') + '.png'
        output_path = os.path.join(chad_dir, filename)
        create_placeholder_image(chad_class, "Chad Class", output_path)

def create_waifu_images():
    """Create placeholder images for Waifu types"""
    waifu_dir = os.path.join(OUTPUT_DIR, "waifu")
    os.makedirs(waifu_dir, exist_ok=True)
    
    for waifu_type in WAIFU_TYPES:
        # Create a few variants for each type
        for i in range(1, 4):
            name = f"{waifu_type} Waifu {i}"
            filename = f"{waifu_type.lower()}-waifu-{i}.png"
            output_path = os.path.join(waifu_dir, filename)
            create_placeholder_image(name, "Waifu", output_path)

def create_item_images():
    """Create placeholder images for item types"""
    item_dir = os.path.join(OUTPUT_DIR, "items")
    os.makedirs(item_dir, exist_ok=True)
    
    for item_type in ITEM_TYPES:
        # Create a few variants for each type
        for i in range(1, 4):
            name = f"{item_type} {i}"
            filename = f"{item_type.lower()}-{i}.png"
            output_path = os.path.join(item_dir, filename)
            create_placeholder_image(name, "Item", output_path)

def create_elixir_images():
    """Create placeholder images for elixir types"""
    elixir_dir = os.path.join(OUTPUT_DIR, "elixirs")
    os.makedirs(elixir_dir, exist_ok=True)
    
    for elixir_type in ELIXIR_TYPES:
        name = f"{elixir_type} Elixir"
        filename = f"{elixir_type.lower()}-elixir.png"
        output_path = os.path.join(elixir_dir, filename)
        create_placeholder_image(name, "Elixir", output_path)

def main():
    """Run the image creation process"""
    print("Creating placeholder images for Chad Battles...")
    
    # Create images for all asset types
    create_chad_images()
    create_waifu_images()
    create_item_images()
    create_elixir_images()
    
    print("All placeholder images created successfully!")

if __name__ == "__main__":
    main() 