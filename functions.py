# БИБЛИОТЕКА ИМПОРТОВ

import sqlite3
from config import dev_list



# СВЯЗАННОЕ С ПОЛЬЗОВАТЕЛЕМ

class CheckUser:

    '''Класс проверки пользователя на что-либо.'''

    async def registration(userid: int) -> bool:

        db = sqlite3.connect('database.db')
        users = db.cursor().execute('SELECT id FROM users').fetchall()
        db.close()

        reg_list = [user[0] for user in users]

        return userid in reg_list
    


class User:

    '''Класс совершения действий с пользователем.'''

    async def add_user(info_user: list[int, str, str]) -> None:

        db = sqlite3.connect('database.db')
        db.cursor().execute(f'INSERT INTO users (id, username, full_name) VALUES (?,?,?)',
                            (info_user[0], info_user[1], info_user[2]))
        db.commit()
        db.close()