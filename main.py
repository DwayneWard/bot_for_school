from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import logging

from db import BotDB
from exceptions import UserNotFound
from tools import is_email_correct

TOKEN = "5287302907:AAF8hOOm_lDGeKeVvefH87pVZoHUiFYMNNo"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

db = BotDB('test.db')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

EMAIL = range(1)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! добро пожаловать в бота-помощника'
                                                                    ' онлайн-школы __НАЗВАНИЕ__!')


def register(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Проверим, учитесь ли вы в нашей школе. Введите email, '
                                  'указанный при регистрации, пожалуйста')
    return EMAIL

def email(update: Update, context: CallbackContext):
    email = update.message.text
    if is_email_correct(email):
        try:
            db.user_exist(email)
            first_name, last_name = db.get_name_by_email(email)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Приветствую, {first_name} {last_name}. Продолжим учиться?')
        except UserNotFound:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Кажется, вы у нас не учитесь :('
                                          'Если вы уверены, что проходите обучение, проверьте правильность написания '
                                          'вашего email'
                                          f'Вы написали {email}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Проверьте, правильно ли вы ввели email")



# def echo(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
#
#
# def caps(update: Update, context: CallbackContext):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


start_handler = CommandHandler('start', start)
register_handler = CommandHandler('register', register)
email_handler = MessageHandler(Filters.text, email)
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(register_handler)
dispatcher.add_handler(email_handler)
# dispatcher.add_handler(echo_handler)
# dispatcher.add_handler(caps_handler)

updater.start_polling()
updater.idle()
