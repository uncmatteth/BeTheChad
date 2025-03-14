import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.utils.scheduled_tasks import send_weekly_cabal_recap, update_cabal_rankings
from app.models.cabal import Cabal, CabalMember, CabalBattle
from app.models.user import User
from app.models.chad import Chad
from app.models.referral import Referral
from app import db

class TestScheduledTasks(unittest.TestCase):
    """Test cases for scheduled tasks related to cabals."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock database session
        self.db_session_mock = MagicMock()
        
    @patch('app.models.cabal.Cabal.get_leaderboard')
    @patch('app.utils.twitter_api.share_weekly_leaderboard')
    @patch('app.utils.twitter_api.post_tweet')
    @patch('app.models.cabal.CabalBattle.query')
    @patch('app.models.cabal.CabalMember.query')
    @patch('app.models.referral.Referral.query')
    @patch('app.models.chad.Chad.query')
    @patch('app.models.user.User.query')
    def test_send_weekly_cabal_recap(self, user_query_mock, chad_query_mock, 
                                    referral_query_mock, member_query_mock, 
                                    battle_query_mock, post_tweet_mock, 
                                    share_leaderboard_mock, get_leaderboard_mock):
        """Test the weekly cabal recap function."""
        # Mock cabal data
        mock_cabal1 = MagicMock(spec=Cabal)
        mock_cabal1.id = 1
        mock_cabal1.name = "Test Cabal 1"
        mock_cabal1.level = 5
        mock_cabal1.total_power = 1000
        mock_cabal1.rank = 1
        mock_cabal1.leader_id = 101
        
        mock_cabal2 = MagicMock(spec=Cabal)
        mock_cabal2.id = 2
        mock_cabal2.name = "Test Cabal 2"
        mock_cabal2.level = 4
        mock_cabal2.total_power = 800
        mock_cabal2.rank = 2
        mock_cabal2.leader_id = 102
        
        mock_cabal3 = MagicMock(spec=Cabal)
        mock_cabal3.id = 3
        mock_cabal3.name = "Test Cabal 3"
        mock_cabal3.level = 3
        mock_cabal3.total_power = 600
        mock_cabal3.rank = 3
        mock_cabal3.leader_id = 103
        
        # Set up the mock leaderboard
        get_leaderboard_mock.return_value = [mock_cabal1, mock_cabal2, mock_cabal3]
        
        # Mock battle data
        mock_battle1 = MagicMock(spec=CabalBattle)
        mock_battle1.result = 'win'
        
        mock_battle2 = MagicMock(spec=CabalBattle)
        mock_battle2.result = 'loss'
        
        # Set up battle query filter chain
        battle_filter_mock = MagicMock()
        battle_filter_mock.all.return_value = [mock_battle1, mock_battle2]
        battle_query_mock.filter.return_value = battle_filter_mock
        
        # Mock member data
        member_filter_mock = MagicMock()
        member_filter_mock.count.return_value = 3
        member_query_mock.filter.return_value = member_filter_mock
        
        # Mock referral data
        referral_filter_mock = MagicMock()
        referral_filter_mock.count.return_value = 2
        referral_query_mock.filter.return_value = referral_filter_mock
        
        # Mock Chad and User data
        mock_chad = MagicMock(spec=Chad)
        mock_chad.id = 101
        chad_query_mock.get.return_value = mock_chad
        
        mock_user = MagicMock(spec=User)
        mock_user.twitter_handle = "test_user"
        user_filter_mock = MagicMock()
        user_filter_mock.first.return_value = mock_user
        user_query_mock.filter_by.return_value = user_filter_mock
        
        # Call the function
        result = send_weekly_cabal_recap()
        
        # Verify the function executed successfully
        self.assertTrue(result)
        
        # Verify the leaderboard was shared
        share_leaderboard_mock.assert_called_once()
        
        # Verify tweets were sent to cabal leaders
        self.assertTrue(post_tweet_mock.called)
        
    @patch('app.models.cabal.Cabal.query')
    @patch('app.models.cabal.Cabal.calculate_total_power')
    @patch('app.models.cabal.Cabal.update_rank')
    @patch('app.extensions.db.session.commit')
    def test_update_cabal_rankings(self, db_mock, update_rank_mock, 
                                  calculate_power_mock, cabal_query_mock):
        """Test the cabal rankings update function."""
        # Mock cabal data
        mock_cabal1 = MagicMock(spec=Cabal)
        mock_cabal2 = MagicMock(spec=Cabal)
        
        # Set up the mock query
        filter_mock = MagicMock()
        filter_mock.all.return_value = [mock_cabal1, mock_cabal2]
        cabal_query_mock.filter_by.return_value = filter_mock
        
        # Set up db mock
        db_mock.session = self.db_session_mock
        
        # Call the function
        result = update_cabal_rankings()
        
        # Verify the function executed successfully
        self.assertTrue(result)
        
        # Verify power was calculated for each cabal
        self.assertEqual(calculate_power_mock.call_count, 2)
        
        # Verify rank was updated for each cabal
        self.assertEqual(update_rank_mock.call_count, 2)
        
        # Verify changes were committed
        self.db_session_mock.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main() 