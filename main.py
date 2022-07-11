import os
import telebot
import logging
import psycopg2
from config import *
from telebot import  types
from flask import Flask, request


# db_connection = psycopg2.connect(DB_URI, sslmode="require")
# db_object = db_connection.cursor()


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    yes = types.KeyboardButton('💳 Да.')
    no = types.KeyboardButton('📝 Нет. Создать виртуальную карту')

    markup.add(yes, no)

    bot.send_message(message.chat.id, '💚 Здравствуйте, <b>{0.first_name}!</b>'
                                      ' Вас приветствует чат-бот сети АЗС «Белоруснефть»! Вы являетесь пользователем '
                                      'нашей виртуальной карты ?'.format(message.from_user), parse_mode='html',
                                      reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message: type.Message):
    if message.text == '💳 Да.':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        adv_game = types.KeyboardButton('🎲 Рекламные игры')
        bonus_program = types.KeyboardButton('💯 Бонусная программа')
        social_network = types.KeyboardButton('📸 Инстраграм')
        profile = types.KeyboardButton('❌ Профиль на доработке')
        balance = types.KeyboardButton('❌ Баланс на доработке')
        back = types.KeyboardButton('🔙 Назад')
        markup.add(adv_game, bonus_program, social_network, profile, balance, back)

        bot.send_message(message.chat.id, '💳 Да.', reply_markup=markup)


    elif message.text == '🎲 Рекламные игры':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Перейти на сайт 💚', url='https://bonus.belorusneft.by/registration')

        markup.add(btn)
        bot.send_message(message.chat.id, '💚 Заполните анкету в личном кабинете для участия '
                                          'в рекламных играх с розыгрышами крупных денежных '
                                          'сумм, подарочных сертификатов и суперпризов от партнера!',
                                          reply_markup=markup)

    elif message.text == '💯 Бонусная программа':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Перейти на сайт 💚', url='https://bit.ly/3xmsebQ')

        markup.add(btn)
        bot.send_message(message.chat.id, '💚 ИЗМЕНЕНИЯ В 2022 году.\n'
                                          '- получайте бонусы: за топливо (1 литр = 1 бонус), '
                                          'за товары (до 10 % от их стоимости);\n'
                                          '- обменивайте бонусы: на нетопливные '
                                          'товары до 50% от их стоимости (1 бонус = 1 копейка);\n'
                                          '- получайте повышенные (х2) бонусы в День Рождения (±3 дня);\n'
                                          '- срок действия бонусов с момента получения – 1 год.', reply_markup=markup)

    elif message.text == '📸 Инстраграм':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Перейти на сайт 💚', url='https://www.instagram.com/belarusn.by/')

        markup.add(btn)
        bot.send_message(message.chat.id, '💚 <b>{0.first_name}</b>, присоединяйся! Нас уже более 10.000.\n'
                                          '🛣 Туристический проект #BelarusN\n'
                                          'Мы знаем, куда поехать и что посмотреть!\n'
                                          'Заправляйся #цікава ☕'.format(message.from_user), parse_mode='html',
                                          reply_markup=markup)

    elif message.text == '🔙 Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        yes = types.KeyboardButton('💳 Да.')
        no = types.KeyboardButton('📝 Нет. Создать виртуальную карту')

        markup.add(yes, no)
        bot.send_message(message.chat.id, '🔙 Назад', reply_markup=markup)

    if message.text == '📝 Нет. Создать виртуальную карту':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        virtual_card = types.KeyboardButton('💳 Посмотреть номер карты')
        markup.add(virtual_card)




@server.route(f"/{TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

bot.polling(none_stop=True)
