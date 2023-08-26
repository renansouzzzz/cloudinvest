import sqlite3

class SQLite:
    def __init__(self):
        self.conn = sqlite3.connect('cloudinvest.db')
        self.cursor = self.conn.cursor()


    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS 
                                    user(
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        name VARCHAR(50) NOT NULL, 
                                        user VARCHAR(10));
                            ''')  
        
    def insert(self):
        self.cursor.execute(''' 
                            INSERT INTO user(name, user) VALUES ('Pedro Louzada', 'pelu')
                            ''');  
        
        self.cursor.execute(''' 
                            INSERT INTO user(name, user) VALUES ('Yago Giroud', 'yaguinho99')
                            ''');  
        
        self.cursor.execute(''' 
                            INSERT INTO user(name, user) VALUES ('Jesco Pereira', 'pjesco87')
                            ''');  
        
        self.cursor.execute(''' 
                            INSERT INTO user(name, user) VALUES ('Marcela Oliveira', 'mahzinha88')
                            ''');  
        
        self.cursor.execute(''' 
                            INSERT INTO user(name, user) VALUES ('João Cristiano', 'joaozin7')
                            ''');  
        
        self.conn.commit()
        
        
    def selectUsers(self):
        users = self.cursor.fetchall()
        return users    