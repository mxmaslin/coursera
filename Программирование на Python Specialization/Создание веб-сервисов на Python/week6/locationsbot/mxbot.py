import os

from collections import defaultdict

import telebot

import redis


token = os.environ.get('TOKEN')

bot = telebot.TeleBot(token)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


START, ADD_NAME, ADD_LOCATION, CONFIRMATION = range(4)

USER_STATE = defaultdict(lambda: START)


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


def write_title_to_redis(message):
    user_id = message.chat.id
    location_title = message.text
    r.lpush(user_id, location_title)


def write_coords_to_redis(user_id, location):
    lat, lon = location.latitude, location.longitude
    title = r.lpop(user_id)
    full_location_data = f'{title}&#124;{lat}&#124;{lon}'
    r.lpush(user_id, full_location_data)


def delete_location(user_id):
    r.lpop(user_id)


@bot.message_handler(
    func=lambda message: get_state(message) == START, commands=['add']
)
def handle_title(message):
    bot.send_message(chat_id=message.chat.id, text='Напиши название')
    update_state(message, ADD_NAME)


@bot.message_handler(
    func=lambda message: get_state(message) == ADD_NAME)
def handle_location(message):
    if message.text in ('/add', '/list', '/reset'):
        bot.send_message(chat_id=message.chat.id, text='Добавление прервано')
        update_state(message, START)
    else:
        write_title_to_redis(message)
        bot.send_message(chat_id=message.chat.id, text='Отправь локацию')
        update_state(message, ADD_LOCATION)


@bot.message_handler(
    func=lambda message: get_state(message) == ADD_LOCATION,
    content_types=['location']
)
def handle_confirmation(message):
    bot.send_message(chat_id=message.chat.id, text='Добавить?')
    update_state(message, CONFIRMATION)
    write_coords_to_redis(message.chat.id, message.location)


@bot.message_handler(func=lambda message: get_state(message) == CONFIRMATION)
def handle_finish(message):
    if message.text in ('/add', '/list', '/reset'):
        update_state(message, START)
        delete_location(message.chat.id)
        bot.send_message(chat_id=message.chat.id, text='Добавление прервано')
    else:
        if 'да' in message.text.lower():
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Локация добавлена'
            )
            update_state(message, START)
        if 'нет' in message.text.lower():
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Локация не добавлена'
            )
            update_state(message, START)
            delete_location(message.chat.id)


@bot.message_handler(
    func=lambda x: True, commands=['list']
)
def handle_list(message):
    if get_state(message) != START:
        update_state(message, START)
        r.lpop(message.chat.id)
    else:
        bot.send_message(chat_id=message.chat.id, text='Последние локации:')
        last_locations = r.lrange(message.chat.id, 0, 10)
        for location in last_locations:
            if '&#124;' in location:
                title, lat, lon = location.split('&#124;')
                bot.send_message(chat_id=message.chat.id, text=title)
                bot.send_location(message.chat.id, lat, lon)
            else:
                bot.send_message(chat_id=message.chat.id, text=location)


@bot.message_handler(func=lambda x: True, commands=['reset'])
def handle_confirmation(message):
    r.flushdb()
    bot.send_message(chat_id=message.chat.id, text='Все локации удалены')


bot.polling()
