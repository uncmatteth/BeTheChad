# Import models to make them available and ensure proper relationships
from app.models.transaction import Transaction, TransactionType
from app.models.inventory import Inventory
from app.models.user import User
from app.models.chad import Chad, ChadClass
from app.models.waifu import Waifu
from app.models.item import Item
from app.models.rarity import Rarity
from app.models.battle import Battle, BattleResult

# Other models that might exist in your app
try:
    from app.models.cabal_analytics import CabalAnalytics
except ImportError:
    pass

try:
    from app.models.referral import Referral
except ImportError:
    pass 