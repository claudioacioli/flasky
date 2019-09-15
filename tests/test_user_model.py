import unittest
import time
from app import db
from app.models import User, Permission, AnonymousUser, Follow


class UserModelTestCase(unittest.TestCase):
    
    def test_password_setter(self):
        u = User(password='gato')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='gato')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'gato')
        self.assertTrue(u.verify_password('gato'))
        self.assertFalse(u.verify_password('cachorro'))

    def test_password_salts_are_random(self):
        u1 = User(password='gato')
        u2 = User(password='gato')
        self.assertFalse(u1.password_hash == u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(username='teste', email='teste@teste.com', password='gato')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))
        ff = Follow.query.filter_by(follower_id=u.id).one()
        db.session.delete(ff)
        db.session.delete(u)
        db.session.commit()

    def test_invalid_confirmation_token(self):
        u1 = User(username='teste gato', email='gato@teste.com', password='gato')
        u2 = User(username='teste cachorro', email='cachorro@teste.com', password='cachorro')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

        ff1 = Follow.query.filter_by(follower_id=u1.id).one()
        ff2 = Follow.query.filter_by(follower_id=u2.id).one()
        db.session.delete(ff1)
        db.session.delete(ff2)

        db.session.delete(u2)
        db.session.delete(u1)
        db.session.commit()
    
    def test_expired_confirmation_token(self):
        u = User(username='teste galinha', email='galinha@teste.com', password='galinha')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        print(token)
        time.sleep(2)
        self.assertFalse(u.confirm(token))
        ff = Follow.query.filter_by(follower_id=u.id).one()
        db.session.delete(ff)
        db.session.delete(u)
        db.session.commit()

    def test_user_role(self):
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
        ff = Follow.query.filter_by(follower_id=u.id).one()
        db.session.delete(ff)
        db.session.delete(u)
        db.session.commit()

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

