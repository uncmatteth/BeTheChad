"""
Rarity model for Chad Battles.
Defines rarity levels for NFTs and items.
"""
from enum import Enum

class Rarity(Enum):
    """Enum for rarity levels."""
    COMMON = 'common'
    UNCOMMON = 'uncommon'
    RARE = 'rare'
    EPIC = 'epic'
    LEGENDARY = 'legendary'
    MYTHIC = 'mythic'

    @property
    def value_multiplier(self):
        """Get the value multiplier for this rarity level."""
        multipliers = {
            Rarity.COMMON: 1.0,
            Rarity.UNCOMMON: 2.0,
            Rarity.RARE: 4.0,
            Rarity.EPIC: 8.0,
            Rarity.LEGENDARY: 16.0,
            Rarity.MYTHIC: 32.0
        }
        return multipliers[self]

    @property
    def drop_rate(self):
        """Get the drop rate for this rarity level."""
        rates = {
            Rarity.COMMON: 0.50,      # 50%
            Rarity.UNCOMMON: 0.25,    # 25%
            Rarity.RARE: 0.15,        # 15%
            Rarity.EPIC: 0.07,        # 7%
            Rarity.LEGENDARY: 0.025,   # 2.5%
            Rarity.MYTHIC: 0.005      # 0.5%
        }
        return rates[self]

    @classmethod
    def from_string(cls, rarity_str):
        """Convert a string to a Rarity enum value."""
        try:
            return cls[rarity_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid rarity: {rarity_str}") 