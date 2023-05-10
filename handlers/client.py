from aiogram import types
from keyboard import kb_client
from DB import sqlite_db
# from aiogram.types import ReplyKeyboardRemove


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await message.answer(f'Привет, {message.from_user.username}!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply(
            'Общение с ботом возможно через личные сообщения! Напишите ему напрямую:\nhttps://t.me/xumpocmb_Pizza_Bot')


async def command_help(message: types.Message):
    try:
        await message.answer('/start - Начало работы с ботом\n'
                             '/help - Получить список команд\n'
                             '/режим - Узнать график работы\n'
                             '/расположение - Наш адрес\n'
                             '/меню - Просмотреть меню\n'
                             '/admin - Войти в панель администратора')
        await message.delete()
    except:
        await message.reply(
            'Общение с ботом возможно через личные сообщения! Напишите ему напрямую:\nhttps://t.me/xumpocmb_Pizza_Bot')


# @dp.message_handler(commands=['Режим'])
async def command_schedule(message: types.Message):
    await message.answer('<b>Режим работы:</b>\nПн-ПТ: 10:00-22:00\nСб-Вс: 10:00-02:00\n'
                           '<i>Без перерывов\nБез выходных</i>',
                           parse_mode='html')
    await message.delete()


# @dp.message_handler(commands=['Расположение'])
async def command_location(message: types.Message):
    await message.answer('Мы находимся по адресу: г. Город, ул. Улица, д.100')
                           # третьим параметром можно отправить reply_markup=ReplyKeyboardRemove())
    await message.delete()


# @dp.message_handler(commands=['Меню'])
async def command_menu(message: types.Message):
    await sqlite_db.sql_show_menu(message)


# регистрация handlers
def register_client_handlers(dp):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_schedule, commands=['режим'])
    dp.register_message_handler(command_location, commands=['расположение'])
    dp.register_message_handler(command_menu, commands=['меню'])
