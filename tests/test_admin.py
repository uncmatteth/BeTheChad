import pytest
from flask import url_for
from app.models.user import User
from app.models.appeal import Appeal
from datetime import datetime, timedelta
import os

# Force SQLite for these tests
os.environ['TEST_DATABASE_URI'] = 'sqlite:///:memory:'

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

def create_appeal(user, requested_class='Blockchain Detective', days_ago=0):
    """Helper function to create an appeal"""
    appeal = Appeal(
        user_id=user.id,
        requested_class=requested_class,
        reason='I deserve to be a Blockchain Detective because I found multiple rugpulls.',
        created_at=datetime.utcnow() - timedelta(days=days_ago)
    )
    return appeal

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
        }, follow_redirects=True)
        
        # Test access after login
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

    def test_appeal_rate_limiting(self, client, db):
        """Test that users can only submit one appeal per month"""
        user = create_regular_user()
        db.session.add(user)
        db.session.commit()

        # Create an appeal from 15 days ago
        old_appeal = create_appeal(user, days_ago=15)
        db.session.add(old_appeal)
        db.session.commit()

        # Login as user
        client.post(url_for('auth.login'), data={
            'username': 'user',
            'password': 'userpass123'
        }, follow_redirects=True)

        # Try to create another appeal
        response = client.post(url_for('admin.submit_appeal'), data={
            'requested_class': 'Blockchain Detective',
            'reason': 'Another attempt'
        }, follow_redirects=True)

        assert response.status_code == 403
        assert b'You can only submit one appeal per month' in response.data

    def test_environment_specific_callback(self, client):
        """Test that Twitter callback URL is environment-specific"""
        # Test development environment
        with client.application.app_context():
            client.application.config['ENV'] = 'development'
            callback_url = url_for('auth.twitter_callback', _external=True)
            assert 'localhost' in callback_url or '127.0.0.1' in callback_url

        # Test production environment
        with client.application.app_context():
            client.application.config['ENV'] = 'production'
            callback_url = url_for('auth.twitter_callback', _external=True)
            assert 'chadbattles.fun' in callback_url

    def test_admin_notification(self, client, db):
        """Test that admins are notified of new appeals"""
        admin = create_admin_user()
        user = create_regular_user()
        db.session.add_all([admin, user])
        db.session.commit()

        # Login as user
        client.post(url_for('auth.login'), data={
            'username': 'user',
            'password': 'userpass123'
        }, follow_redirects=True)

        # Submit an appeal
        response = client.post(url_for('admin.submit_appeal'), data={
            'requested_class': 'Blockchain Detective',
            'reason': 'Testing notifications'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Login as admin
        client.post(url_for('auth.login'), data={
            'username': 'admin',
            'password': 'adminpass123'
        }, follow_redirects=True)

        # Check admin dashboard for notification
        response = client.get(url_for('admin.index'))
        assert b'New Appeal' in response.data
        assert b'Testing notifications' in response.data 