"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.likes),0)
        self.assertTrue(User.query.filter(User.username =="testuser").all())

    
    def test2(self):
        """crashes on missing required email field need to catch this error"""

        u = User(
            username="dummy",
            password="nu")
        db.session.add(u)

        error = False
        try:
            db.session.commit()
        except:
            error = True
            db.session.rollback()

        self.assertTrue(error)
        self.assertFalse(User.query.filter(User.username =="dummy").all())

    def test_isFollowing(self):

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()        
        u1.following.append(u2)
        self.assertTrue(u1.is_following(u2))


    def test_repr(self):

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.__repr__(), f"<User #{u1.id}: {u1.username}, {u1.email}>")



    def test_notFollowing(self):

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()        
        self.assertFalse(u1.is_following(u2))

    def test_isFollowedBy(self):

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()        
        u2.following.append(u1)
        self.assertTrue(u1.is_followed_by(u2))
        

    def test_isNotFollowedBy(self):

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()        
        self.assertFalse(u1.is_followed_by(u2))




    def test_Authenticate(self):

        password = "HASHED_PASSWORD"
        hashed_Pw= bcrypt.generate_password_hash(password).decode('UTF-8')

        u1 = User(
            email="test@test.com",
            username="testuser",
            password = hashed_Pw
        )
        db.session.add(u1)
        db.session.commit()
        u = User.query.filter_by(username="testuser").first()

        self.assertTrue(User.authenticate("testuser",password),
                        f"<User #{u.id}: {u.username}, {u.email}>")
        

    def test_InvalidUsername(self):

        password = "HASHED_PASSWORD"
        hashed_Pw= bcrypt.generate_password_hash(password).decode('UTF-8')

        u1 = User(
            email="test@test.com",
            username="testuser",
            password = hashed_Pw
        )
        db.session.add(u1)
        db.session.commit()
        u = User.query.filter_by(username="testuser").first()

        self.assertFalse(User.authenticate("wronguser",password))

        
    def test_InvalidPassWord(self):

        password = "HASHED_PASSWORD"
        wrongPassword = "WRONG_PASSWORD"
        hashed_Pw= bcrypt.generate_password_hash(password).decode('UTF-8')

        u1 = User(
            email="test@test.com",
            username="testuser",
            password = hashed_Pw
        )
        db.session.add(u1)
        db.session.commit()
        u = User.query.filter_by(username="testuser").first()

        self.assertFalse(User.authenticate("testuser",wrongPassword))

        


        
        
