# БИБЛИОТЕКА ИМПОРТОВ
from aiogram.types import User
from config import db



# СВЯЗАННОЕ С ПОЛЬЗОВАТЕЛЕМ

class UserService:
    '''Класс взаимодействий с пользователем'''

    async def __init__(self, user: User, *args, **kwargs):
        self.user = user


    async def check_register(self) -> bool:
        '''Проверка пользователя на регистрацию'''

        return db.cursor().execute(f'SELECT id FROM users WHERE id = {self.user.id}').fetchone()
    

    async def add_user(self) -> None:
        db.cursor().execute(f'INSERT INTO users (id, username, full_name) VALUES (?,?,?)',
                            (self.user.id, f'@{self.user.username}', self.user.full_name))
        db.commit()