# -*- coding: utf-8 -*-

import telebot
import re
from test import get_string_of_points
from telebot import types

token = '1064607492:AAE0zKbB_Jbn2e7MqpcASS_JcJ7EMgkaYYI'
bot = telebot.TeleBot(token)

# Регулярное выражение, реагирующее на 2 введённых через пробел числа
login_pattern = re.compile(r'^student_[0-9]+ \w+$', re.MULTILINE)


@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text="Выбери чат", switch_inline_query="student_56169 ABSS2gp")
    keyboard.add(switch_button)
    bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)


# При отсутствии запроса ( = пустой запрос) выводим некоторую информацию
@bot.inline_handler(lambda query: len(query.query) is 0)
def empty_query(query):
    hint = "Подождите пока результаты загрузятся"
    try:
        r = types.InlineQueryResultArticle(
                id='1',
                title="Бот \"eKazNMU\"",
                description=hint,
                # Текст сообщения, которое будет выводиться при нажатии на подсказку
                input_message_content=types.InputTextMessageContent(
                message_text="points")
        )
        bot.answer_inline_query(query.id, [r], cache_time=86400)
    except Exception as e:
        print(e)

# Иконки, выводимые в качестве превью к результатам
plus_icon = "https://pp.vk.me/c627626/v627626512/2a627/7dlh4RRhd24.jpg"
# minus_icon = "https://pp.vk.me/c627626/v627626512/2a635/ILYe7N2n8Zo.jpg"
# divide_icon = "https://pp.vk.me/c627626/v627626512/2a620/oAvUk7Awps0.jpg"
# multiply_icon = "https://pp.vk.me/c627626/v627626512/2a62e/xqnPMigaP5c.jpg"
# error_icon = "https://pp.vk.me/c627626/v627626512/2a67a/ZvTeGq6Mf88.jpg"


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    try:
        matches = re.match(login_pattern, query.query)
    # Вылавливаем ошибку, если вдруг юзер ввёл чушь
    # или задумался после ввода первого числа
    except AttributeError as ex:
        return
    # В этом месте мы уже уверены, что всё хорошо,
    # поэтому достаем данные
    login, password = matches.group().split()
    try:
        points = get_string_of_points(str(login), str(password))

        full = types.InlineQueryResultArticle(
                id='1', title="Показать оценки",
                # Описание отображается в подсказке,
                # message_text - то, что будет отправлено в виде сообщения
                description="Результат: {!s}".format("wait"),
                input_message_content=types.InputTextMessageContent(
                message_text="{!s}".format(points[10])),
                # Указываем ссылку на превью и его размеры
                thumb_url=plus_icon, thumb_width=48, thumb_height=48
        )
        bot.answer_inline_query(query.id, [full], cache_time=300, is_personal="true")
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


if __name__ == '__main__':
    bot.infinity_polling()