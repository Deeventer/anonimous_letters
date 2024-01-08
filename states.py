# БИБЛИОТЕКА ИМПОРТОВ

from aiogram.dispatcher.filters.state import State, StatesGroup



# ОБЪЯВЛЕНИЕ ЭКЗЕМПЛЯРОВ

class SendLetter(StatesGroup):
    inter_text = State()