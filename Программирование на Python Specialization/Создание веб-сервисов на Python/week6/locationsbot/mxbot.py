import os

from collections import defaultdict

import telebot

import redis


token = os.environ.get('TOKEN')

bot = telebot.TeleBot(token)

r = redis.Redis(host='localhost', port=6379, db=0)


START, ADD_NAME, ADD_LOCATION, CONFIRMATION = range(4)

USER_STATE = defaultdict(lambda: START)

LOCATIONS = defaultdict(lambda: {})


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


def get_location(user_id):
    return LOCATIONS[user_id]


def update_location(user_id, key, value):
    LOCATIONS[user_id][key] = value


@bot.message_handler(
    func=lambda message: get_state(message) == START, commands=['add']
)
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Напиши название')
    update_state(message, ADD_NAME)


@bot.message_handler(
    func=lambda message: get_state(message) == ADD_NAME)
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Отправь локацию')
    update_state(message, ADD_LOCATION)


@bot.message_handler(
    func=lambda message: get_state(message) == ADD_LOCATION,
    content_types=['location']
)
def handle_title(message):
    bot.send_message(chat_id=message.chat.id, text='Добавить?')
    update_state(message, CONFIRMATION)


@bot.message_handler(func=lambda message: get_state(message) == CONFIRMATION)
def handle_price(message):
    if 'да' in message.text.lower():
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Локация добавлена'
        )
        update_location(message.chat.id, 'title', message.location)
        update_state(message, START)
    if 'нет' in message.text.lower():
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Локация не добавлена'
        )
        update_state(message, START)


bot.polling()
