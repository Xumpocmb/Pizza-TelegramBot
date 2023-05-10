import sqlite3 as sq
from aiogram import types

def sql_start():
    global base, cur
    base = sq.connect('pizza.db')
    cur = base.cursor()
    if base:
        print('[+] Connection is OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_show_menu(message: types.Message):
    for i in cur.execute('SELECT * FROM menu').fetchall():
        await message.answer_photo(i[0], f'{i[1]}\nОписание: {i[2]}\nЦена: {i[3]}')


async def sql_show_all_data():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
