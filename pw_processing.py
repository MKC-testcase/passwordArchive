# The purpose of this file is to augment the data with hashing before sending them into the database
import bcrypt
import json

class datahash_basic:
    def __init__(self):
        self.salt = ""
        self.encode

    def generate_salt(self):
        self.salt = bcrypt.gensalt()
        return True

    def encrypt_bcrypt(self, pw):
        self.encode = pw.encode('utf-8')
        return self.encode

    def hashing(self):
        return bcrypt.hashpw(self.encode, self.salt)

    def check_password(self, password, hash):
        self.encode = password.encode('utf-8')
        return bcrypt.checkpw(self.encode, hash)

    def archive_pw(self, password):
        self.generate_salt()
        self.encrypt_bcrypt(password)
        hashed_pw = self.hashing()
        return hashed_pw

