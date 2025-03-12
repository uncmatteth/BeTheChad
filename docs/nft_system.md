# Chad Battles NFT System

This document provides an overview of the NFT (Non-Fungible Token) system in Chad Battles, including how to mint NFTs, burn them for Chadcoin, and understand the technical implementation.

## Table of Contents

1. [Overview](#overview)
2. [NFT Types](#nft-types)
3. [Minting NFTs](#minting-nfts)
4. [Burning NFTs](#burning-nfts)
5. [Wallet Integration](#wallet-integration)
6. [Royalties](#royalties)
7. [Technical Implementation](#technical-implementation)
8. [Environment Setup](#environment-setup)
9. [Testing](#testing)

## Overview

Chad Battles allows players to mint their in-game assets (Chad characters, waifus, and items) as NFTs on the Solana blockchain. These NFTs can be transferred to other wallets, traded on third-party marketplaces, or burned to receive Chadcoin.

The NFT system uses Solana's SPL404 token standard, which combines fungible and non-fungible characteristics, allowing for a unified token system that handles both NFTs and Chadcoin.

## NFT Types

The following entity types can be minted as NFTs:

1. **Chad Characters**: Your main character in the game. Minting a Chad as an NFT will lock its current appearance, even if you continue to level up or change equipment in the game.

2. **Waifus**: Battle companions that provide stat bonuses. When minting a waifu, her current equipped items are captured in the NFT metadata.

3. **Items**: Equipment pieces that boost stats. These can be minted independently and represent the base item.

## Minting NFTs

To mint an NFT:

1. Connect your Solana wallet in the inventory screen.
2. Navigate to the entity you want to mint (Chad, waifu, or item).
3. Click the "Mint NFT" button.
4. Confirm the transaction in your wallet.

Important considerations:
- Minting requires a connected Solana wallet.
- Each entity can only be minted once.
- Chad NFTs lock the character's current appearance and stats at the time of minting.
- Minting may require Chadcoin and/or Solana for gas fees.
- There is a cooldown period between minting operations to prevent spam.

## Burning NFTs

To burn an NFT and receive Chadcoin:

1. Go to your NFT collection.
2. Select the NFT you want to burn.
3. Click the "Burn for X Chadcoin" button.
4. Confirm the transaction.

The Chadcoin value of an NFT depends on:
- The entity type (Chad, waifu, or item)
- The rarity of the entity
- For Chads, their level at the time of minting

Base values:
- Chad: 100 * level (max 10x multiplier)
- Waifu: 50 * rarity multiplier
- Item: 25 * rarity multiplier

Rarity multipliers:
- Common: 1x
- Rare: 2x
- Epic: 4x
- Legendary: 10x

## Wallet Integration

Chad Battles supports multiple Solana wallets:
- Phantom
- Solflare
- Metamask (with Solana support)
- Magic Eden
- Slope

To connect your wallet:
1. Click the "Connect Wallet" button in the inventory.
2. Select your wallet provider.
3. Approve the connection request in your wallet.

You can disconnect your wallet at any time by clicking the "Disconnect" button.

## Royalties

All NFT transactions on third-party marketplaces include a 1% royalty fee that supports the development of Chad Battles. This royalty is enforced at the protocol level using Solana's Metaplex standard.

## Technical Implementation

The NFT system consists of the following components:

1. **Database Models**:
   - `NFT`: Stores NFT metadata, token IDs, and ownership information.
   - `Transaction`: Records all NFT-related transactions (minting, burning, transfers).

2. **Metadata Generation**:
   - NFT metadata follows the Metaplex standard.
   - Metadata includes entity stats, attributes, and image links.

3. **On-chain Interaction**:
   - Minting uses Solana's SPL404 token standard.
   - Transactions are signed using the user's connected wallet.

4. **User Interface**:
   - Inventory integration for minting entities.
   - NFT collection view for managing minted NFTs.
   - Transaction history for tracking operations.

## Environment Setup

The NFT system is configured to work across all environments (development, testing, production) with appropriate settings for each.

To set up the NFT environment:
```
python setup/setup_nft_environment.py --env [dev|test|prod]
```

This script:
1. Creates necessary directories for metadata storage.
2. Sets up placeholder images and metadata.
3. Configures environment variables for the NFT system.

## Testing

The NFT system includes comprehensive tests to ensure proper functionality:

1. **Unit Tests**: Test individual components like metadata generation.
2. **Integration Tests**: Test the interaction between components.
3. **End-to-End Tests**: Test the full minting and burning processes.

To run the tests:
```
python -m unittest tests/test_nft_system.py
```

Additional test coverage includes:
- Wallet connection/disconnection
- Metadata creation and loading
- NFT value calculation
- Transaction recording 