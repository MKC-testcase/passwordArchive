import unittest
from postgresInt import db_use, pass_repository, Base

class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MyTestCase,self).__init__(*args, **kwargs)
        self.database = db_use()

    def test_load_config(self):
        results = self.database.load_config("config.json")
        self.assertEqual(results, True)

    def test_insert_database(self):
        results = self.database.load_config("config.json")
        received = self.database.insert_entry("test_password", "portfolioTest147.com")
        self.assertEqual(received, True)

    def test_select_databaseEntry(self):
        results = self.database.load_config("config.json")
        received = self.database.select_entry(website="portfolioTest147.com")
        pw = received[0].pw
        self.assertEqual(pw, "test_password")

    def test_update_dataEntry(self):
        results = self.database.load_config("config.json")
        self.database.update_entry(website="portfolioTest147.com", update_value = "password")
        received = self.database.select_entry(website="portfolioTest147.com")
        pw = received[0].pw
        self.assertEqual(pw, "password")

    def test_delete_dataEntry(self):
        results = self.database.load_config("config.json")
        received = self.database.select_entry(website="portfolioTest147.com")
        id_number = received[0].id
        prev_pw = received[0].pw
        self.database.delete_entry(id = id_number)
        received2 = self.database.select_entry(website="portfolioTest147.com")
        if received2 == []:
            self.assertNotEqual(received2, prev_pw)
        else:
            pw = received2[0].pw
            self.assertNotEqual(prev_pw, pw)


if __name__ == '__main__':
    unittest.main()
