from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from DB import sqlite_db
from keyboard import admin_keyboard

u_ID = None


# записываем классы состояний
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# получаем ID текущего пользователя (проверка на админа в чате группы)
# @dp.message_handler(commands=['admin'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global u_ID
    try:
        u_ID = message.from_user.id
        await message.reply('Что пожелаете?', reply_markup=admin_keyboard.button_case_admin)
        await message.delete()
    except:
        await message.reply(
            'Общение с ботом возможно через личные сообщения! Напишите ему напрямую:\nhttps://t.me/xumpocmb_Pizza_Bot')
        await message.delete()


# начало диалога загрузки
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == u_ID:
        await FSMAdmin.photo.set()
        await message.reply('Пришлите фото:')


# выход из состояний
# выход из состояний должен быть выше, чтобы был приоритет срабатвания
# @dp.message_handler(state='*', commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == u_ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


# обработка первого ответа
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == u_ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Напишите название:')


# обработка второго ответа
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == u_ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Напишите описание:')


# обработка третьего ответа
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == u_ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Напишите стоимость:')


# обработка четвертого ответа
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == u_ID:
        async with state.proxy() as data:
            data['price'] = message.text.replace(',', '.')
        # перед командой state.finish() мы должны проделать операцию с данными (записать в БД)
        # для теста выведем в чат
        await sqlite_db.sql_add_command(state)
        await bot.send_message(message.from_user.id, '[+] Запись добавлена!')
        print('[+] Запись добавлена!')
        await state.finish()


# @dp.callback_query_handler(lambda x: x.data and x.data.startwith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена!', show_alert=True)


# @dp.message.handler(commands='Удалить')
async def delete_record(message: types.Message):
    if message.from_user.id == u_ID:
        read = await sqlite_db.sql_show_all_data()
        for i in read:
            await bot.send_photo(message.from_user.id, i[0], f'{i[1]}\nОписание: {i[2]}\nЦена: {i[3]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {i[1]}', callback_data=f'del {i[1]}')))


# регистрация handlers
def register_admin_handlers(dp):
    # обработка команд
    dp.register_message_handler(cm_start, commands=['загрузить'], state=None)
    # регистрация handlers выхода из состояний. состояние выхода должно быть выше, чтобы был приоритет срабатывания
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(delete_record, commands=['Удалить'])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
