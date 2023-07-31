import telebot
from gsheet import google
bot = telebot.TeleBot("6394171812:AAFcJORzBVOjb9Fwn1_wsYpjvJyQGSTFeHk")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Я Мистер Парсер! Я ещё всему учусь, так что снисходительнее пожалуйста.")

@bot.message_handler(commands=['Пеленг','Наблюдение','Разведка','Scan'])
def start_scan(message):
	google()
	bot.send_message(message,' Начинаю наблюдение...')

bot.infinity_polling()