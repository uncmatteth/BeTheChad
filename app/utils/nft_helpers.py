import os
import json
import uuid
import logging
from flask import current_app
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

def ensure_metadata_dirs():
    """
    Creates the necessary directory structure for NFT metadata storage
    across all environments.
    """
    # Base directory for NFT metadata
    base_dir = os.path.join(current_app.static_folder, 'metadata')
    
    # Entity type directories
    entity_types = ['chad', 'waifu', 'item']
    
    try:
        # Create base metadata directory if it doesn't exist
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            logger.info(f"Created base metadata directory: {base_dir}")
        
        # Create entity-specific directories
        for entity_type in entity_types:
            entity_dir = os.path.join(base_dir, entity_type)
            if not os.path.exists(entity_dir):
                os.makedirs(entity_dir)
                logger.info(f"Created {entity_type} metadata directory: {entity_dir}")
        
        return True
    except Exception as e:
        logger.error(f"Error creating metadata directories: {str(e)}")
        return False

def create_metadata_file(entity_type, entity_id, metadata, token_id=None):
    """
    Create a metadata file for an NFT.
    
    Args:
        entity_type (str): Type of entity ('chad', 'waifu', 'item')
        entity_id (int): ID of the entity
        metadata (dict): The metadata to save
        token_id (str, optional): Token ID to use for the filename. If None, a UUID will be generated.
        
    Returns:
        tuple: (success, uri, error_message)
    """
    if token_id is None:
        token_id = str(uuid.uuid4())
    
    # Ensure metadata directories exist
    ensure_metadata_dirs()
    
    # Create directory path
    metadata_dir = os.path.join(current_app.static_folder, 'metadata', entity_type)
    
    # Create filename
    filename = f"{token_id}.json"
    file_path = os.path.join(metadata_dir, filename)
    
    try:
        # Ensure all required metadata fields are present
        required_fields = ['name', 'description', 'image', 'attributes']
        for field in required_fields:
            if field not in metadata:
                return False, None, f"Missing required metadata field: {field}"
        
        # Add metadata standard version and creation timestamp
        metadata['version'] = '1.0'
        metadata['created_at'] = datetime.utcnow().isoformat()
        
        # Write metadata to file
        with open(file_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create URI (relative path from static folder)
        uri = f"/static/metadata/{entity_type}/{filename}"
        
        logger.info(f"Created metadata file: {file_path}")
        return True, uri, None
    except Exception as e:
        logger.error(f"Error creating metadata file: {str(e)}")
        return False, None, str(e)

def load_metadata(uri):
    """
    Load metadata from a URI.
    
    Args:
        uri (str): URI of the metadata file
        
    Returns:
        dict: The metadata, or a default metadata object if loading fails
    """
    try:
        # Convert URI to file path
        if uri.startswith('/static/'):
            file_path = os.path.join(current_app.static_folder, uri[8:])
        else:
            file_path = os.path.join(current_app.static_folder, uri)
        
        with open(file_path, 'r') as f:
            metadata = json.load(f)
        
        return metadata
    except Exception as e:
        logger.error(f"Error loading metadata from {uri}: {str(e)}")
        
        # Return default metadata
        return {
            "name": "Unknown NFT",
            "description": "Metadata could not be loaded",
            "image": "/static/img/placeholders/nft-placeholder.png",
            "attributes": []
        }

def create_chad_metadata(chad):
    """
    Create metadata for a Chad NFT.
    
    Args:
        chad: The Chad model instance
        
    Returns:
        dict: The metadata
    """
    # Base image URL
    image_url = f"/static/img/chad/{chad.avatar}"
    
    # Create attributes
    attributes = [
        {
            "trait_type": "Class",
            "value": chad.chad_class.name
        },
        {
            "trait_type": "Level",
            "value": chad.level
        },
        {
            "trait_type": "Clout",
            "value": chad.get_total_stats().clout
        },
        {
            "trait_type": "Roast Level",
            "value": chad.get_total_stats().roast_level
        },
        {
            "trait_type": "Cringe Resistance",
            "value": chad.get_total_stats().cringe_resistance
        },
        {
            "trait_type": "Drip Factor",
            "value": chad.get_total_stats().drip_factor
        }
    ]
    
    # Add equipped items as attributes
    equipped_items = chad.get_all_equipped_items()
    if equipped_items:
        for item in equipped_items:
            attributes.append({
                "trait_type": f"Equipped {item.item_type.slot.capitalize()}",
                "value": item.item_type.name
            })
    
    # Create metadata
    metadata = {
        "name": chad.name,
        "description": f"Level {chad.level} {chad.chad_class.name} Chad from Chad Battles. This Chad has {chad.get_total_stats().clout} clout and {chad.get_total_stats().drip_factor} drip factor.",
        "image": image_url,
        "attributes": attributes,
        "external_url": f"https://chadbattles.com/profile/{chad.user.username}/chad"
    }
    
    return metadata

def create_waifu_metadata(waifu):
    """
    Create metadata for a Waifu NFT.
    
    Args:
        waifu: The Waifu model instance
        
    Returns:
        dict: The metadata
    """
    # Base image URL
    image_url = f"/static/img/waifu/{waifu.waifu_type.name.lower().replace(' ', '-')}.png"
    
    # Create attributes
    attributes = [
        {
            "trait_type": "Type",
            "value": waifu.waifu_type.name
        },
        {
            "trait_type": "Rarity",
            "value": waifu.waifu_type.rarity.name
        },
        {
            "trait_type": "Clout",
            "value": waifu.clout
        },
        {
            "trait_type": "Roast Level",
            "value": waifu.roast_level
        },
        {
            "trait_type": "Cringe Resistance",
            "value": waifu.cringe_resistance
        },
        {
            "trait_type": "Drip Factor",
            "value": waifu.drip_factor
        }
    ]
    
    # Add equipped items as attributes
    equipped_items = waifu.get_equipped_items()
    if equipped_items:
        for item in equipped_items:
            attributes.append({
                "trait_type": f"Equipped {item.item_type.slot.capitalize()}",
                "value": item.item_type.name
            })
    
    # Create metadata
    metadata = {
        "name": waifu.waifu_type.name,
        "description": f"{waifu.waifu_type.rarity.name} {waifu.waifu_type.name} from Chad Battles. This waifu provides {waifu.clout} clout and {waifu.drip_factor} drip factor.",
        "image": image_url,
        "attributes": attributes,
        "external_url": f"https://chadbattles.com/inventory/waifu/{waifu.id}"
    }
    
    return metadata

def create_item_metadata(item):
    """
    Create metadata for an Item NFT.
    
    Args:
        item: The Item model instance
        
    Returns:
        dict: The metadata
    """
    # Base image URL
    image_url = f"/static/img/item/{item.item_type.name.lower().replace(' ', '-')}.png"
    
    # Create attributes
    attributes = [
        {
            "trait_type": "Type",
            "value": item.item_type.name
        },
        {
            "trait_type": "Rarity",
            "value": item.item_type.rarity.name
        },
        {
            "trait_type": "Slot",
            "value": item.item_type.slot
        }
    ]
    
    # Add stat bonuses as attributes
    if item.clout_bonus:
        attributes.append({
            "trait_type": "Clout Bonus",
            "value": item.clout_bonus
        })
    
    if item.roast_bonus:
        attributes.append({
            "trait_type": "Roast Bonus",
            "value": item.roast_bonus
        })
    
    if item.cringe_resistance_bonus:
        attributes.append({
            "trait_type": "Cringe Resistance Bonus",
            "value": item.cringe_resistance_bonus
        })
    
    if item.drip_bonus:
        attributes.append({
            "trait_type": "Drip Bonus",
            "value": item.drip_bonus
        })
    
    # Create metadata
    metadata = {
        "name": item.item_type.name,
        "description": f"{item.item_type.rarity.name} {item.item_type.name} from Chad Battles. This {item.item_type.slot} provides bonuses to your Chad or Waifu stats.",
        "image": image_url,
        "attributes": attributes,
        "external_url": f"https://chadbattles.com/inventory/item/{item.id}"
    }
    
    return metadata

def get_nft_value(nft):
    """
    Calculate the Chadcoin value of an NFT for burning.
    
    Args:
        nft: The NFT model instance
        
    Returns:
        int: The Chadcoin value
    """
    base_values = {
        'chad': 100,   # Base value for Chad NFTs
        'waifu': 50,   # Base value for Waifu NFTs
        'item': 25     # Base value for Item NFTs
    }
    
    rarity_multipliers = {
        'common': 1,
        'rare': 2,
        'epic': 4,
        'legendary': 10
    }
    
    # Get base value by entity type
    value = base_values.get(nft.entity_type, 10)
    
    # Apply entity-specific multipliers
    if nft.entity_type == 'chad':
        # For Chads, multiply by level
        chad = nft.get_entity()
        if chad:
            value *= min(10, max(1, chad.level))  # Cap at 10x multiplier
    
    elif nft.entity_type in ['waifu', 'item']:
        # For Waifus and Items, multiply by rarity
        entity = nft.get_entity()
        if entity:
            if nft.entity_type == 'waifu':
                rarity = entity.waifu_type.rarity.name.lower()
            else:  # item
                rarity = entity.item_type.rarity.name.lower()
            
            multiplier = rarity_multipliers.get(rarity, 1)
            value *= multiplier
    
    return value 