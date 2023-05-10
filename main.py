from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from art import tprint

from config import load_config
from handlers import client, admin, utility
from DB import sqlite_db


config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# ДЕЙСТВИЯ ПРИ ЗАПУСКЕ БОТА
async def on_startup(_):

    tprint('Pizza Bot')
    print('[+] Pizza Bot is online now..')
    print('[/] Attempt to connect to the DB..')
    sqlite_db.sql_start()


client.register_client_handlers(dp)
admin.register_admin_handlers(dp)
utility.register_utility_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
