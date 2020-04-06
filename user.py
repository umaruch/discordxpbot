import sqlite3
import os

from config import DB_NAME

class Users:
    def __init__(self):
        dirs = os.listdir()
        if DB_NAME in dirs:
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()   
        else:
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""CREATE TABLE users
                                    (
                                        user_id TEXT,
                                        messages INTEGER,
                                        voice_time TEXT,
                                        xp INTEGER
                                    )
                                """)

        print(f"Подключение к БД {DB_NAME} успешно осуществлено")


    def add_user(self, user_id, mes_n, voice_time, xp):
        self.cursor.execute(f"INSERT INTO users VALUES ({user_id},{mes_n},{voice_time},{xp})")
        self.conn.commit()

    def add_message(self, user_id):
        user = self.cursor.execute(f"SELECT messages, xp FROM users WHERE user_id={user_id}").fetchall()
        if user == []:
            self.add_user(user_id, 1, 0, 1)
        else:
            mes = int(user[0][0])+1
            xp = int(user[0][1])+1
            self.cursor.execute(f"UPDATE users SET messages={mes}, xp={xp} WHERE user_id={user_id}")
            self.conn.commit()

    def add_voice(self, user_id):
        user = self.cursor.execute(f"SELECT voice_time, xp FROM users WHERE user_id={user_id}").fetchall()
        if user == []:
            self.add_user(user_id, 0, 0.1, 2)
        else:
            voice_time = float(user[0][0])+0.1
            if (voice_time%1)*10>=6:
               voice_time += 0.4 
            xp = int(user[0][1])+2
            print(voice_time)
            self.cursor.execute(f"UPDATE users SET voice_time={voice_time}, xp={xp} WHERE user_id={user_id}")
            self.conn.commit()

    def get_info(self, user_id):
        return self.cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}").fetchall()[0]