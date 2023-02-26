import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    all = []
    

    def __init__(self, name, breed, id=None):
        '''initializes with name and breed attributes, and id attribute'''
        self.id = id
        self.name = name
        self.breed = breed
    

    @classmethod
    def create_table(cls):
        '''contains method "create_table()" that creates table "dogs" if it does not exist.'''
        sql = """
            create table if not exists dogs (
                id integer primary key,
                name text,
                breed text
            )
        """
        CURSOR.execute(sql)

    
    @classmethod
    def drop_table(cls):
        '''contains method "drop_table()" that drops table "dogs" if it exists.'''
        sql = """
            drop table if exists dogs

        """
        CURSOR.execute(sql)

    
    
    def save(self):
        '''contains method "save()" that saves/insert a Dog instance to the database.'''
        sql = """
            insert into dogs (name, breed)
            values (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))

        # find the matched row in db with name = self.name
        # self.id = CURSOR.execute("select dogs.id from dogs where dogs.name = ? ", (self.name,)).fetchone()[0]
        
        # returns the last inserted rowid
        self.id = CURSOR.lastrowid


    @classmethod
    def create(cls, name, breed):
        '''contains method "create()" that creates a new row in the database and returns a Dog instance.'''
        # dog = Dog.create("name", "breed")
        dog = cls(name, breed)      # create new instance
        dog.save()                  # save the new instance into db by calling save() which inserts the instance to db
        return dog

    
    @classmethod
    def new_from_db(cls, row):
        '''contains method "new_from_db()" that takes a database row and creates a Dog instance.'''
        dog = cls(row[1], row[2])      # song = Song(row[1], row[2])
        dog.id = row[0]
        return dog


    @classmethod
    def get_all(cls):
        '''contains method "get_all()" that returns a list of Dog instances for every record in the database.'''
        
        sql = """
            select * from dogs
        """
        all = CURSOR.execute(sql).fetchall()    # fetch all rows in db, save it to all variable
        cls.all = [cls.new_from_db(row) for row in all] # convert each row get back from db into python obj using new_from_db(), assgin the results to class attr "all"
        return cls.all

    
    @classmethod
    def find_by_name(cls, name):
        '''contains method "find_by_name()" that returns a Dog instance corresponding to its database record retrieved by name.'''
        
        sql = """
            select * from dogs where name = ? limit 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)


    @classmethod
    def find_by_id(cls, id):
        '''contains method "find_by_id()" that returns a Dog instance corresponding to its database record retrieved by id.'''
        
        sql = """
            select * from dogs where id = ? 
        """

        dog = CURSOR.execute(sql, (id,)).fetchone()

        return cls.new_from_db(dog)


    @classmethod
    def find_or_create_by(cls, name, breed):
        '''contains method "find_or_create_by()" that takes a name and a breed as arguments and creates a Dog instance matching that record if it does not exist.'''
        
        sql = """
            select * from dogs where name = ? and breed = ?
        """

        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if dog:
            return cls.new_from_db(dog)         # convert that row into python obj
        else:
            new_dog = cls.create(name, breed) # save new dog into db
            return new_dog                    # return new_dog

    # def update(self):
    #     '''contains a method "update()" that updates an instance's corresponding database record to match its new attribute values.'''
    #     sql = """
    #         update dogs
    #         set name = ?, breed = ?
    #         where id = ?
    #     """
    #     updated_dog = CURSOR.execute(sql, (self.name, self.breed, self.id))
    #     return updated_dog
