from ast import main
from os import name
from turtle import update
import telebot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '7181172204:AAHz5jlU7cFMva22JDhiV14Z5K2fN53KjR0'

users = [] # لیستی برای ذخیره کاربران آنلاین

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Anonymous Chat Bot!\nType /connect to find a chat partner.")
users.append(update.__annotations__sitart .message.chat_id)

def connect(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if len(users) > 1:
         users.remove(user_id)
         partner_id = users.pop(0)
         context.bot.send_message(partner_id, "Connected! Start chatting.")
         context.bot.send_message(user_id, "Connected! Start chatting.")
         context.user_data['partner'] = partner_id
         context.dispatcher.user_data[partner_id]['partner'] = user_id
    else:
            update.message.reply_text("Waiting for a partner...")

def message_handler(update: Update, context: CallbackContext) -> None:
    partner_id = context.user_data.get('partner')
    if partner_id:
        context.bot.send_message(partner_id, update.message.text)
    else:update.message.reply_text("Type /connect to find a partner.")
            
def disconnect(update: Update, context: CallbackContext) -> None:
    partner_id = context.user_data.pop('partner', None)
    if partner_id:
        context.bot.send_message(partner_id, "Your partner has disconnected.")
        context.dispatcher.user_data[partner_id].pop('partner', None)
        update.message.reply_text("You are disconnected.") 
def main() -> None: 
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("connect", connect))
    dispatcher.add_handler(CommandHandler("disconnect", disconnect))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
    updater.start_polling()
    updater.idle()


if  name == '__main__':
    main()