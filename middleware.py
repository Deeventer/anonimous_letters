# БИБЛИОТЕКА ИМПОРТОВ
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from config import db


# ЭКЗЕМПЛЯРЫ

class AutoUpdate(BaseMiddleware):

    async def on_pre_process_message(self, msg: Message, *args, **kwargs):
        info_user = db.cursor().execute(f'SELECT username, full_name FROM users WHERE id = {msg.from_user.id}').fetchall()

        for username, full_name in info_user:
            if username == f'@{msg.from_user.username}' and full_name == msg.from_user.full_name:
                pass

            elif username != f'@{msg.from_user.username}':
                db.cursor().execute(f'UPDATE users SET username = "@{msg.from_user.username}" WHERE id = {msg.from_user.id}')
                db.commit()

            elif full_name != msg.from_user.full_name:
                db.cursor().execute(f'UPDATE users SET full_name = "{msg.from_user.full_name}" WHERE id = {msg.from_user.id}')
                db.commit()

        return True