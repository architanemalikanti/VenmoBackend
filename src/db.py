import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        secures a connection with the database and stores it in a variable, 'conn' 
        """
        self.conn = sqlite3.connect("venmo.db", check_same_thread = False)

    def create_task_table(self):
        """
        using SQL, it creates a task table
        """
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS task(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL, 
                            username TEXT NOT NULL,
                            balance FLOAT NOT NULL
        );""")

    def delete_task_table(self):
        """
        using SQL, delete a task table. 
        """
        self.conn.execute("""
        DROP TABLE IF EXISTS task;

        """)

    #querying a value from the data table, by ID. 
    def get_user_by_id(self, user_id):
        """
        using SQL, get a user's information by their user id.
        """
        cursor = self.conn.execute("SELECT * FROM task WHERE id = ?;", (user_id))
        for row in cursor: 
            return ({"id": row[0], "name": row[1], "username": row[2], "balance": row[3]})
   
        #and if the ID doesn't exist in the database, we just return None. 
        return None
    
    #inserting a value in the database
    def insert_user(self, name, username, balance):
        """
        Using SQL, inserts a user into the user table
        """
        cursor = self.conn.execute("""
        INSERT INTO task(name, username, balance) VALUES (?, ?, ?);""", (name, username, balance))
        #saving the information in the database
        self.conn.commit()
        return cursor.lastrowid
    
    #get user by their ID (not a required database method)
    def get_user_by_id(self, user_id):
        """
        Using SQL, get a task by its ID. 
        """
        cursor = self.conn.execute("SELECT * FROM task WHERE  id = ?;", (user_id,))
        for row in cursor:
            return ({"id": row[0], "name": row[1], "username": row[2], "balance": row[3]})
        
        return None
    
    #DataBase Method (todo): updating a user's balance. 
    def update_user_balance(self, user_id, new_balance):
        """
        using SQL, updates the user's balance given the user's id and new_balance
        """
        self.conn.execute("""
        UPDATE task 
        SET balance = ?
        WHERE id = ?;
        """, (new_balance, user_id)
        )
        #save changes to the database
        self.conn.commit()


    #Database Method (todo): deleting a user. 
    def delete_user_by_id(self, user_id):
        """
        Using SQL, this deletes a user in our table
        """
        self.conn.execute("""
                            DELETE FROM task WHERE id= ?""", (user_id,))
        

    #Database method: get all users:
    def get_all_users(self):
        """
        Using SQL, retrieves all users from the task table.
        """
        cursor = self.conn.execute("SELECT * FROM task;")
        users = []
        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2], "balance": row[3]})
        return users


    




# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
