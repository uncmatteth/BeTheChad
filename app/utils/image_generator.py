import os
import requests
import uuid
from PIL import Image
from io import BytesIO
from flask import current_app
from app.extensions import db, cache

# Configure your AI image generation service API keys
# We're using Replicate.com's Stable Diffusion API for pixel art
REPLICATE_API_TOKEN = os.environ.get('REPLICATE_API_TOKEN')
REPLICATE_PIXEL_MODEL = "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478"

def generate_chad_avatar(chad_class, style_preferences=None, seed=None):
    """
    Generate a pixel art avatar for a Chad character
    
    Args:
        chad_class (str): The class of the Chad (sigma, gigachad, etc.)
        style_preferences (list): Optional list of style preferences (sunglasses, beard, etc.)
        seed (int): Optional seed for reproducible generation
        
    Returns:
        str: Path to the generated image
    """
    if style_preferences is None:
        style_preferences = []
    
    # Create a detailed prompt for the AI
    style_text = ", ".join(style_preferences) if style_preferences else ""
    prompt = f"16-bit pixel art character portrait of a {chad_class} Chad, {style_text}, pixelated, retro game style, RPG character portrait"
    
    # Negative prompt to avoid unwanted elements
    negative_prompt = "realistic, 3D, modern, high resolution, blurry, anime, cartoon, text, words, logo"
    
    # Cache key for this specific request
    cache_key = f"avatar_{chad_class}_{'-'.join(style_preferences)}_{seed}"
    cached_path = cache.get(cache_key)
    
    if cached_path and os.path.exists(cached_path):
        return cached_path
    
    try:
        # Call the AI image generation API
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {REPLICATE_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "version": REPLICATE_PIXEL_MODEL,
                "input": {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "width": 256,
                    "height": 256,
                    "num_outputs": 1,
                    "seed": seed,
                    "guidance_scale": 7.5
                }
            }
        )
        
        if response.status_code != 201:
            current_app.logger.error(f"Failed to generate image: {response.text}")
            # Fall back to default image
            return get_default_avatar(chad_class)
        
        prediction = response.json()
        
        # Poll for completion
        prediction_id = prediction["id"]
        api_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        
        # Wait for the prediction to complete
        while True:
            response = requests.get(
                api_url,
                headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}
            )
            
            prediction = response.json()
            if prediction["status"] == "succeeded":
                break
            elif prediction["status"] == "failed":
                current_app.logger.error(f"Prediction failed: {prediction}")
                return get_default_avatar(chad_class)
                
            import time
            time.sleep(1)
        
        # Get the image URL from the prediction
        image_url = prediction["output"][0]
        
        # Download the image
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        
        # Save the image
        static_folder = current_app.static_folder
        generated_filename = f"{uuid.uuid4()}.png"
        avatar_dir = os.path.join(static_folder, "img", "chad", "generated")
        os.makedirs(avatar_dir, exist_ok=True)
        
        image_path = os.path.join(avatar_dir, generated_filename)
        img.save(image_path)
        
        # Get the relative path for the database/frontend
        relative_path = f"img/chad/generated/{generated_filename}"
        
        # Cache the result
        cache.set(cache_key, relative_path, timeout=86400)  # Cache for 24 hours
        
        return relative_path
        
    except Exception as e:
        current_app.logger.error(f"Error generating avatar: {str(e)}")
        return get_default_avatar(chad_class)

def get_default_avatar(chad_class):
    """Get a default avatar for a Chad class if generation fails"""
    avatar_map = {
        "sigma": "img/chad/default/sigma.png",
        "gigachad": "img/chad/default/gigachad.png",
        "trad": "img/chad/default/trad.png",
        "chad": "img/chad/default/chad.png"
    }
    
    return avatar_map.get(chad_class.lower(), "img/chad/default/chad.png")

def process_avatar_with_equipment(avatar_path, equipped_items):
    """
    Processes an avatar with equipped items
    This is for preview only - the NFT image will be locked after minting
    
    Args:
        avatar_path (str): Path to the avatar image
        equipped_items (list): List of equipped items
        
    Returns:
        str: Path to the processed image
    """
    try:
        static_folder = current_app.static_folder
        
        # Load the base avatar
        avatar_full_path = os.path.join(static_folder, avatar_path)
        base_img = Image.open(avatar_full_path).convert("RGBA")
        
        # Layer equipped items on top
        for item in equipped_items:
            if not item.item_type.image_path:
                continue
                
            item_img_path = os.path.join(static_folder, item.item_type.image_path)
            if not os.path.exists(item_img_path):
                continue
                
            item_img = Image.open(item_img_path).convert("RGBA")
            
            # Resize item image to match avatar if needed
            if item_img.size != base_img.size:
                item_img = item_img.resize(base_img.size, Image.LANCZOS)
            
            # Composite the images
            base_img = Image.alpha_composite(base_img, item_img)
        
        # Save the processed image
        processed_filename = f"equipped_{uuid.uuid4()}.png"
        preview_dir = os.path.join(static_folder, "img", "chad", "preview")
        os.makedirs(preview_dir, exist_ok=True)
        
        processed_path = os.path.join(preview_dir, processed_filename)
        base_img.save(processed_path)
        
        return f"img/chad/preview/{processed_filename}"
        
    except Exception as e:
        current_app.logger.error(f"Error processing avatar: {str(e)}")
        return avatar_path  # Return original avatar path if processing fails 