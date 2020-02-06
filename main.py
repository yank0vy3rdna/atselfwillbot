# -*- coding: utf-8 -*-
import telebot
import os
from latex.build import build_pdf
from telebot import apihelper
import settings
import logging
import datetime
import sys
import time
apihelper.proxy = {'https': settings.credentials['proxy']}
bot = telebot.TeleBot(settings.credentials['api-key'])
user_dict = {}
texTemplate = open('/root/atselfwillbot/atselfwill.tex', encoding="utf-8").read()
import traceback

class User:
    def __init__(self, name):
        self.name = name
        self.group = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
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
        user = User(name)
        user_dict[chat_id] = user
        if len(name.split(' ')) != 3:
            raise ValueError('not 3 words')
        msg = bot.reply_to(message, 'Обучающимся в группе(напиши свою группу)')
        bot.register_next_step_handler(msg, process_age_step)
    except ValueError:
        bot.reply_to(message, 'ФИО ЭТО 3 СЛОВА ГЕНИЙ')
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        group = message.text
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
            os.system('rm /root/atselfwillbot/temp.*')
            with open('/root/atselfwillbot/temp.tex','w',encoding='utf-8') as f:
                f.write(tex)
            os.system('cd /root/atselfwillbot/; ./getpdf.sh')
            time.sleep(2)
            bot.send_message(chat_id, 'Поздравляю, твой бланк ПСЖ заполнен')
            doc = open('/root/atselfwillbot/temp.pdf', 'rb')
            bot.send_document(chat_id, doc)
            print(datetime.datetime.now(),fio,user.group, file=open('/var/log/atselfwill.out.log','a'))
        except Exception as e:
            bot.send_message(chat_id,str(e))
            traceback.print_exc(file=sys.stderr)
    except Exception as e:
        bot.reply_to(message, sys.exc_info()[0])
        traceback.print_exc(file=sys.stderr)

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()
print('Bot started successfully')
bot.polling()
