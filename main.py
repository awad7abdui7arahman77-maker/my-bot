import os
from flask import Flask
from threading import Thread
import telebot

# ضع توكن بوت تيليجرام الخاص بك هنا بين العلامتين
TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا أواّد، البوت يعمل بنجاح 24/7!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# إعداد سيرفر Flask البسيط للحفاظ على استمرار تشغيل السيرفر
app = Flask('')

@app.route('/')
def home():
    return "I am alive and running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
