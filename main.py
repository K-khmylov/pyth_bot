import telebot
import json
import random as r
from telebot import types

bot = telebot.TeleBot('5262563135:AAHBUFbhiZiVyUiEToPnkG_PFhA1J8DZNu4')
counter = 0
jokes_data = []

@bot.message_handler(commands=['start'])
def startJokes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Уеби мне анекдот")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, f"Привет {message.from_user.username}! Выбери тип анекдота", reply_markup=markup)

def nahrada(data, path, i):
    data[i]['counter'] = 1
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    if message.text.lower() == "уеби мне анекдот":
        global counter
        if counter != len(jokes_data):
            while True:
                number = r.randint(0, len(jokes_data) - 1)
                if jokes_data[number]['counter'] != 1:
                    nahrada(jokes_data, "Jokes.json", number)
                    counter += 1
                    bot.send_message(message.from_user.id, jokes_data[number]['joke'])
                    break
        else:
            bot.send_message(message.from_user.id, 'Мы работаем над новыми шутками )')

with open("Jokes.json", encoding="utf8") as file:
    jokes_data = json.load(file)

bot.polling(none_stop=True, interval=0)