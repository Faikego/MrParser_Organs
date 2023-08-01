import telebot
from telebot import types
import pygsheets
import gspread
import time
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
bot = telebot.TeleBot("6394171812:AAFcJORzBVOjb9Fwn1_wsYpjvJyQGSTFeHk")
stop_x=False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	print(stop_x)
	bot.reply_to(message, "Привет! Я Мистер Парсер! Я ещё всему учусь, так что снисходительнее пожалуйста.")
	time.sleep(1)
	bot.send_message(message.chat.id,"p.s. Если кнопки управления не появляются, введите команду /button")

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Команды" or "команды" or "Кнопки" or "кнопки":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Парсинг KazanExpress")
        markup.add(item1)
        item2=types.KeyboardButton("Остановить парсинг KazanExpress")
        markup.add(item2)
        bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    def kazan():
        gc = pygsheets.authorize(
            service_account_file='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
        GC = gspread.service_account(
            filename='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
        counter = 2
        worksheett = 'KazanExpress'
        SH = GC.open(worksheett)
        worksheet = SH.get_worksheet(0)
        sh = gc.open(worksheett)
        while True:
            global stop_x
            if stop_x == True:
                return (print("Прекращаю парсинг..."))
            else:
                values_list = worksheet.row_values(counter)
                url = values_list[0]
                def Parsing(url):
                    driver = webdriver.ChromiumEdge()
                    driver.get(url)
                    time.sleep(13)
                    amount = driver.find_element(By.CLASS_NAME, "available-amount").text
                    price = driver.find_element(By.CLASS_NAME, "currency").text
                    if amount=='Нет в наличии':
                        amount=0
                    else:
                        amount = amount[9:]
                        amount = int(amount)
                    return amount, price
                    driver.close()
                value, price = Parsing(url)
                worksheet.update_cell(counter, 4, value)
                worksheet.update_cell(counter, 3, price)
                counter=counter+1
                try:
                    values_list = worksheet.row_values(counter)
                    url = values_list[0]
                except:
                    print('Начинаю сравнение...')
                    for i in range (counter):
                        x = worksheet.cell(counter, 4).value
                        y = worksheet.cell(counter, 5).value
                        try:
                            if x > y:
                                text = (
                                        "У конкурента пополнение товара!" +
                                        "\nНазвание товара-" + worksheet.cell(counter, 2).value +
                                        "\nИЗМЕНЕНИЕ" + y +"--->" + x
                                    )
                                bot.send_message(message.chat.id, text)
                            worksheet.update_cell(counter, 5, x)
                        except:
                            worksheet.update_cell(counter, 5, 0)
                        counter=counter-1
                    counter=2
                    print('Новый цикл...')
                time.sleep(900)
    if message.text=="Остановить парсинг KazanExpress":
        bot.send_message(message.chat.id,"Прекращаю парсинг...")
        global stop_x
        stop_x = True
        return stop_x
        print(stop_x)
    elif message.text=="Парсинг KazanExpress":
        bot.send_message(message.chat.id,"Начинаю парсинг")
        stop_x = False
        kazan()
        return stop_x
@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Парсинг KazanExpress")
    markup.add(item1)
    item2=types.KeyboardButton("Остановить парсинг KazanExpress")
    markup.add(item2)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

print("Процесс включения успешен, начинаю работу...")
bot.infinity_polling()