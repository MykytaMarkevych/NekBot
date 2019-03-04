# -*- coding: utf-8 -*-
import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start','help'])
def handle_start_help(message):
    pass

@bot.message_handler(commands=['test'])
def game(message):
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[2], row[3])
    bot.send_message(message.chat.id, roow[1], reply_markup=markup)
    utils.set_user_game(message.chat.id, row[2])
    db_worker.close()

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = utils.get_answer_for_user(message.chat.id)
    if not answer:
        bot.send.message(message.chat.id, 'Щоб почати тестування, оберіть команду /test')
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id, "Так!", reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, "Ні, правильна відповідь ", answer, reply_markup=keyboard_hider)
        utils.finish_user_game(message.chat.id)            
        


if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)
