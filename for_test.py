# -*- coding: utf-8 -*-

import time
import eventlet
import requests
import logging
import telebot
import re
from test import get_string_of_points
from time import sleep

token = '1064607492:AAE0zKbB_Jbn2e7MqpcASS_JcJ7EMgkaYYI'
bot = telebot.TeleBot(token)

# Регулярное выражение, реагирующее на 2 введённых через пробел числа
login_pattern = re.compile(r'^student_[0-9]+ \w+$')

@bot.message_handler(commands=['start'])
def game(message):
    bot.send_message(message.chat.id, "Write your login and pass in the form of \n\n  "
                                      "student_67439 password \n\n  через пробел между ними")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, важно не повторяться
    try:
        matches = re.match(login_pattern, message.text)
        print(message.text)
        # Вылавливаем ошибку, если вдруг юзер ввёл чушь
        # или задумался после ввода первого числа
    except AttributeError as ex:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Неправильно введены данные!')
        return
    bot.send_message(message.chat.id, 'Загрузка...')
    login, password = matches.group().split()
    print(login + '\n' + password)
    try:
        points = get_string_of_points(str(login), str(password))
    except Exception:
        bot.send_message(message.chat.id, "Попробуйте снова...")
        bot.send_message(message.chat.id, "Write your login and pass in the form of \n\n  "
                                          "student_67439 password \n\n  через пробел между ними")
        pass
    bot.send_message(message.chat.id, points)


if __name__ == "__main__":
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
    bot.infinity_polling()
