from aiogram import types
import pymorphy3
import json
import string


# ФИЛЬТР МАТА
def normal_mat(word: str):
    word = word.lower().translate(str.maketrans('', '', string.punctuation))
    morph = pymorphy3.MorphAnalyzer()
    parsed_token = morph.parse(word)
    normal_form = parsed_token[0].normal_form
    return normal_form


# @dp.message_handler()
async def delete_ban_words(message: types.Message):
    if {normal_mat(i) for i in message.text.split(' ')}\
            .intersection(set(json.load(open('ban-words/new-banwords.json')))):
        await message.reply('Будьте вежливы!')
        await message.delete()
    # else:
    #     await message.reply(message.text)


# ПОДОБНЫМ ОБРАЗОМ РАЗБИТЬ РАЗБОР ТЕКСТА НА КЛЮЧЕВЫЕ СЛОВА В ОТДЕЛЬНОМ МОДУЛЕ!!!
# @dp.message_handler(lambda message: 'пицца' in message.text)
async def take_pizza(message: types.Message):
    # пишем в общий чат
    await message.reply('Вам были высланы инструкции в личные сообщения. Проверьте, пожалуйста!')
    # пишем в личку
    await message.answer('Простите, реализация будет позднее..')


# улавливает любые сообщения которые были отправлены боту
# @dp.message_handler()
# async def echo_send(message: types.Message):
#     # await message.answer("Hi!\nI'm EchoBot!\nPowered by aiogram.")
#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram. Developed by Xumpocmb")
#     #     отправка в личку (но бот первым в личку писать не может
#     # await bot.send_message(message.from_user.id, message.text)

def register_utility_handlers(dp):
    dp.register_message_handler(take_pizza, lambda message: 'заказать пиццу' in message.text)
    dp.register_message_handler(delete_ban_words)
