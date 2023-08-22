from sqlalchemy import create_engine, Column, String, Integer, DateTime, select, delete, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
import json
from os import getcwd
from datetime import datetime

#http://kronosapiens.github.io/blog/2014/07/29/setting-up-unit-tests-with-flask.html

# declaring the table
Base = declarative_base()
class pass_repository(Base):
    __tablename__ = 'pass_repository'
    id = Column(Integer, primary_key=True, nullable=False)
    website = Column(String, nullable=False)
    pw = Column(String, nullable=False)
    update = Column(DateTime, nullable=False)

class db_use:
    def __init__(self):
        self.db = ""
        self.host = ""
        self.user = ""
        self.pw = ""

    def load_config(self, file):
        path = getcwd()
        if path.endswith("\\unittests"):
            path = path[:-len("\\unittests")] + "\\JSON\\"
        else:
            path = path + "\\JSON\\"
        with open(path+file) as filename:
            data = json.load(filename)
            self.user = data["DATABASE"]["USERNAME"]
            self.host = data["DATABASE"]["HOST"]
            self.db = data["DATABASE"]["DB"]
            self.pw = data["DATABASE"]["PASSWORD"]
            return True
        return False

    #def check_tb(self, tb_name):
    #    engine = create_engine('postgresql://' + self.user + ':' + self.pw + '@' + self.host + '/' + self.db)
    #    #insp = inspect(engine)
    #    return inspect(engine).has_table(tb_name)

    #def delete_tb(self, db_name):
    #    pass

    # creates the password table/ feature testing report: success visual confirmation in PgAdmin4 confirmed
    def create_tables(self):
        """
        Generates the pass_repository table that that is central to the db_use class
        :return: None
        """
        # sets up database connection based on internal class variables
        engine = create_engine('postgresql+psycopg2://' + self.user + ':' + self.pw + '@' + self.host + '/' + self.db)
        # creates table based on classes with Base, initialized at start of file
        #line that creates the table in the database
        Base.metadata.create_all(engine)


    def delete_entry(self, website=None, id=None):
        """
        Deletes a entry in the pass_repository table with associated ID
        :param id: used to identify where row to delete
        :return: Boolean to indicate success
        """
        engine = create_engine('postgresql+psycopg2://' + self.user + ':' + self.pw + '@' + self.host + '/' + self.db)
        Session = sessionmaker(engine)
        with Session() as session:
            if website != None:
                statement = delete(pass_repository).where(pass_repository.website == website)
            elif id != None:
                statement = delete(pass_repository).where(pass_repository.id == id)
            session.execute(statement)
            session.commit()
            return True

    def select_entry(self,website=None, id=None):
        """
        selects and returns the queried entries from the pass_repository table
        :param id: Parameter for user to specify id for table row
        :param website: Parameter for user to specify website for table row
        :return: List of Row Objects to access as dictionary separte row then row._mapping()
        """
        engine = create_engine('postgresql+psycopg2://' + self.user + ':' + self.pw + '@' + self.host + '/' + self.db)
        Session = sessionmaker(engine)
        with Session() as session:
            if id == None and website==None:
                return session.query(pass_repository).all()
            elif id == None:
                statement = select(pass_repository).where(pass_repository.website == website)
                return session.scalars(statement).all()
            else:
                statement = select(pass_repository).where(pass_repository.id == id)
                return session.scalars(statement).all()

    def update_entry(self, website, update_value):
        """
        Updates a variable based on the id of the update value dictionary
        :param update_value: dictionary with id, website, update, and password values
        :return: boolean
        """
        engine = create_engine('postgresql+psycopg2://'+ self.user + ':' + self.pw + "@" + self.host + '/' + self.db)
        Session = sessionmaker(engine)
        with Session() as session:
            if update_value is None:
                return False
            else:
                statement = select(pass_repository).where(pass_repository.website == website)
                row_modified = session.scalars(statement).first()
                if row_modified != None:
                    row_modified.pw = update_value
                    session.commit()
                    return True
                else:
                    return False

#may want to consider switching the order of password and website to standardize inputs
    def insert_entry(self, password, website):
        """
        inserts a new entry into the database in the PostgreSQL database
        :param password: password that has been hashed and salted
        :param website: website that is associated with the password
        :return:
        """
        engine = create_engine('postgresql+psycopg2://' + self.user + ':' + self.pw + '@' + self.host + '/' + self.db)
        Session = sessionmaker(engine)
        with Session.begin() as session:
            statement = select(pass_repository).where(pass_repository.website == website)
            row_modified = session.scalars(statement).first()
            if row_modified == None or row_modified.website == None:
                new_pw = pass_repository(website = website, update = datetime.now(), pw = password)
                session.add(new_pw)
                session.commit()
                return True
            else:
                print("Entry has already been added modifying instead")
                self.update_entry(website, password)
                return True
        return False

if __name__ == "__main__":
    test = db_use()
    # if successful returns true, else false
    results = test.load_config("config.json")
    #print(results)
    #test_rest = test.select_entry("hello_world.com")
    #print(test_rest[0].pw)
    #test.update_entry("hello_world.com", "Licking Butter")
    #test_rest = test.select_entry("hello_world.com")
    #print(test_rest[0].pw)
    test.insert_entry("check123", "hello_world.com")
    #test.delete_entry("hello_world.com")