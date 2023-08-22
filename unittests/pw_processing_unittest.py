import unittest

import bcrypt

from pw_processing import datahash_basic
from bcrypt import checkpw

class MyTestCase(unittest.TestCase):
    def test_salt_gen(self):
        state = datahash_basic()
        check = state.generate_salt()
        if not state.salt:
            check = False
        self.assertTrue(check, "Salt not generated")

    def test_password_encrypt(self):
        state = datahash_basic()
        state.encrypt_bcrypt("Hello123")
        self.assertEqual(state.encode, "\u0048\u0065\u006c\u006c\u006f\u0031\u0032\u0033", "Password not encoded properly")

    def test_hash_pw(self):
        state = datahash_basic()
        check = state.generate_salt()
        state.encrypt_bcrypt("Hello123")
        result = state.hashing()
        self.assertTrue(bcrypt.checkpw("Hello123".encode('utf-8'), result))

    def test_password_match(self):
        state = datahash_basic()
        check = state.generate_salt()
        state.encrypt_bcrypt("Hello123")
        result = state.hashing()
        self.assertTrue(state.check_password("Hello123", result))

    def test_full_run(self):
        state = datahash_basic()
        result = state.archive_pw("Hello123")
        check = state.check_password("Hello123", result)
        self.assertTrue(check, "The user simplified version failed")


if __name__ == '__main__':
    unittest.main()
