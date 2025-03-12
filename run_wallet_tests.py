#!/usr/bin/env python
"""
Test runner for wallet-related tests in Chad Battles.
Run this script to execute all wallet, NFT, and Solana API tests.
"""
import unittest
import sys
import os
from tests.test_wallet import WalletTestCase
from tests.test_nft import NFTTestCase
from tests.test_solana_api import SolanaAPITestCase

def run_tests():
    """Run all wallet-related tests."""
    # Create test suites
    wallet_suite = unittest.TestLoader().loadTestsFromTestCase(WalletTestCase)
    nft_suite = unittest.TestLoader().loadTestsFromTestCase(NFTTestCase)
    solana_suite = unittest.TestLoader().loadTestsFromTestCase(SolanaAPITestCase)
    
    # Combine all test suites
    all_tests = unittest.TestSuite([wallet_suite, nft_suite, solana_suite])
    
    # Run the tests
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    
    # Return the test result
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running wallet-related tests for Chad Battles...")
    success = run_tests()
    
    if not success:
        sys.exit(1)
    
    print("\nAll tests passed successfully!")
    sys.exit(0) 