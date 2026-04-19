import telebot
import os
import sqlite3
from telebot import types

# টোকেন সেটআপ
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

MY_APP_URL = "https://alaminsanto2008sep13-design.github.io/smartapp/"

# ডাটাবেস তৈরি (টাকা সেভ রাখার জন্য)
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, balance REAL DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

# ব্যালেন্স চেক করার ফাংশন
def get_balance(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else 0.0

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    balance = get_balance(user_id) # ডাটাবেস থেকে ব্যালেন্স আনবে
    
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(MY_APP_URL)
    button = types.InlineKeyboardButton("🚀 ওপেন স্মার্ট আর্ন প্রো", web_app=web_app)
    markup.add(button)

    welcome_text = (
        f"👋 স্বাগতম আমাদের স্মার্ট আর্ন অ্যাপে!\n\n"
        f"💰 আপনার বর্তমান ব্যালেন্স: ৳ {balance:.2f}\n"
        f"🤑 এখন থেকে আপনি ভিডিও দেখে আয় করতে পারবেন।\n"
        f"✅ আপনার ইনকাম শুরু করতে নিচের বাটনে ক্লিক করুন।")
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

print("Bot is running...")
bot.polling()
