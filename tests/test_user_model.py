import unittest
from app.models import User


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