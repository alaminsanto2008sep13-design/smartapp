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

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    if message.web_app_data.data == "add_money":
        user_id = message.from_user.id
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (id, balance) VALUES (?, 0)", (user_id,))
        c.execute("UPDATE users SET balance = balance + 0.20 WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "💰 অভিনন্দন! আপনার ব্যালেন্সে ২০ পয়সা যোগ হয়েছে। নতুন ব্যালেন্স দেখতে /start দিন।")
print("Bot is running...")
bot.polling()
