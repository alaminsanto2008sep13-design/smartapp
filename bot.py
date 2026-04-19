import telebot
import os  # এই লাইনটা যোগ কর
from telebot import types

# কোটেশন মার্ক ছাড়া এভাবে লিখবি
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

MY_APP_URL = "https://alaminsanto2008sep13-design.github.io/smartapp/"

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(MY_APP_URL)
    button = types.InlineKeyboardButton(text="🚀 ওপেন স্মার্ট আর্ন প্রো", web_app=web_app)
    markup.add(button)
    
    welcome_text = (
        "👋 স্বাগতম আমাদের স্মার্ট আর্ন অ্যাপে!\n\n"
        "💰 এখন থেকে আপনি ভিডিও দেখে আয় করতে পারবেন।\n"
        "✅ আপনার ইনকাম শুরু করতে নিচের বাটনে ক্লিক করুন।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

print("Bot is running...")
bot.polling()
