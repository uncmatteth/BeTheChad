import unittest
from app import create_app, db
from app.models.user import User
from app.models.chad import Chad
from app.models.cabal import Cabal, CabalMember, CabalBattle
from flask_login import current_user
from flask import url_for
import uuid
from datetime import datetime, timedelta

class TestCabalRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        
        # Create test user and chad
        self.user = User(
            id=str(uuid.uuid4()),
            twitter_handle='test_user',
            twitter_id='12345',
            email='test@example.com'
        )
        
        self.chad = Chad(
            id=str(uuid.uuid4()),
            name='Test Chad',
            clout=10,
            roast_level=20,
            cringe_resistance=15,
            drip_factor=25
        )
        
        self.user.chad_id = self.chad.id
        db.session.add_all([self.user, self.chad])
        
        # Create additional users for testing
        self.other_users = []
        self.other_chads = []
        
        for i in range(5):
            user = User(
                id=str(uuid.uuid4()),
                twitter_handle=f'test_user_{i}',
                twitter_id=f'{1000+i}',
                email=f'test{i}@example.com'
            )
            
            chad = Chad(
                id=str(uuid.uuid4()),
                name=f'Test Chad {i}',
                clout=10 + i,
                roast_level=20 + i,
                cringe_resistance=15 + i,
                drip_factor=25 + i
            )
            
            user.chad_id = chad.id
            db.session.add_all([user, chad])
            
            self.other_users.append(user)
            self.other_chads.append(chad)
        
        db.session.commit()
        
        # Create a test cabal
        self.cabal = Cabal(
            name="Test Cabal",
            description="A test cabal",
            leader_id=self.chad.id
        )
        db.session.add(self.cabal)
        db.session.commit()
        
        # Add the leader as a member
        self.cabal.add_member(self.chad.id)
        
        # Helper to perform login
        with self.client.session_transaction() as session:
            session['_user_id'] = str(self.user.id)
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_index_route(self):
        """Test the main cabal index route"""
        response = self.client.get('/cabal/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Cabal', response.data)
    
    def test_create_cabal(self):
        """Test creating a cabal"""
        # First, remove current cabal membership
        CabalMember.query.filter_by(chad_id=self.chad.id).delete()
        db.session.delete(self.cabal)
        db.session.commit()
        
        response = self.client.post('/cabal/create', data={
            'name': 'New Test Cabal',
            'description': 'A new test cabal description'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cabal created successfully', response.data)
        self.assertIn(b'New Test Cabal', response.data)
        
        # Check database
        cabal = Cabal.query.filter_by(name='New Test Cabal').first()
        self.assertIsNotNone(cabal)
        self.assertEqual(cabal.leader_id, self.chad.id)
        self.assertEqual(cabal.member_count, 1)
    
    def test_appoint_officer(self):
        """Test appointing an officer"""
        # Add another member to the cabal
        self.cabal.add_member(self.other_chads[0].id)
        
        response = self.client.post(f'/cabal/{self.cabal.id}/appoint_officer', data={
            'chad_id': self.other_chads[0].id,
            'role_type': 'clout'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Member appointed as Clout Commander', response.data)
        
        # Check database
        officer = self.cabal.get_officer('clout')
        self.assertIsNotNone(officer)
        self.assertEqual(officer.chad_id, self.other_chads[0].id)
    
    def test_remove_officer(self):
        """Test removing an officer"""
        # Add another member and make them an officer
        self.cabal.add_member(self.other_chads[0].id)
        self.cabal.appoint_officer(self.other_chads[0].id, 'clout')
        
        response = self.client.get(f'/cabal/{self.cabal.id}/remove_officer/clout', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Officer removed from clout role', response.data)
        
        # Check database
        officer = self.cabal.get_officer('clout')
        self.assertIsNone(officer)
    
    def test_schedule_battle(self):
        """Test scheduling a battle"""
        # Create another cabal to battle against
        other_cabal = Cabal(
            name="Opponent Cabal",
            description="An opponent cabal",
            leader_id=self.other_chads[0].id
        )
        db.session.add(other_cabal)
        db.session.commit()
        
        tomorrow = datetime.utcnow() + timedelta(days=1)
        date_str = tomorrow.strftime('%Y-%m-%d')
        time_str = tomorrow.strftime('%H:%M')
        
        response = self.client.post(f'/cabal/{self.cabal.id}/schedule_battle', data={
            'opponent_cabal_id': other_cabal.id,
            'battle_date': date_str,
            'battle_time': time_str
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Battle scheduled successfully', response.data)
        
        # Check database
        battle = CabalBattle.query.filter_by(cabal_id=self.cabal.id).first()
        self.assertIsNotNone(battle)
        self.assertEqual(battle.opponent_cabal_id, other_cabal.id)
    
    def test_opt_into_battle(self):
        """Test opting into a battle"""
        # Create a battle
        battle = CabalBattle(
            cabal_id=self.cabal.id,
            opponent_cabal_id=None,
            scheduled_at=datetime.utcnow() + timedelta(days=1),
            week_number=CabalBattle.get_current_week_number()
        )
        db.session.add(battle)
        db.session.commit()
        
        response = self.client.get(f'/cabal/battle/{battle.id}/opt_in', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully opted into battle', response.data)
        
        # Check database
        member = CabalMember.query.filter_by(chad_id=self.chad.id).first()
        self.assertEqual(member.daily_battles, 1)
        self.assertEqual(member.battles_participated, 1)
    
    def test_vote_remove_leader(self):
        """Test voting to remove a leader"""
        # Add another member
        self.cabal.add_member(self.other_chads[0].id)
        
        # Login as the other user
        with self.client.session_transaction() as session:
            session['_user_id'] = str(self.other_users[0].id)
        
        response = self.client.get(f'/cabal/{self.cabal.id}/vote_remove_leader', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your vote to remove the leader has been recorded', response.data)
        
        # Check database
        vote_count = CabalVote.query.filter_by(
            cabal_id=self.cabal.id,
            vote_type='remove_leader',
            target_id=self.chad.id
        ).count()
        self.assertEqual(vote_count, 1)
    
    def test_all_battles(self):
        """Test viewing all battles"""
        # Create some battles
        for i in range(3):
            battle = CabalBattle(
                cabal_id=self.cabal.id,
                opponent_cabal_id=None,
                scheduled_at=datetime.utcnow() + timedelta(days=i+1),
                week_number=CabalBattle.get_current_week_number()
            )
            db.session.add(battle)
        
        # Add a completed battle
        past_battle = CabalBattle(
            cabal_id=self.cabal.id,
            opponent_cabal_id=None,
            scheduled_at=datetime.utcnow() - timedelta(days=1),
            completed=True,
            result='win',
            week_number=CabalBattle.get_current_week_number()
        )
        db.session.add(past_battle)
        db.session.commit()
        
        response = self.client.get('/cabal/battles')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upcoming Battles', response.data)
        self.assertIn(b'Past Battles', response.data)
    
    def test_leaderboard(self):
        """Test cabal leaderboard"""
        # Create multiple cabals with different power levels
        for i in range(3):
            cabal = Cabal(
                name=f"Leaderboard Test Cabal {i}",
                description="A test cabal for leaderboard",
                leader_id=self.other_chads[i].id,
                total_power=1000 * (i + 1)
            )
            db.session.add(cabal)
        db.session.commit()
        
        response = self.client.get('/cabal/leaderboard')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cabal Leaderboard', response.data)
        self.assertIn(b'Leaderboard Test Cabal 2', response.data)  # Highest power should be listed
    
    def test_disband_cabal(self):
        """Test disbanding a cabal"""
        cabal_id = self.cabal.id
        
        response = self.client.get(f'/cabal/{cabal_id}/disband', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cabal disbanded successfully', response.data)
        
        # Check database
        self.assertIsNone(Cabal.query.get(cabal_id))
        self.assertEqual(CabalMember.query.filter_by(cabal_id=cabal_id).count(), 0)

if __name__ == '__main__':
    unittest.main() 