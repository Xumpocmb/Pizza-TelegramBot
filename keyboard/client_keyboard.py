from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# для удаления клавиатуры используется ReplyKeyboardRemove
# from aiogram.types import ReplyKeyboardRemove

b1 = KeyboardButton('/Режим')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Сказать где я', request_location=True)


# для однократного использования клавиатуры используется параметр one_time_keyboard=True
# этот параметр не используется если в ходе выполнения программы используется ReplyKeyboardRemove
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b1, b2, b3).row(b4, b5)

# примеры добавления кнопок
# kb_client.add(b1).add(b2).add(b3)
# kb_client.add(b1).insert(b2).add(b3)
# kb_client.add(b1).row(b2, b3)
