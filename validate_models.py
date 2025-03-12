import os
import sys
from datetime import datetime
from collections import defaultdict

# Add the current directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.nft import NFT
from app.models.transaction import Transaction, TransactionType
from app.models.battle import Battle, BattleType, BattleStatus
from app.models.pve_enemy import PVEEnemy, EnemyType
from app.models.location import Location, LocationType
from app.models.user import User
from app.models.chad import Chad, ChadClass
from app.models.waifu import Waifu, WaifuType, WaifuRarity
from app.models.item import Item, ItemType, ItemRarity, CharacterItem, WaifuItem
from app.models.squad import Squad, SquadMember


def setup_environment(environment):
    """Set up a specific environment for testing."""
    config = {
        'test': {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'TESTING': True,
        },
        'dev': {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///dev.db',
            'TESTING': False,
        },
        'prod': {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///prod.db',
            'TESTING': False,
        }
    }
    
    # Create app with the appropriate config
    app = create_app(config[environment])
    return app


def init_test_data(db_session):
    """Initialize test data for validation."""
    # Create a test ChadClass
    chad_class = ChadClass(
        name='Test Class',
        description='A test Chad class',
        base_clout_bonus=1,
        base_roast_bonus=1,
        base_cringe_resistance_bonus=1,
        base_drip_bonus=1
    )
    db_session.add(chad_class)
    db_session.commit()
    
    # Create test users
    user1 = User(
        x_id='12345',
        x_username='test_user1',
        x_displayname='Test User 1',
        x_profile_image='https://example.com/user1.jpg',
        chadcoin_balance=1000
    )
    db_session.add(user1)
    
    user2 = User(
        x_id='67890',
        x_username='test_user2',
        x_displayname='Test User 2',
        x_profile_image='https://example.com/user2.jpg',
        chadcoin_balance=1000
    )
    db_session.add(user2)
    db_session.commit()
    
    # Create Chads for each user
    chad1 = Chad(
        user_id=user1.id,
        class_id=chad_class.id,
        clout=10,
        roast_level=10,
        cringe_resistance=10,
        drip_factor=10,
        level=5
    )
    db_session.add(chad1)
    
    chad2 = Chad(
        user_id=user2.id,
        class_id=chad_class.id,
        clout=8,
        roast_level=12,
        cringe_resistance=9,
        drip_factor=11,
        level=4
    )
    db_session.add(chad2)
    db_session.commit()
    
    # Create Waifu rarity and type
    waifu_rarity = WaifuRarity(
        name='Common',
        description='Common waifu rarity',
        drop_rate=0.7,
        min_stat_bonus=1,
        max_stat_bonus=3
    )
    db_session.add(waifu_rarity)
    db_session.commit()
    
    waifu_type = WaifuType(
        name='Test Waifu',
        description='A test waifu type',
        rarity_id=waifu_rarity.id,
        base_clout_bonus=1,
        base_roast_bonus=1,
        base_cringe_resistance_bonus=1,
        base_drip_bonus=1
    )
    db_session.add(waifu_type)
    db_session.commit()
    
    # Create a waifu for each user
    waifu1 = Waifu(
        user_id=user1.id,
        chad_id=chad1.id,
        type_id=waifu_type.id,
        level=1
    )
    db_session.add(waifu1)
    
    waifu2 = Waifu(
        user_id=user2.id,
        chad_id=chad2.id,
        type_id=waifu_type.id,
        level=1
    )
    db_session.add(waifu2)
    db_session.commit()
    
    # Create Item rarity and types
    item_rarity = ItemRarity(
        name='Common',
        description='Common item rarity',
        drop_rate=0.7,
        min_stat_bonus=1,
        max_stat_bonus=3
    )
    db_session.add(item_rarity)
    db_session.commit()
    
    # Character item type
    char_item_type = ItemType(
        name='Test Weapon',
        description='A test weapon',
        rarity_id=item_rarity.id,
        is_character_item=True,
        slot='weapon'
    )
    db_session.add(char_item_type)
    db_session.commit()
    
    # Create Locations
    starter_location = Location(
        name='Starter Town',
        description='The starting area',
        location_type=LocationType.STARTER.value,
        min_level=1,
        enemy_level_min=1,
        enemy_level_max=3
    )
    db_session.add(starter_location)
    db_session.commit()
    
    # Create Enemy
    enemy = PVEEnemy(
        name='Goblin',
        description='A weak goblin',
        enemy_type=EnemyType.BASIC.value,
        level=1,
        base_power=50,
        base_hp=100,
        attack_power=10,
        defense=5,
        speed=5,
        location_id=starter_location.id
    )
    db_session.add(enemy)
    db_session.commit()
    
    # Create Squad
    squad = Squad(
        name='Test Squad',
        description='A test squad',
        leader_id=chad1.id
    )
    db_session.add(squad)
    db_session.commit()
    
    # Add members to the squad
    squad.add_member(chad1.id)
    
    return {
        'users': [user1, user2],
        'chads': [chad1, chad2],
        'waifus': [waifu1, waifu2],
        'locations': [starter_location],
        'enemies': [enemy],
        'squads': [squad]
    }


def validate_nft_model(db_session, entities):
    """Validate NFT model."""
    print("Testing NFT model...")
    user = entities['users'][0]
    waifu = entities['waifus'][0]
    
    # Test minting an NFT
    token_id = "test-token-123"
    mint_tx_hash = "0xabcdef123456"
    
    nft, message = NFT.mint(
        user_id=user.id,
        entity_type="waifu",
        entity_id=waifu.id,
        token_id=token_id,
        mint_tx_hash=mint_tx_hash
    )
    
    validation_results = []
    
    # Validate NFT properties
    validation_results.append(("NFT creation", nft is not None))
    validation_results.append(("NFT token ID", nft.token_id == token_id))
    validation_results.append(("NFT entity type", nft.entity_type == "waifu"))
    validation_results.append(("NFT owner", nft.user_id == user.id))
    
    # Test NFT marketplace functionality
    success, _ = nft.list_for_sale(price=500)
    validation_results.append(("NFT listing for sale", success and nft.is_listed and nft.current_price == 500))
    
    success, _ = nft.unlist()
    validation_results.append(("NFT unlisting", success and not nft.is_listed))
    
    # Test NFT transfer
    recipient = entities['users'][1]
    success, _ = nft.transfer(to_user_id=recipient.id)
    validation_results.append(("NFT transfer", success and nft.user_id == recipient.id))
    
    # Test NFT burning
    success, _ = nft.burn()
    validation_results.append(("NFT burning", success and nft.is_burned))
    
    return validation_results


def validate_transaction_model(db_session, entities):
    """Validate Transaction model."""
    print("Testing Transaction model...")
    user1 = entities['users'][0]
    user2 = entities['users'][1]
    
    # Set initial balances
    initial_balance1 = user1.chadcoin_balance = 500
    initial_balance2 = user2.chadcoin_balance = 700
    db_session.commit()
    
    validation_results = []
    
    # Test system-generated transaction
    transaction, message = Transaction.create(
        transaction_type=TransactionType.BATTLE_REWARD.value,
        amount=100,
        to_user_id=user1.id,
        description="Battle reward test"
    )
    
    validation_results.append(("Transaction creation", transaction is not None))
    validation_results.append(("Reward transaction amount", transaction.amount == 100))
    validation_results.append(("Recipient balance update", user1.chadcoin_balance == initial_balance1 + 100))
    
    # Test user-to-user transaction
    transaction, message = Transaction.create(
        transaction_type=TransactionType.MARKETPLACE_PURCHASE.value,
        amount=200,
        from_user_id=user2.id,
        to_user_id=user1.id,
        description="Marketplace purchase test"
    )
    
    validation_results.append(("User-to-user transaction", transaction is not None))
    validation_results.append(("Sender balance update", user2.chadcoin_balance == initial_balance2 - 200))
    validation_results.append(("Recipient balance update (2)", user1.chadcoin_balance == initial_balance1 + 100 + 200))
    
    # Test invalid transaction (insufficient funds)
    transaction, message = Transaction.create(
        transaction_type=TransactionType.MARKETPLACE_PURCHASE.value,
        amount=1000,
        from_user_id=user2.id,
        to_user_id=user1.id,
        description="Should fail - insufficient funds"
    )
    
    validation_results.append(("Insufficient funds check", transaction is None and "Insufficient balance" in message))
    
    return validation_results


def validate_battle_model(db_session, entities):
    """Validate Battle model."""
    print("Testing Battle model...")
    user1 = entities['users'][0]
    user2 = entities['users'][1]
    chad1 = entities['chads'][0]
    chad2 = entities['chads'][1]
    waifu1 = entities['waifus'][0]
    waifu2 = entities['waifus'][1]
    enemy = entities['enemies'][0]
    squad = entities['squads'][0]
    
    validation_results = []
    
    # Create a PVP battle
    pvp_battle = Battle.create_pvp_battle(
        initiator_id=user1.id,
        opponent_id=user2.id,
        initiator_chad_id=chad1.id,
        opponent_chad_id=chad2.id,
        initiator_waifu_ids=[waifu1.id],
        opponent_waifu_ids=[waifu2.id]
    )
    
    validation_results.append(("PVP battle creation", pvp_battle is not None))
    validation_results.append(("PVP battle type", pvp_battle.battle_type == BattleType.PVP.value))
    
    # Test battle workflow
    success, _ = pvp_battle.start_battle()
    validation_results.append(("Battle start", success and pvp_battle.status == BattleStatus.IN_PROGRESS.value))
    
    success, _ = pvp_battle.process_battle()
    validation_results.append(("Battle processing", 
                              success and 
                              pvp_battle.status == BattleStatus.COMPLETED.value and
                              pvp_battle.winner_id is not None))
    
    # Test PVE battle
    pve_battle = Battle.create_pve_battle(
        initiator_id=user1.id,
        pve_enemy_id=enemy.id,
        initiator_chad_id=chad1.id
    )
    
    validation_results.append(("PVE battle creation", pve_battle is not None))
    validation_results.append(("PVE battle type", pve_battle.battle_type == BattleType.PVE.value))
    
    success, _ = pve_battle.start_battle()
    success, _ = pve_battle.process_battle()
    validation_results.append(("PVE battle completion", success and pve_battle.status == BattleStatus.COMPLETED.value))
    
    # Create a second squad for testing
    squad2 = Squad(
        name='Test Squad 2',
        description='A second test squad',
        leader_id=chad2.id
    )
    db_session.add(squad2)
    db_session.commit()
    squad2.add_member(chad2.id)
    
    # Test Squad battle
    squad_battle = Battle.create_squad_battle(
        initiator_squad_id=squad.id,
        opponent_squad_id=squad2.id
    )
    
    validation_results.append(("Squad battle creation", squad_battle is not None))
    validation_results.append(("Squad battle type", squad_battle.battle_type == BattleType.SQUAD.value))
    
    success, _ = squad_battle.start_battle()
    success, _ = squad_battle.process_battle()
    validation_results.append(("Squad battle completion", success and squad_battle.status == BattleStatus.COMPLETED.value))
    
    return validation_results


def validate_location_model(db_session, entities):
    """Validate Location model."""
    print("Testing Location model...")
    user = entities['users'][0]
    starter_location = entities['locations'][0]
    
    # Create another location with higher level requirement
    dungeon_location = Location(
        name='Test Dungeon',
        description='A test dungeon',
        location_type=LocationType.DUNGEON.value,
        min_level=10,
        enemy_level_min=10,
        enemy_level_max=15
    )
    db_session.add(dungeon_location)
    db_session.commit()
    
    # Connect locations
    starter_location.connected_locations = str(dungeon_location.id)
    dungeon_location.connected_locations = str(starter_location.id)
    db_session.commit()
    
    validation_results = []
    
    # Test location accessibility
    accessible, _ = starter_location.is_accessible_by_player(user)
    validation_results.append(("Starter location accessibility", accessible is True))
    
    accessible, message = dungeon_location.is_accessible_by_player(user)
    validation_results.append(("Level-restricted location", 
                              accessible is False and 
                              "Minimum level 10 required" in message))
    
    # Test location connections
    connections = starter_location.get_connected_locations()
    validation_results.append(("Location connections", 
                              len(connections) == 1 and 
                              connections[0].id == dungeon_location.id))
    
    # Create a starter location through the class method
    new_location = Location.create_location(
        name="New Area",
        location_type=LocationType.FIELD.value,
        description="A new test area",
        min_level=3
    )
    
    validation_results.append(("Location creation via class method", 
                              new_location is not None and
                              new_location.name == "New Area" and
                              new_location.min_level == 3))
    
    return validation_results


def validate_enemy_model(db_session, entities):
    """Validate PVE Enemy model."""
    print("Testing PVE Enemy model...")
    
    validation_results = []
    
    # Create different enemy types
    base_stats = {"power": 100, "hp": 200, "attack": 30, "defense": 20, "speed": 10}
    
    basic_enemy = PVEEnemy.create_enemy(
        name="Test Basic Enemy",
        enemy_type=EnemyType.BASIC.value,
        level=5,
        base_stats=base_stats
    )
    
    elite_enemy = PVEEnemy.create_enemy(
        name="Test Elite Enemy",
        enemy_type=EnemyType.ELITE.value,
        level=10,
        base_stats=base_stats
    )
    
    boss_enemy = PVEEnemy.create_enemy(
        name="Test Boss Enemy",
        enemy_type=EnemyType.BOSS.value,
        level=20,
        base_stats=base_stats
    )
    
    validation_results.append(("Enemy creation", 
                              basic_enemy is not None and
                              elite_enemy is not None and
                              boss_enemy is not None))
    
    # Test battle power scaling by type and level
    validation_results.append(("Enemy power scaling by type",
                              elite_enemy.calculate_battle_power() > basic_enemy.calculate_battle_power() and
                              boss_enemy.calculate_battle_power() > elite_enemy.calculate_battle_power()))
    
    # Test reward scaling
    low_level_player_rewards = boss_enemy.get_scaled_rewards(player_level=5)
    same_level_player_rewards = boss_enemy.get_scaled_rewards(player_level=20)
    high_level_player_rewards = boss_enemy.get_scaled_rewards(player_level=30)
    
    validation_results.append(("Enemy reward scaling by player level",
                              low_level_player_rewards["xp"] > same_level_player_rewards["xp"] and
                              same_level_player_rewards["xp"] > high_level_player_rewards["xp"]))
    
    return validation_results


def validate_models_in_environment(environment):
    """Run validation tests in a specific environment."""
    print(f"\n=== Testing in {environment.upper()} environment ===")
    
    app = setup_environment(environment)
    
    with app.app_context():
        # Reset the database for this environment
        db.drop_all()
        db.create_all()
        
        # Initialize test data
        entities = init_test_data(db.session)
        
        # Run validations
        results = []
        results.extend(validate_nft_model(db.session, entities))
        results.extend(validate_transaction_model(db.session, entities))
        results.extend(validate_battle_model(db.session, entities))
        results.extend(validate_location_model(db.session, entities))
        results.extend(validate_enemy_model(db.session, entities))
        
        # Print results
        success_count = sum(1 for _, success in results if success)
        total_count = len(results)
        
        print(f"\nResults for {environment} environment:")
        print(f"Passed: {success_count}/{total_count} tests ({success_count/total_count*100:.1f}%)")
        
        if success_count < total_count:
            print("\nFailed tests:")
            for test_name, success in results:
                if not success:
                    print(f"- {test_name}")
        
        return success_count, total_count, results


def main():
    """Main validation function."""
    environments = ['test', 'dev', 'prod']
    all_results = {}
    
    for env in environments:
        success_count, total_count, results = validate_models_in_environment(env)
        all_results[env] = {
            'success_count': success_count,
            'total_count': total_count,
            'results': results
        }
    
    # Print summary
    print("\n=== VALIDATION SUMMARY ===")
    for env in environments:
        env_results = all_results[env]
        success_rate = env_results['success_count'] / env_results['total_count'] * 100
        print(f"{env.upper()}: {env_results['success_count']}/{env_results['total_count']} tests passed ({success_rate:.1f}%)")
    
    # Check if all tests passed in all environments
    all_passed = all(
        env_results['success_count'] == env_results['total_count']
        for env_results in all_results.values()
    )
    
    if all_passed:
        print("\nALL TESTS PASSED IN ALL ENVIRONMENTS! 🎉")
        return 0
    else:
        print("\nSome tests failed. Please check the results above.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 