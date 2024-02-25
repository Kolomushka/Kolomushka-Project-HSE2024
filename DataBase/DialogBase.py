import sys
import os
import time
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from Commands.GlobalData import GlobalData
import sqlite3 as sq

class DialogDB:
    def __init__(self, name):
        self.table_name = name
        self.conn = sq.connect('UserQueiries.db', check_same_thread=False) # В базе данных dialog будет таблица на каждую тему
        self.create_table()
        self.gd = GlobalData()
        for el in self.gd.hard_cortege:
            self.set_id(self.gd.switch_hard_num(el))

    def create_table(self): # Создаем в нашей базе новую таблицу self.table_name = theme | автоинкремент
        query = """ 
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                iterator INTEGER DEFAULT 1
            )
        """.format(table_name=self.table_name)
        self.conn.execute(query)

    def check_value_in_table(self, name, id):
        try:
            query = f'SELECT {name} FROM {self.table_name} WHERE id = ?'
            cursor = self.conn.execute(query, (id,))
            result = cursor.fetchone()

            if result is None or result[0] is None:
                return True  # Поле пустое
            else:
                return False
        
        except Exception as e:
            print(f"check_value_in_table DialogBase error: {e}")
            return True

    # ОСТОРОЖНО в использовании, если поля нет -> будет создано
    def set_replica(self, column, id, value):
        query = 'UPDATE {table_name} SET {column} = ? WHERE id = ?'.format(table_name=self.table_name, column=column)
        try:
            with self.conn:
                self.conn.execute(query, (value, id))
        except sq.OperationalError as e:
            #print(f"Error updating {column} for {id}: {e}")
            if "no such column" in str(e):
                #print(f"Column {column} does not exist. Adding new field.")
                self.add_new_field(column, 'TEXT')
                try:
                    with self.conn:
                        self.set_replica(column, id, value)
                except sq.OperationalError as ex:
                    pass
                #   print(f"Error updating {column} after adding the new field: {ex}")
            else:
                print(f"Unhandled error: {e}")

    def set_id(self, id): # тк автоинкремент у id => автоматически идет приращение
        query = 'SELECT id FROM {table_name} WHERE id = ?'.format(table_name=self.table_name)
        cursor = self.conn.execute(query, (3,))        
        result = cursor.fetchone()

        if result:
            print('Запись',id,'в',self.table_name,'уже есть')
        else:
            try:
                query = 'INSERT INTO {table_name} (id) VALUES (?)'.format(table_name=self.table_name)
                self.conn.execute(query, (id,))
                self.conn.commit()
            except Exception as e:
                print(f"set_id DialogBase error: {e}")

    # Приращение итератора, используем для подсчета кол-ва реплик в диалоге                
    def increment_iterator(self, id):
        query = 'UPDATE {table_name} SET iterator = iterator + 1 WHERE id = ?'.format(table_name=self.table_name)
        self.conn.execute(query, (id,))
        self.conn.commit()

    # Эта штука только для объектов конкретных таблиц
    def get_iterator(self, id):
        query = 'SELECT iterator FROM {table_name} WHERE id = ?'.format(table_name=self.table_name)
        cursor = self.conn.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return 1 # Иначе значение по умолчанию

    # Взять любое поле таблицы
    def get_value(self, id, column):
        query = 'SELECT {} FROM {} WHERE id = ?'.format(column, self.table_name)
        try:
            cursor = self.conn.execute(query, (id,))
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                return -1
        except Exception as e:
            print(f"Error executing query: {e}")
            return -1

    # Добавляем новый столбец с указанным типом данных и именем
    def add_new_field(self, field_name, field_type):
        try:
            query = 'ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type}'.format(
                table_name=self.table_name, field_name=field_name, field_type=field_type
            )
            self.conn.execute(query)
            self.conn.commit()
        except sq.OperationalError as e:
            if "already exists" in str(e):
                print(f"Column {field_name} already exists.")
            else:
                print(f"Error: {e}")

    #--------------------Запись из файлов ----------------------
    def table_entry(self):
        current_dir = os.path.dirname(__file__)
        dialog_text_dir = os.path.join(os.path.dirname(current_dir), "DialogText")

        # Потом в DialogBase как метод, когда все ок будет
        for hard in self.gd.hard_cortege:
            file_name = f"{self.table_name}{self.gd.switch_hard_key(hard)}.txt" # Имя файла: ThemeAHardB, Где A & B - цифры
            file_path = os.path.join(dialog_text_dir, file_name)
            
            hard_num = self.gd.switch_hard_num(hard)

            with open(file_path, "r") as file: # Изменить на r а то плохо
                lines = file.readlines() # Считываем строки
                
                goStop = self.check_value_in_table('bot_replica1',hard_num)
                if goStop:
                # --------------------- ДОБАВИТЬ ПРОВЕРКУ НА есть значения в ПОЛЕ, если есть то break нахуй
                    for i, line in enumerate(lines, start=1):  

                        # Тут все ок, вопрос с записью в бд
                        if line.startswith('/'):  # Из темы в цикле фор получаем id в бд, по id находим итератор -> узнаем номер реплики
                            bot_replica_field = f'bot_replica{self.get_iterator(hard_num)}' 
                            self.set_replica(bot_replica_field, hard_num, line[1:].strip())
            
                        elif line.startswith('+'):
                            correct_reply_field = f'correct_reply{self.get_iterator(hard_num)}'
                            self.set_replica(correct_reply_field, hard_num, line[1:].strip())

                        elif line.startswith('-'):
                            user_reply1_1_field = f'user_reply{self.get_iterator(hard_num)}_1'
                            self.set_replica(user_reply1_1_field, hard_num, line[1:].strip())

                        elif line.startswith('_'):
                            user_reply1_2_field = f'user_reply{self.get_iterator(hard_num)}_2'
                            self.set_replica(user_reply1_2_field, hard_num, line[1:].strip())

                        elif line.startswith('$'):
                            self.increment_iterator(hard_num)
                else:
                    print("Запись в", self.table_name, hard, "уже есть")