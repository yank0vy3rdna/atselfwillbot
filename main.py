# -*- coding: utf-8 -*-
import telebot
import os
from telebot import apihelper
import datetime
import sys
import time
bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
user_dict = {}
texTemplate = open('atselfwill.tex', encoding="utf-8").read()
import traceback

class User:
    def __init__(self, name):
        self.name = name
        self.group = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
ПСЖ бот by yank0vy3rdna
Привет,
сейчас я помогу тебе числануться
Ректору Университета ИТМО от студента(напиши ФИО в родительном падеже):
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        if '\\' in name:
            raise Exception('dich')
        user = User(name)
        user_dict[chat_id] = user
        if len(name.split(' ')) != 3:
            raise ValueError('not 3 words')
        msg = bot.reply_to(message, 'Обучающимся в группе(напиши свою группу)')
        bot.register_next_step_handler(msg, process_age_step)
    except ValueError:
        bot.reply_to(message, 'ФИО это 3 слова')
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        group = message.text
        if '\\' in group:
            raise Exception('dich')
        user = user_dict[chat_id]
        user.group = group
        if group[0] in ['M','m','М','м']:
            bot.send_message(chat_id, 'ИТИП СОСАТБ')
        fio = user.name.split(' ')
        f = fio[0]
        i = fio[1]
        o = fio[2]
        fio = f + ' ' + i + ' ' + o
        fio = fio.title()
        bot.send_message(chat_id, 'Заполняем бланк')
        try:
            current_dir = os.path.abspath(os.path.dirname(__file__))
            tex = texTemplate.replace('@GROUP@', user.group).replace('@FIO@', fio)
            os.system('rm ПСЖ.*')
            with open('ПСЖ.tex','w',encoding='utf-8') as f:
                f.write(tex)
            os.system('python3 texliveonfly.py ПСЖ.tex')
            time.sleep(2)
            bot.send_message(chat_id, 'Поздравляю, твой бланк ПСЖ заполнен')
            doc = open('ПСЖ.pdf', 'rb')
            bot.send_document(chat_id, doc)
            print(datetime.datetime.now(),fio,user.group, message.from_user.id, message.from_user.username) 
        except Exception as e:
            bot.send_message(chat_id, "ooops")
            traceback.print_exc(file=sys.stderr)
    except Exception as e:
        bot.reply_to(message, 'oops')
        traceback.print_exc(file=sys.stderr)

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()
print('Bot started successfully')
bot.polling()
