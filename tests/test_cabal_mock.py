import unittest
import uuid
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

class TestCabalMock(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create mock IDs for testing
        self.test_chad_ids = [str(uuid.uuid4()) for _ in range(5)]
        self.cabal_id = str(uuid.uuid4())
        
        # Create a mock cabal class
        self.mock_cabal = MagicMock()
        self.mock_cabal.id = self.cabal_id
        self.mock_cabal.name = "Test Cabal"
        self.mock_cabal.description = "A test cabal"
        self.mock_cabal.leader_id = self.test_chad_ids[0]
        self.mock_cabal.level = 1
        self.mock_cabal.xp = 0
        self.mock_cabal.invite_code = "ABC123"
        self.mock_cabal.member_count = 0
        
        # Mock the add_member method
        def mock_add_member(chad_id):
            if chad_id in self.mock_members:
                return False, "Member already in cabal"
            self.mock_members.append(chad_id)
            self.mock_cabal.member_count = len(self.mock_members)
            return True, "Member added successfully"
        
        self.mock_cabal.add_member = mock_add_member
        
        # Mock the remove_member method
        def mock_remove_member(chad_id):
            if chad_id == self.mock_cabal.leader_id:
                return False, "Cannot remove leader"
            if chad_id not in self.mock_members:
                return False, "Member not in cabal"
            self.mock_members.remove(chad_id)
            self.mock_cabal.member_count = len(self.mock_members)
            return True, "Member removed successfully"
        
        self.mock_cabal.remove_member = mock_remove_member
        
        # Mock members list
        self.mock_members = []
        
        # Mock officers
        self.mock_officers = {}
        
        # Mock the appoint_officer method
        def mock_appoint_officer(chad_id, role):
            if chad_id == self.mock_cabal.leader_id:
                return False, "Cannot appoint leader as officer"
            if chad_id not in self.mock_members:
                return False, "Member not in cabal"
            if role not in ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']:
                return False, "Invalid officer role"
            
            # Create mock officer
            mock_officer = MagicMock()
            mock_officer.cabal_id = self.cabal_id
            mock_officer.chad_id = chad_id
            mock_officer.role = role
            
            self.mock_officers[role] = mock_officer
            return True, f"Officer appointed for {role}"
        
        self.mock_cabal.appoint_officer = mock_appoint_officer
        
        # Mock the get_officer method
        def mock_get_officer(role):
            return self.mock_officers.get(role)
        
        self.mock_cabal.get_officer = mock_get_officer
    
    def test_cabal_creation(self):
        """Test basic cabal properties"""
        # Check basic properties
        self.assertEqual(self.mock_cabal.name, "Test Cabal")
        self.assertEqual(self.mock_cabal.description, "A test cabal")
        self.assertEqual(self.mock_cabal.leader_id, self.test_chad_ids[0])
        self.assertEqual(self.mock_cabal.level, 1)
        self.assertEqual(self.mock_cabal.xp, 0)
        self.assertEqual(self.mock_cabal.invite_code, "ABC123")
        self.assertEqual(self.mock_cabal.member_count, 0)
    
    def test_add_member(self):
        """Test adding members to a cabal"""
        # Add leader as member
        success, message = self.mock_cabal.add_member(self.test_chad_ids[0])
        self.assertTrue(success)
        self.assertEqual(self.mock_cabal.member_count, 1)
        
        # Add another member
        success, message = self.mock_cabal.add_member(self.test_chad_ids[1])
        self.assertTrue(success)
        self.assertEqual(self.mock_cabal.member_count, 2)
        
        # Try to add the same member again
        success, message = self.mock_cabal.add_member(self.test_chad_ids[1])
        self.assertFalse(success)
        self.assertEqual(self.mock_cabal.member_count, 2)
    
    def test_remove_member(self):
        """Test removing members from a cabal"""
        # Add members
        self.mock_cabal.add_member(self.test_chad_ids[0])
        self.mock_cabal.add_member(self.test_chad_ids[1])
        
        # Try to remove the leader (should fail)
        success, message = self.mock_cabal.remove_member(self.test_chad_ids[0])
        self.assertFalse(success)
        self.assertEqual(self.mock_cabal.member_count, 2)
        
        # Remove a regular member
        success, message = self.mock_cabal.remove_member(self.test_chad_ids[1])
        self.assertTrue(success)
        self.assertEqual(self.mock_cabal.member_count, 1)
    
    def test_appoint_officer(self):
        """Test appointing officers"""
        # Add members
        self.mock_cabal.add_member(self.test_chad_ids[0])
        self.mock_cabal.add_member(self.test_chad_ids[1])
        
        # Appoint an officer
        success, message = self.mock_cabal.appoint_officer(self.test_chad_ids[1], 'clout')
        self.assertTrue(success)
        
        # Verify officer was appointed
        officer = self.mock_cabal.get_officer('clout')
        self.assertIsNotNone(officer)
        self.assertEqual(officer.chad_id, self.test_chad_ids[1])
        
        # Try to appoint the leader (should fail)
        success, message = self.mock_cabal.appoint_officer(self.test_chad_ids[0], 'roast_level')
        self.assertFalse(success)
        
        # Try to appoint invalid role
        success, message = self.mock_cabal.appoint_officer(self.test_chad_ids[1], 'invalid_role')
        self.assertFalse(success) 