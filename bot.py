# -*- coding: utf-8 -*-
from config import *
import telebot
import utils
from SQLighter import SQLighter
import random
import os
from flask import Flask, request
import datetime

bot = telebot.TeleBot(token)
server = Flask(__name__)
now = datetime.datetime.now

class randomrow:
    def __init__(self,rownum):
        self.rownum = rownum
    def rand(self):
        return random.randint(1,201) #жуткий костыль

@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://enigmatic-river-40567.herokuapp.com/' + token)
    return "?", 200
    
@bot.message_handler(commands=['start'])
def start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Почати підготовку')
    bot.send_message(message.chat.id, 'Щоб побачити наступне питання, оберіть команду /test')
def remainder():
    if now.hour == 18 and now.minute == 0 :
        bot.send_message(message.chat.id, 'Щоб побачити наступне питання, оберіть команду /test')

@bot.message_handler(commands=['test'])
def game(message):
    db_worker = SQLighter(database_name)
    c = randomrow(utils.get_rows_count())
    row = db_worker.select_single(c.rand)
    markup = utils.generate_markup(row[2], row[3])
    bot.send_message(message.chat.id, row[1], reply_markup=markup)
    utils.set_user_game(message.chat.id, row[2])
    db_worker.close()

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = utils.get_answer_for_user(message.chat.id)
    if not answer:
        bot.send_message(message.chat.id, 'Щоб почати наступне питання, оберіть команду /test')
    else:
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id, "Так! Далі - /test", reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, "Ні, правильна відповідь: %s. Далі - /test" %answer, reply_markup=keyboard_hider)
        utils.finish_user_game(message.chat.id)
            
if __name__ == '__main__':
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
    utils.count_rows()
    random.seed()
       
    
    
