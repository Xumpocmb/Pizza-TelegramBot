from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton('/загрузить')
button_delete = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete)
