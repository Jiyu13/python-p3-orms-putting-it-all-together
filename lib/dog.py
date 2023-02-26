import sqlite3

CONN = sqlite3.connect('dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        '''initializes with name and breed attributes.'''
        self.name = name
        self.breed = breed
        self.id = id


    @classmethod
    def create_table(cls):
        '''
            contains method "create_table()" that creates table "dogs" if it does not exist.
            set self.id = None
        '''
        query = """
            create table if not exists dogs (
                id integer primary key,
                name text,
                breed text
            )
        """
        CURSOR.execute(query)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        '''contains method "drop_table()" that drops table "dogs" if it exists.'''
        query = """
            drop table if exists dogs
        """
        CURSOR.execute(query)
        CONN.commit()


    def save(self):
        '''contains method "save()" that saves a Dog instance to the database.'''
        query = """
            insert into dogs (name, breed)
            values (?, ?)
        """
        CURSOR.execute(query, (self.name, self.breed))
        self.id = CURSOR.lastrowid
        CONN.commit()

    
    
    @classmethod
    def create(cls, name, breed):
        '''contains method "create()" that creates a new row in the database and returns a Dog instance.'''
        new_dog = Dog(name, breed)
        new_dog.save()
        return new_dog


    @classmethod
    def new_from_db(cls, row):
        '''contains method "new_from_db()" that takes a database row and creates a Dog instance.'''
        dog_from_db = cls(
            id=row[0],
            name=row[1],
            breed=row[2]
        )

        return dog_from_db
        # if not set id=None => def __init__(self, name, breed)


        # dog = cls(row[1], row[2])
        # dog.id = row[0]
        # return dog
        
    

    @classmethod
    def get_all(cls):
         '''contains method "get_all()" that returns a list of Dog instances for every record in the database.'''
         query = """
            select * from dogs
         """

         all_rows = CURSOR.execute(query).fetchall()
         
         return [cls.new_from_db(row) for row in all_rows]
    

    @classmethod
    def find_by_name(cls, name):
        '''contains method "find_by_name()" that returns a Dog instance corresponding to its database record retrieved by name.'''
        query = """
            select * from dogs where name = ? limit 1
        """

        find_row = CURSOR.execute(query, (name,)).fetchone()
        if find_row:
            return cls.new_from_db(find_row)
        else: 
            return None

    
    @classmethod
    def find_by_id(cls, id):
        '''contains method "find_by_id()" that returns a Dog instance corresponding to its database record retrieved by id.'''

        query = """
            select * from dogs where id = ? limit 1
        """

        find_row = CURSOR.execute(query, (id,)).fetchone()
        if find_row:
            return cls.new_from_db(find_row)
        else:
            return None
    

    @classmethod
    def find_or_create_by(cls, name, breed):
        '''
            contains method "find_or_create_by()" that takes a name and a breed as arguments and creates a Dog instance matching that record if it does not exist.
            # select * from dogs where (name, breed) = (?, ?) limit 1
        '''    
        
        query = """
            select * from dogs where name = ? and breed = ? limit 1
        """
        find_row = CURSOR.execute(query, (name, breed)).fetchone()

        if find_row:
            return cls.new_from_db(find_row)
        else:
            # automatically create new row and instance if not in db
            print("not found!")
            return cls.create(name, breed)
            
            # answer from lecture, not persist to db
            # query = """
            #     insert into dogs (name, breed)
            #     values (?, ?)
            # """
            # CURSOR.execute(query, (name, breed))
            # return cls.find_by_name(name)



    def update(self):
        query = """
            update dogs
            set name = ?, breed = ? where id = ?
        """

        CURSOR.execute(query, (self.name, self.breed, self.id))
        
        # commit() to make the update persist in db
        CONN.commit()

        #  dog = Dog.find_by_name/id()
        #  change dog.name/id = ""
        #  dog.update()

    