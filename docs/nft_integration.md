# NFT Integration Documentation

This document details the NFT system implementation in Chad Battles, which allows players to mint their Chad characters, waifus, and items as NFTs on the Solana blockchain.

## Overview

The NFT system in Chad Battles enables:

1. Minting of game entities (Chad characters, waifus, and items) as NFTs
2. Updating metadata for Chad NFTs when they level up 
3. Burning NFTs to receive Chadcoin
4. A 1% royalty on all NFT transactions
5. Support for multiple wallet types (Phantom, Solflare, Metamask, Magic Eden)

## Database Models

### NFT Model

The `NFT` model tracks each minted NFT and includes:

- Reference to the entity type (`chad`, `waifu`, or `item`)
- Links to the respective entity via foreign keys
- Token ID and transaction IDs for blockchain operations
- Metadata URI for the NFT's metadata
- Burn status and timestamp

### Inventory Model

The `Inventory` model provides utility methods for managing a user's items, waifus, and NFTs, including:

- Equipping/unequipping items
- Equipping/unequipping waifus
- Tracking inventory statistics

## API Endpoints

- `/api/mint-nft` - Mint a waifu or item as an NFT
- `/api/mint-chad-nft` - Mint a Chad character as an NFT
- `/api/burn-nft` - Burn an NFT to receive Chadcoin

## Wallet Integration

The system supports connecting multiple wallet types:
- Phantom
- Solflare
- Metamask
- Magic Eden

Players connect their wallets through the wallet connection UI, which displays supported options and handles the connection process.

## NFT Updatability

Chad NFTs support metadata updates as the character progresses. When a Chad levels up or changes equipment, the NFT's metadata can be updated to reflect these changes without requiring a new mint.

## Item Overriding

Waifus can have their equipped items overridden with better items. The system tracks which items are equipped to which waifus and ensures that:

1. Only one item of each type can be equipped per waifu
2. Better items replace existing ones
3. The waifu's stats are updated accordingly

## Burning Mechanism

Players can burn their NFTs to receive Chadcoin. The amount received depends on:

- Entity type (Chad, waifu, or item)
- Entity rarity (common, rare, epic, legendary)
- For Chads, the character's level also affects the value

## Database Migration

The `inventory_and_nft.py` migration creates necessary tables and columns for the NFT and inventory systems, including:

- Creating the `inventories` table
- Updating the `nfts` table structure
- Adding `is_minted` column to entity tables
- Adding `is_equipped` column to the `waifus` table
- Adding `wallet_type` column to the `users` table

## Frontend Interface

The inventory system provides a comprehensive UI for managing NFTs and inventory:

- Battle Stash (main inventory page)
- Waifu management
- Item management
- NFT vault for viewing and managing minted NFTs

## Testing

The NFT system should be tested across all environments:

1. **Development**: Test basic functionality with mocked blockchain interactions
2. **Test**: Verify against a Solana testnet
3. **Production**: Ensure real blockchain transactions work correctly

## Royalty Implementation

A 1% royalty is automatically applied to all NFT transactions on supported marketplaces through Solana's Metaplex standard. 