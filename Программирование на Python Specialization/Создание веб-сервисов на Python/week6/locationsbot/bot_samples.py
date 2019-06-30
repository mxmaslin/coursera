import os

from collections import defaultdict

import telebot

from telebot import types


token = os.environ.get('TOKEN')

bot = telebot.TeleBot(token)

###################################################################

# Продажа ноутбуков

START, TITLE, PRICE, CONFIRMATION = range(4)

USER_STATE = defaultdict(lambda: START)
PRODUCTS = defaultdict(lambda: {})


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


def get_product(user_id):
    return PRODUCTS[user_id]


def update_product(user_id, key, value):
    PRODUCTS[user_id][key] = value


@bot.message_handler(func=lambda message: get_state(message) == START)
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Напиши название')
    update_state(message, TITLE)


@bot.message_handler(func=lambda message: get_state(message) == TITLE)
def handle_title(message):
    update_product(message.chat.id, 'title', message.text)
    bot.send_message(chat_id=message.chat.id, text='Укажи цену')
    update_state(message, PRICE)


@bot.message_handler(func=lambda message: get_state(message) == PRICE)
def handle_price(message):
    update_product(message.chat.id, 'price', message.text)
    product = get_product(message.chat.id)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Опубликовать объявление? {product}'
    )
    update_state(message, CONFIRMATION)


@bot.message_handler(func=lambda message: get_state(message) == CONFIRMATION)
def handle_price(message):
    if 'да' in message.text.lower():
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Объявление опубликовано'
        )
    # if 'нет' in message.text.lower():
    #     bot.send_message(
    #         chat_id=message.chat.id,
    #         text=f'Объявление опубликовано'
    #     )
    update_state(message, START)


#################################################################

# Ближайший банк


def closest_bank(location):
    lat = location.latitude
    lon = location.longitude
    bank_address = 'Якуба Коласа, 3'
    bank_lat, bank_lon = 55.800389, 37.543710
    return bank_address, bank_lat, bank_lon


@bot.message_handler(content_types=['location'])
def handle_location(message):
    print(message.location)
    bank_address, bank_lat, bank_lon = closest_bank(message.location)
    bot.send_location(message.chat.id, bank_lat, bank_lon)
    image = open('bank.jpg', 'rb')
    bot.send_photo(message.chat.id, image, caption=f'Ближайший банк {bank_address}')


##################################################################

# Курс валют

currencies = ['евро', 'доллар']


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text=c, callback_data=c)
        for c in currencies
    ]
    keyboard.add(*buttons)
    return keyboard


def currency_in_message(message):
    for currency in currencies:
        if currency in message.text.lower():
            return True
    return False


def check_currency_value(text):
    currency_values = {'евро': 70, 'доллар': 60}
    for currency, value in currency_values.items():
        if currency in text.lower():
            return currency, value
    return None, None


@bot.callback_query_handler(func=lambda x: True)
def callback_handler(callback_query):
    # срабатывает только при нажатии на кнопку
    message = callback_query.message
    text = callback_query.data
    currency, value = check_currency_value(text)
    keyboard = create_keyboard()
    bot.send_message(
        message.chat.id,
        text=f'Курс {currency} равен {value}',
        reply_markup=keyboard
    )


@bot.message_handler()
def handle_currency(message):
    currency, value = check_currency_value(message.text)
    keyboard = create_keyboard()
    if currency:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Курс {currency} равен {value}',
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Узнай курс валют',
            reply_markup=keyboard
        )


###############################################################

# Печатает текст сообщения и отвечает Ура


@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Ура')


bot.polling()
