import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models.cabal import Cabal, CabalMember, CabalOfficerRole, CabalVote, CabalBattle
from app.models.chad import Chad
from app.models.user import User
from app.utils.bot_commands import (
    handle_create_cabal, 
    handle_appoint_officer,
    handle_schedule_battle,
    handle_vote_remove_leader,
    handle_opt_in_battle
)
import uuid
from datetime import datetime, timedelta

class TestBotCabalCommands(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test users and chads
        self.test_users = []
        self.test_chads = []
        
        for i in range(5):
            user = User(
                id=str(uuid.uuid4()),
                twitter_handle=f'test_user_{i}',
                twitter_id=f'{1000+i}',
                email=f'test{i}@example.com'
            )
            db.session.add(user)
            db.session.flush()
            
            chad = Chad(
                id=str(uuid.uuid4()),
                name=f'Test Chad {i}',
                clout=10 + i,
                roast_level=20 + i,
                cringe_resistance=15 + i,
                drip_factor=25 + i
            )
            user.chad_id = chad.id
            db.session.add(chad)
            
            self.test_users.append(user)
            self.test_chads.append(chad)
        
        db.session.commit()
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    @patch('app.utils.bot_commands.twitter_api.create_tweet')
    def test_create_cabal(self, mock_create_tweet):
        """Test creating a cabal via Twitter command"""
        # Mock the tweet creation
        mock_create_tweet.return_value = {'id': '12345'}
        
        # Test creating a cabal
        response = handle_create_cabal('67890', 'test_user_0', 'TestCabal')
        
        # Check that a tweet was sent
        mock_create_tweet.assert_called_once()
        
        # Verify cabal was created
        cabal = Cabal.query.filter_by(name='TestCabal').first()
        self.assertIsNotNone(cabal)
        self.assertEqual(cabal.leader_id, self.test_chads[0].id)
        
        # Verify leader is a member
        member = CabalMember.query.filter_by(
            cabal_id=cabal.id,
            chad_id=self.test_chads[0].id
        ).first()
        self.assertIsNotNone(member)
    
    @patch('app.utils.bot_commands.twitter_api.create_tweet')
    def test_appoint_officer(self, mock_create_tweet):
        """Test appointing an officer via Twitter command"""
        # Mock the tweet creation
        mock_create_tweet.return_value = {'id': '12345'}
        
        # Create a cabal
        cabal = Cabal(
            name="Officer Test Cabal",
            description="Testing officer appointment",
            leader_id=self.test_chads[0].id
        )
        db.session.add(cabal)
        db.session.commit()
        
        # Add members
        cabal.add_member(self.test_chads[0].id)
        cabal.add_member(self.test_chads[1].id)
        
        # Test appointing an officer
        response = handle_appoint_officer('67890', 'test_user_0', 'test_user_1', 'CLOUT')
        
        # Check that a tweet was sent
        mock_create_tweet.assert_called_once()
        
        # Verify officer was appointed
        officer = cabal.get_officer('clout')
        self.assertIsNotNone(officer)
        self.assertEqual(officer.chad_id, self.test_chads[1].id)
    
    @patch('app.utils.bot_commands.twitter_api.create_tweet')
    def test_schedule_battle(self, mock_create_tweet):
        """Test scheduling a battle via Twitter command"""
        # Mock the tweet creation
        mock_create_tweet.return_value = {'id': '12345'}
        
        # Create two cabals
        cabal1 = Cabal(
            name="Battle Test Cabal 1",
            description="Testing battle scheduling",
            leader_id=self.test_chads[0].id
        )
        cabal2 = Cabal(
            name="Battle Test Cabal 2",
            description="Testing battle scheduling",
            leader_id=self.test_chads[1].id
        )
        db.session.add_all([cabal1, cabal2])
        db.session.commit()
        
        # Add members
        cabal1.add_member(self.test_chads[0].id)
        cabal2.add_member(self.test_chads[1].id)
        
        # Test scheduling a battle
        response = handle_schedule_battle('67890', 'test_user_0', 'Battle Test Cabal 2')
        
        # Check that a tweet was sent
        mock_create_tweet.assert_called_once()
        
        # Verify battle was scheduled
        battle = CabalBattle.query.filter_by(cabal_id=cabal1.id).first()
        self.assertIsNotNone(battle)
        self.assertEqual(battle.opponent_cabal_id, cabal2.id)
    
    @patch('app.utils.bot_commands.twitter_api.create_tweet')
    def test_vote_remove_leader(self, mock_create_tweet):
        """Test voting to remove a leader via Twitter command"""
        # Mock the tweet creation
        mock_create_tweet.return_value = {'id': '12345'}
        
        # Create a cabal
        cabal = Cabal(
            name="Vote Test Cabal",
            description="Testing leader removal",
            leader_id=self.test_chads[0].id
        )
        db.session.add(cabal)
        db.session.commit()
        
        # Add members
        cabal.add_member(self.test_chads[0].id)
        cabal.add_member(self.test_chads[1].id)
        
        # Test voting as a member who is not the leader
        response = handle_vote_remove_leader('67890', 'test_user_1')
        
        # Check that a tweet was sent
        mock_create_tweet.assert_called_once()
        
        # Verify vote was recorded
        vote = CabalVote.query.filter_by(
            cabal_id=cabal.id,
            voter_id=self.test_chads[1].id,
            vote_type='remove_leader'
        ).first()
        self.assertIsNotNone(vote)
    
    @patch('app.utils.bot_commands.twitter_api.create_tweet')
    def test_opt_in_battle(self, mock_create_tweet):
        """Test opting into a battle via Twitter command"""
        # Mock the tweet creation
        mock_create_tweet.return_value = {'id': '12345'}
        
        # Create a cabal
        cabal = Cabal(
            name="Opt-in Test Cabal",
            description="Testing battle opt-in",
            leader_id=self.test_chads[0].id
        )
        db.session.add(cabal)
        db.session.commit()
        
        # Add member
        cabal.add_member(self.test_chads[0].id)
        
        # Create a battle
        battle = CabalBattle(
            cabal_id=cabal.id,
            opponent_cabal_id=None,
            scheduled_at=datetime.utcnow() + timedelta(days=1),
            week_number=CabalBattle.get_current_week_number()
        )
        db.session.add(battle)
        db.session.commit()
        
        # Test opting into the battle
        response = handle_opt_in_battle('67890', 'test_user_0')
        
        # Check that a tweet was sent
        mock_create_tweet.assert_called_once()
        
        # Verify opt-in was recorded
        member = CabalMember.query.filter_by(chad_id=self.test_chads[0].id).first()
        self.assertEqual(member.daily_battles, 1)
        self.assertEqual(member.battles_participated, 1)
        
        # Check that participant record exists
        participant = CabalBattleParticipant.query.filter_by(
            battle_id=battle.id,
            chad_id=self.test_chads[0].id
        ).first()
        self.assertIsNotNone(participant)


if __name__ == '__main__':
    unittest.main() 