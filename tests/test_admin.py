import pytest
from flask import url_for
from app.models.user import User
from app.models.appeal import Appeal
from datetime import datetime, timedelta

def create_admin_user():
    """Helper function to create an admin user"""
    admin = User(
        username='admin',
        email='admin@chadbattles.fun',
        twitter_username='chadmin'
    )
    admin.set_password('adminpass123')
    admin.is_admin = True
    return admin

def create_regular_user():
    """Helper function to create a regular user"""
    user = User(
        username='user',
        email='user@chadbattles.fun',
        twitter_username='regularuser'
    )
    user.set_password('userpass123')
    user.chad_class = 'Exit Liquidity'
    return user

def create_appeal(user, requested_class='Blockchain Detective'):
    """Helper function to create an appeal"""
    return Appeal(
        user_id=user.id,
        requested_class=requested_class,
        reason='I deserve to be a Blockchain Detective because I found multiple rugpulls.'
    )

@pytest.mark.usefixtures('client')
class TestAdminInterface:
    def test_admin_access(self, client, db):
        """Test that only admin users can access admin pages"""
        # Create and save admin user
        admin = create_admin_user()
        db.session.add(admin)
        db.session.commit()
        
        # Test without login
        response = client.get(url_for('admin.index'))
        assert response.status_code == 302  # Redirect to login
        
        # Login as admin
        client.post(url_for('auth.login'), data={
            'username': 'admin',
            'password': 'adminpass123'
        })
        
        # Test admin access
        response = client.get(url_for('admin.index'))
        assert response.status_code == 200
        assert b'Admin Dashboard' in response.data
    
    def test_non_admin_access(self, client, db):
        """Test that non-admin users cannot access admin pages"""
        # Create and save regular user
        user = create_regular_user()
        db.session.add(user)
        db.session.commit()
        
        # Login as regular user
        client.post(url_for('auth.login'), data={
            'username': 'user',
            'password': 'userpass123'
        })
        
        # Try to access admin pages
        response = client.get(url_for('admin.index'))
        assert response.status_code == 302  # Redirect to main page
        
        response = client.get(url_for('admin.appeals'))
        assert response.status_code == 302
    
    def test_appeal_listing(self, client, db):
        """Test that appeals are listed correctly"""
        # Create users and appeals
        admin = create_admin_user()
        user = create_regular_user()
        db.session.add_all([admin, user])
        db.session.commit()
        
        appeal = create_appeal(user)
        db.session.add(appeal)
        db.session.commit()
        
        # Login as admin
        client.post(url_for('auth.login'), data={
            'username': 'admin',
            'password': 'adminpass123'
        })
        
        # Check appeals page
        response = client.get(url_for('admin.appeals'))
        assert response.status_code == 200
        assert b'Blockchain Detective' in response.data
        assert b'regularuser' in response.data
    
    def test_appeal_approval(self, client, db):
        """Test appeal approval process"""
        # Create users and appeal
        admin = create_admin_user()
        user = create_regular_user()
        db.session.add_all([admin, user])
        db.session.commit()
        
        appeal = create_appeal(user)
        db.session.add(appeal)
        db.session.commit()
        
        # Login as admin
        client.post(url_for('auth.login'), data={
            'username': 'admin',
            'password': 'adminpass123'
        })
        
        # Approve appeal
        response = client.post(url_for('admin.appeal_detail', appeal_id=appeal.id), data={
            'action': 'approve',
            'reason': 'Approved based on evidence provided'
        })
        assert response.status_code == 302  # Redirect to appeals list
        
        # Check appeal status
        appeal = Appeal.query.get(appeal.id)
        assert appeal.status == 'approved'
        assert appeal.admin_id == admin.id
        assert appeal.user.chad_class == 'Blockchain Detective'
    
    def test_appeal_rejection(self, client, db):
        """Test appeal rejection process"""
        # Create users and appeal
        admin = create_admin_user()
        user = create_regular_user()
        db.session.add_all([admin, user])
        db.session.commit()
        
        appeal = create_appeal(user)
        db.session.add(appeal)
        db.session.commit()
        
        # Login as admin
        client.post(url_for('auth.login'), data={
            'username': 'admin',
            'password': 'adminpass123'
        })
        
        # Reject appeal
        response = client.post(url_for('admin.appeal_detail', appeal_id=appeal.id), data={
            'action': 'reject',
            'reason': 'Insufficient evidence provided'
        })
        assert response.status_code == 302  # Redirect to appeals list
        
        # Check appeal status
        appeal = Appeal.query.get(appeal.id)
        assert appeal.status == 'rejected'
        assert appeal.admin_id == admin.id
        assert appeal.user.chad_class == 'Exit Liquidity'  # Class unchanged
    
    def test_appeal_status_filtering(self, client, db):
        """Test appeal filtering by status"""
        # Create users and appeals
        admin = create_admin_user()
        user = create_regular_user()
        db.session.add_all([admin, user])
        db.session.commit()
        
        # Create appeals with different statuses
        pending_appeal = create_appeal(user)
        approved_appeal = create_appeal(user, 'Tech Bro')
        rejected_appeal = create_appeal(user, 'Diamond Hands')
        
        db.session.add_all([pending_appeal, approved_appeal, rejected_appeal])
        db.session.commit()
        
        # Approve and reject appeals
        approved_appeal.approve(admin, 'Approved')
        rejected_appeal.reject(admin, 'Rejected')
        db.session.commit()
        
        # Login as admin
        client.post(url_for('auth.login'), data={
            'username': 'admin',
            'password': 'adminpass123'
        })
        
        # Check pending appeals
        response = client.get(url_for('admin.appeals', status='pending'))
        assert response.status_code == 200
        assert b'Blockchain Detective' in response.data
        assert b'Tech Bro' not in response.data
        
        # Check approved appeals
        response = client.get(url_for('admin.appeals', status='approved'))
        assert response.status_code == 200
        assert b'Tech Bro' in response.data
        assert b'Blockchain Detective' not in response.data
        
        # Check rejected appeals
        response = client.get(url_for('admin.appeals', status='rejected'))
        assert response.status_code == 200
        assert b'Diamond Hands' in response.data
        assert b'Tech Bro' not in response.data 