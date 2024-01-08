# БИБЛИОТЕКА ИМПОРТОВ

import aiogram
import sqlite3

from functions import CheckUser, User
from states import SendLetter
from config import dp, dev_list, DEVELOPER


# /START И РЕГИСТРАЦИЯ

@dp.message_handler(commands=['start', 'старт'], state='*')
async def registration(msg: aiogram.types.Message):
    if await CheckUser.registration(userid=msg.from_user.id):
        await msg.reply('Вы уже зарегистрированы!')

    else:
        info_list = [msg.from_user.id, f'@{msg.from_user.username}', msg.from_user.full_name]

        await User.add_user(info_user=info_list)
        await msg.reply('<i><b>Добро пожаловать в Anonymous Letters!</b></i>\n\n'
                        'Ознакомиться со всеми командами можно в /help или /commands. Приятного общения!')
        await msg.bot.send_message(chat_id=DEVELOPER,
                                   text='#user , #registration\n\n'
                                   f'- Инициалы: {msg.from_user.full_name}\n'
                                   f'- Юзернейм: @{msg.from_user.username}\n'
                                   f'- ID: {msg.from_user.id}')
        

# /HELP , /COMMANDS 

@dp.message_handler(commands=['help', 'commands', 'cmd', 'хелп', 'команды', 'кмд'], state='*')
async def commands(msg: aiogram.types.Message):
    if await CheckUser.registration(userid=msg.from_user.id):
        await msg.reply('<i><b>Команды:</b></i>\n\n'
                        '- /start : зарегистрироваться ;\n'
                        '- /help(/commands) : посмотреть команды бота ;\n'
                        '- /info : посмотреть информацию о боте .\n\n'
                        '- /usend [username] : отправить письмо по юзернейму ;\n'
                        '- /isend [id] : отправить письмо по айди .\n\n'
                        '- /rep : связаться с разработчиком .')
    else:
        await msg.reply('Вы не зарегистрированы! Введите /start .')


# /INFO , ИНФОРМАЦИЯ О БОТЕ

@dp.message_handler(commands=['info'], state='*')
async def information(msg: aiogram.types.Message):
    if await CheckUser.registration(userid=msg.from_user.id):
        await msg.reply('<i><b>Информация:</b></i>\n\n'
                        '- «Anonimous Letters» : это бот, позволяющий отправлять анонимные письма другим пользователям. Никто не ограничивает вас в том, что отправлять, '
                        'однако бот принимает только текстовые сообщения. Любовные признания, гневные сообщения или сплетни - всё это вы сможете отправить анонимно, не опасаясь '
                        'какого-либо презрения в вашу сторону. Начните же общение прямо сейчас!')
    else:
        await msg.reply('Вы не зарегистрированы! Введите /start .')


# /REP , СВЯЗЬ С РАЗРАБОТЧИКОМ

@dp.message_handler(commands=['rep', 'report', 'реп', 'репорт'], state='*')
async def report(msg: aiogram.types.Message):
    if msg.get_args():
        await msg.bot.send_message(chat_id=DEVELOPER,
                                   text='#user , #report\n\n'
                                   f'- Инициалы: {msg.from_user.full_name}\n'
                                   f'- Юзернейм: @{msg.from_user.username}\n'
                                   f'- ID: <code>{msg.from_user.id}</code>\n\n'
                                   f'- Текст: {msg.get_args()}\n\n'
                                   'Введите /ans [ID] [ответ] для ответа на репорт.')
        await msg.reply('Ваш репорт был успешно доставлен разработчику!')

    else:
        await msg.reply('Используйте /rep [текст]')


# /ANS , ОТВЕТ ОТ РАЗРАБОТЧИКА

@dp.message_handler(commands=['ans', 'анс'], state='*')
async def answer(msg: aiogram.types.Message):
    if msg.from_user.id == DEVELOPER and msg.get_args():
        args = msg.get_args().split(sep=' ')
        if len(args) < 2:
            await msg.reply('Неверно вставлены аргументы. Пожалуйста, используйте шаблон.')
        
        else:
            
            try:
                user_id = args[0]
                user_id = int(user_id)

                answer_on_report = " ".join(args[1:])

                await msg.bot.send_message(chat_id=user_id,
                                           text='<b><i>Новое сообщение от разработчика!</i></b>\n\n'
                                           f'{answer_on_report}')
                await msg.reply('Ответ был успешно доставлен!')

            except ValueError:
                await msg.reply('Неверный ID.')
    
    elif msg.from_user.id != DEVELOPER:
        await msg.reply('Доступно только разработчику.')
    
    elif not msg.get_args():
        await msg.reply('Введите /ans [ID] [ответ]')
    


# /USEND , ОТПРАВКА ПИСЬМА ПО ЮЗЕРНЕЙМУ

@dp.message_handler(commands='usend', state='*')
async def username_send(msg: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if await CheckUser.registration(userid=msg.from_user.id) and msg.get_args():
        
        db = sqlite3.connect('database.db')
        users = db.cursor().execute('SELECT username, id FROM users').fetchall()
        db.close()

        founded = []
        
        for username, id in users:
            if username == msg.get_args():
                founded.append(id)
            else:
                pass

        if len(founded) == 0:
            await msg.reply('Указанный пользователь не зарегистрирован, либо введён неверный юзернейм.')
        
        else:
            await SendLetter.inter_text.set()
            await state.update_data(id=founded[0])
            await msg.reply('Пользователь был успешно найден! Введите текст письма.')

    elif not msg.get_args():
        await msg.reply('Используйте /usend [username]')

    else:
        await msg.reply('Вы не зарегистрированы! Введите /start .')


# /ISEND , ОТПРАВКА ПИСЬМА ПО АЙДИ

@dp.message_handler(commands='isend', state='*')
async def username_send(msg: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if await CheckUser.registration(userid=msg.from_user.id) and msg.get_args():

        try:
            user_id = int(msg.get_args())

            db = sqlite3.connect('database.db')
            users = db.cursor().execute('SELECT id FROM users WHERE').fetchall()
            db.close()

            registred_users = [user[0] for user in users]
            
            if user_id in registred_users:
                await SendLetter.inter_text.set()
                await state.update_data(id=user_id)
                await msg.reply('Пользователь был успешно найден! Введите текст письма.')
            
            else:
                await msg.reply('Указанный пользователь не зарегистрирован.')

        except ValueError:
            await msg.reply('Введён неверный ID. Он должен состоять только из цифр.')
        
    elif not msg.get_args():
        await msg.reply('Используйте /isend [ID]')

    else:
        await msg.reply('Вы не зарегистрированы! Введите /start .')


# ОТПРАВКА ТЕКСТА ДЛЯ ПИСЬМА

@dp.message_handler(state=SendLetter.inter_text)
async def inter_text_to_letter(msg: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    await state.update_data(text=msg.text)
    await msg.reply('Ваш текст записан. Подтвердите отправку сообщения.',
                    reply_markup=aiogram.types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [aiogram.types.InlineKeyboardButton(text='Отправить', callback_data='let:send'),
                             aiogram.types.InlineKeyboardButton(text='Отмена', callback_data='let:cancel')]]))
    

# ПОДТВЕРЖДЕНИЕ ОТПРАВКИ

@dp.callback_query_handler(aiogram.filters.Text(startswith='let:'), state=SendLetter.inter_text)
async def sumbit_send_letter(query: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    answer_from_user = query.data.split(sep=':')

    if answer_from_user[1] == 'send':
        
        user = await state.get_data()

        await query.bot.send_message(chat_id=user["id"],
                                     text=f'Тебе пришло анонимное письмо!\n\n{user["text"]}')
        if user["id"] in dev_list:
            await query.bot.send_message(chat_id=user["id"],
                                         text=f'Отправлено пользователем: <a href="{query.from_user.url}">{query.from_user.full_name}</a>.')
        else:
            pass

        await query.answer()
        await query.message.edit_text(text='Письмо успешно доставлено!')
        await state.reset_state(with_data=True)

    elif answer_from_user[1] == 'cancel':
        await state.reset_state(with_data=True)
        await query.message.edit_text(text='Отправка письма успешно отменена!')