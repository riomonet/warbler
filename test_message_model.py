
"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    def test_message_model(self):
        """Does basic model work?"""

        text = "This is a test message"

        message = Message(text=text,user_id=1)
        db.session.add(message)
        db.session.commit()

        msg = Message.query.all()
        self.assertEqual(len(msg), 1)

        msg = Message.query.first()
        self.assertEqual(msg.text, text)


    def test_textRequired(self):
        """can a row be added if there is no text in a message?"""

        text = "This is a test message"

        message = Message(user_id=1)
        db.session.add(message)

        error = False
        try:
            db.session.commit()
        except:
            error = True
            db.session.rollback()

        self.assertTrue(error)

    def test_user_idRequired(self):
        """can a row be added if there is no user_id in a message?"""

        text = "This is a test message"

        message = Message(text=text)
        db.session.add(message)

        error = False
        try:
            db.session.commit()
        except:
            error = True
            db.session.rollback()

        self.assertTrue(error)

        
    def test_hasMessage(self):
        """if a user posts a message does it have the correct user_id in the messages table"""

        text = "This is a test message"
        
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        msg = Message(text=text)
        u1.messages.append(msg)
        res = Message.query.filter(text == text).first()
        self.assertEqual(res.user_id, u1.id)

    def test_hasNoMessage(self):
        """if user doesnt post a message then it has no message associated"""

        text = "This is a test message"
        
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="tes2t@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        
        u2.messages.append(Message(text=text))
        res = Message.query.filter(text == text).first()
        self.assertNotEqual(res.user_id, u1.id)

    def test_likedMessage(self):
        """do likes attach correctly to user and message?"""
        text = "This is a test message"
        
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        msg = Message(text=text)
        u1.messages.append(msg)
        res = Message.query.filter(text == text).first()
        u1.likes.append(msg);

        like = Likes.query.all()
        self.assertEqual(u1.id,like[0].user_id)
        self.assertEqual(res.id,like[0].message_id)
        

    def test_notLikedMessage(self):
        """are there entries for messages likes for users that didn't like them?"""
        text = "This is a test message"
        
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="tes2t@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        msg = Message(text=text)
        u1.messages.append(msg)
        u1.likes.append(msg);

        like = Likes.query.all()

        self.assertNotEqual(like[0].user_id, u2.id)

