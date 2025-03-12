# Wallet Integration for Chad Battles

This directory contains the templates and components for the Chad Battles wallet integration, which allows users to connect their Solana wallets and interact with NFTs within the game.

## Key Features

- Connect and disconnect Solana wallets (Phantom, Solflare, Slope, and Magic Eden)
- View wallet information and balances
- Mint NFTs for in-game entities (Chads, Waifus, etc.)
- Burn NFTs for in-game rewards
- Transfer NFTs to other users
- View transaction history
- Responsive design for desktop and mobile

## Directory Structure

The wallet integration consists of the following components:

- **Templates**
  - `index.html` - Main wallet dashboard
  - `connect.html` - Wallet connection page
  - `transactions.html` - Transaction history page

- **Controllers**
  - `wallet.py` - Handles wallet connection and status
  - `nft.py` - Handles NFT operations (mint, burn, transfer)
  - `api.py` - Provides API endpoints for wallet operations

- **Static Assets**
  - `css/wallet.css` - Wallet-specific styles
  - `js/wallet.js` - Wallet functionality scripts
  - `img/wallets/` - Wallet icons and assets

- **Utils**
  - `solana_api.py` - Utilities for interacting with the Solana blockchain

- **Tests**
  - `test_wallet.py` - Tests for wallet functionality
  - `test_nft.py` - Tests for NFT functionality
  - `test_solana_api.py` - Tests for Solana API utilities

## Usage

### Connecting a Wallet

1. Visit the `/wallet/connect` page
2. Select a supported wallet provider
3. Approve the connection request in your wallet

### Viewing Wallet Information

1. Visit the `/wallet` page when connected
2. View your wallet address, balance, and connected NFTs

### Minting an NFT

1. Visit the entity page (Chad, Waifu, etc.)
2. Click the "Mint NFT" button
3. Approve the transaction in your wallet

### Burning an NFT

1. Visit the `/wallet` page
2. Find the NFT you want to burn
3. Click the "Burn" button
4. Approve the transaction in your wallet

### Transferring an NFT

1. Visit the `/wallet` page
2. Find the NFT you want to transfer
3. Click the "Transfer" button
4. Enter the recipient's wallet address
5. Approve the transaction in your wallet

### Viewing Transaction History

1. Visit the `/wallet/transactions` page
2. View all your transactions organized by type and date

## Development Notes

### Testing

Run the wallet tests using the test runner:

```bash
python run_wallet_tests.py
```

### Environment Variables

The wallet integration requires the following environment variables:

- `SOLANA_RPC_URL` - Solana RPC URL (mainnet or devnet)
- `SOLANA_NETWORK` - Solana network to use (mainnet or devnet)
- `NFT_STORAGE_API_KEY` - API key for NFT.storage (for IPFS uploads)

### Adding New Wallet Providers

To add support for additional wallet providers:

1. Add the wallet icon to `app/static/img/wallets/`
2. Update the wallet connection options in `connect.html`
3. Update the wallet connection handling in `wallet.js`
4. Update the wallet type validation in `wallet.py`

## Support

For issues or questions related to the wallet integration, please contact the development team or create an issue in the project repository. 