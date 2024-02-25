import sqlite3 as sq

class UserDB:    
    table_name = 'user_base'
    db = 'UserQueiries.db'
    
    def __init__(self, chat_id):
        self.conn = sq.connect(self.db, check_same_thread=False)
        self.create_table()
        self.set_id(chat_id)
        
    def create_table(self):
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                theme TEXT,
                iter INTEGER,
                line INTEGER
            )""")
    
    def set_all(self, name, value, chat_id):
        query = 'UPDATE {table_name} SET {name} = ? WHERE id = ?'.format(table_name = self.table_name ,name = name) #чтобы вставить параметры непосредственно в строку запроса
        self.conn.execute(query, (value, chat_id))
        self.conn.commit()

    def get_all(self, name, chat_id):
        query = 'SELECT {name} FROM {table_name} WHERE id = ?'.format(name = name, table_name=self.table_name)
        cursor = self.conn.execute(query, (chat_id,))

        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def set_id(self, chat_id): # Передать в конструктор message.chat.id
        try:
            self.conn.execute(f'INSERT INTO {self.table_name} (id) VALUES (?)', (chat_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Произошла ошибка, при записи chat_id в бд: {e}") 

    def set_theme(self, theme, chat_id): 
           self.set_all("theme", theme, chat_id)

    def set_iter(self, iter, chat_id): 
        self.set_all("iter", iter, chat_id)

    def set_line(self, iter, chat_id): 
        self.set_all("line", iter, chat_id)

    def get_theme(self, chat_id):
        return self.get_all("theme", chat_id)
    
    def get_iter(self, chat_id):
        return self.get_all("iter", chat_id)

    def get_line(self, chat_id):
        return self.get_all("line", chat_id)

    def clear_line(self, chat_id): # Удаляем строку в таблице
        query = ('DELETE FROM {table_name} WHERE id = (?)').format(table_name=self.table_name)
        self.conn.execute(query,(chat_id,))
        self.conn.commit()