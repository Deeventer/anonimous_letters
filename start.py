# БИБЛИОТЕКА ИМПОРТОВ
import logging

from aiogram.utils.executor import start_polling

import handlers
from middleware import AutoUpdate
from config import dp


# ЗАПУСК

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    logging.info(f'Handlers are loaded: {handlers}')
    logging.info(f'AutoUpdate middleware is loaded: {AutoUpdate}')

    dp.setup_middleware(middleware=AutoUpdate())

    start_polling(dispatcher=dp, 
                  skip_updates=True,
                  timeout=180)