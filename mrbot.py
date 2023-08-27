import telebot
from telebot import types
import pygsheets
import gspread
import time
import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import ast
from statistics import mean
import pendulum
#Вводные данные
bot = telebot.TeleBot("6394171812:AAFcJORzBVOjb9Fwn1_wsYpjvJyQGSTFeHk")
stop_x=False
worksheett = 'KazanExpress'
#options = Options()
#options.add_argument("--headless=new")
service = Service(executable_path='C:\chromedriver\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
list_of_users = []
def get_users():
    users = bot.get_updates()
    print(users)
    for user in users:
        if user.message.chat_id not in list_of_users:
            list_of_users.append(user.message.chat_id)
            print(list_of_users)
def send_message_to_users(message_text):
    for chat_id in list_of_users:
        bot.send_message(chat_id, message_text)
def KazanExpress(url):
    mnus = len(url) - 7
    mnus = url[mnus:]
    file_name = mnus + '.json'
    global driver
    driver.get(url)
    time.sleep(20)
    sum_amount = driver.find_element(By.CLASS_NAME, "available-amount").text
    if sum_amount == 'Нет в наличии':
        sum_amount = 0
    elif sum_amount == 'Остался последний!':
        sum_amount = 1
    else:
        try:
            sum_amount = sum_amount[9:]
            sum_amount = int(sum_amount)
        except ValueError:
            sum_amount = sum_amount[6:]
            sum_amount = int(sum_amount)
        except:
            sum_amount = 1
    counter=0
    scounter=0
    scounter=str(scounter)
    def comp(comparison, data):# Сравненение полученных данных
        text=[]
        counter=0
        InspectorMain=True
        while InspectorMain==True:
                counter=counter+1
                name = str(counter) + 'amount'
                color_name = str(counter) + 'color'
                try:
                    list_y = comparison[name]
                    list_x = data[name]
                    color_list = data[color_name]
                except:
                    return text
                i=0
                InspectorSecond=True
                while InspectorSecond==True:
                    try:
                        y = list_y[i]
                        x = list_x[i]
                        color = color_list[i]
                        all_amount=data['sum_amount']
                        z=int(x)-int(y)
                        z=z
                        i = i + 1
                        if int(x) > int(y) + 9:
                                text.append('У конкурента изменение количества!' + str(y) + '-->' + str(x)+
                                            '\n Изменение общего количества- '+str(all_amount-z) + '-->'+ str(all_amount)+
                                            '\n Цвет-'+str(color))
                    except IndexError:
                        try:
                            InspectorSecond=False
                        except UnboundLocalError:
                            print('Проблемы в сравнении!')
                            return text
                name = str(counter) + 'price'
                color_name = str(counter) + 'color'
                list_y = comparison[name]
                list_x = data[name]
                color_list = data [color_name]
                InspectorSecond=True
                i=0
                while InspectorSecond==True:
                    try:
                        y = list_y[i]
                        x = list_x[i]
                        color = color_list[i]
                        i = i + 1
                        if int(x) != int(y):
                                text.append('У конкурента изменение цены!' + str(y) + '-->' + str(x)+
                                            '\nЦвет-'+str(color))
                    except IndexError:
                        try:
                            #print('Конец индекса!'+str(i))
                            InspectorSecond=False
                        except UnboundLocalError:
                            text.append('Проблемы в сравнении!')
                            return text
    def scan(): #Проходится по нижнему уровню
        global driver
        levels=0
        counter = 0
        amount_list=[]
        price_list=[]
        color_list=[]
        while True:
            try:
                counter = int(counter) + 1
                counter = str(counter)
                amogus = driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div[2]/div[2]/div/div[' + counter + ']')
                levels=2
                amogus.click()
                time.sleep(0.4)
                #Поиск нужной информации
                amount = driver.find_element(By.CLASS_NAME, "available-amount").text
                price = driver.find_element(By.CLASS_NAME, "currency").text
                color = driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div[1]/div[1]').text
                color = color.replace('\n', '')
                color_finder = color.find(':') + 1
                color = color[color_finder:]
                if amount == 'Нет в наличии':
                    amount = 0
                elif amount == 'Остался последний!':
                    amount = 1
                else:
                    try:
                        amount = amount[9:]
                        amount = int(amount)
                    except ValueError:
                        amount = amount[6:]
                        amount = int(amount)
                    except:
                        amount = 1
                amount_list.append(amount)
                minmx = len(price) - 1
                price = int(price[:minmx])
                price_list.append(price)
                color_list.append(color)
            except selenium.common.exceptions.ElementClickInterceptedException:
                amogus = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div/div[1]/button')
                amogus.click()
                time.sleep(1)
                counter=int(counter)-1
                counter=str(counter)
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    amogus = driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div/div[2]/div/div[' + counter + ']')
                    levels = 1
                    amogus.click()
                    time.sleep(0.4)
                    amount = driver.find_element(By.CLASS_NAME, "available-amount").text
                    price = driver.find_element(By.CLASS_NAME, "currency").text
                    color = driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div[1]/div[1]').text
                    #color = color.replace(" ","")
                    color = color.replace('\n','')
                    color_finder = color.find(':')+1
                    color = color[color_finder:]
                    y=price.find(',')
                    if y!=-1:
                        y=y+1
                        price = price[:y]
                    price = price.replace(" ","")
                    if amount == 'Нет в наличии':
                        amount = 0
                    elif amount == 'Остался последний!':
                        amount = 1
                    else:
                        try:
                            amount = amount[9:]
                            amount = int(amount)
                        except ValueError:
                            amount = amount[6:]
                            amount = int(amount)
                        except:
                            amount = 1
                    amount_list.append(amount)
                    minmx = len(price) - 1
                    price = int(price[:minmx])
                    price_list.append(price)
                    color_list.append(color)
                except selenium.common.exceptions.ElementClickInterceptedException:
                    amogus = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/button')
                    amogus.click()
                    time.sleep(1)
                    counter = int(counter) - 1
                    counter = str(counter)
                except:
                    return amount_list,price_list,levels,color_list
            except:
                 return amount_list,price_list,levels,color_list
    amount_list, price_list,levels,color_list = scan()
    # print('Количество настроек-',levels)
    if levels == 0:
        amount_list=[]
        price_list=[]
        amount=driver.find_element(By.CLASS_NAME, "available-amount").text
        price=driver.find_element(By.CLASS_NAME, "currency").text
        y = price.find(',')
        if y != -1:
            y=y+1
            price = price[:y]
            # print(price)
        price = price.replace(" ", "")
        if amount == 'Нет в наличии':
            amount = 0
        elif amount == 'Остался последний!':
            amount = 1
        else:
            try:
                amount = amount[9:]
                amount = int(amount)
            except ValueError:
                amount = amount[6:]
                amount = int(amount)
            except:
                amount = 1
        amount_list.append(amount)
        minmx = len(price) - 1
        price_list.append(int(price[:minmx]))
        data = {"1amount": amount_list, "1price": price_list,'sum_amount':sum_amount}
        try:
            with open(file_name) as read_file:
                comparison = json.load(read_file)
                print(comparison)
                print(data)
                try:
                    comparison = ast.literal_eval(comparison)
                except ValueError:
                    False
                try:
                    text = comp(comparison, data)
                except KeyError:
                    with open(file_name, "w") as write_file:
                        json.dump(data, write_file)
                        print('KeyError')
        except FileNotFoundError:
            data = json.dumps(data)
            with open(file_name, "w") as write_file:
                json.dump(data, write_file)
                text='Новый товар в парсинге!'
                print(text)
                avg_price = price
                return text, avg_price, sum_amount
        with open(file_name, "w") as write_file:
            json.dump(data, write_file)
        avg_price = price
        return text,avg_price,sum_amount,color_list
    if levels == 1: #Для одинарных товаров
            data={"1amount":amount_list,"1price":price_list,'1sum_amount':sum_amount,'1color':color_list,'sum_amount':sum_amount}
            try:
                with open(file_name) as read_file:
                    comparison = json.load(read_file)
                    print(comparison)
                    print(data)
                    try:
                        comparison = ast.literal_eval(comparison)
                    except ValueError:
                        False
                    try:
                        text = comp(comparison, data)
                    except KeyError:
                        with open(file_name, "w") as write_file:
                            json.dump(data, write_file)
            except FileNotFoundError:
                data = json.dumps(data)
                with open(file_name, "w") as write_file:
                    json.dump(data, write_file)
                    text='Новый товар в парсинге!'
                    avg_price=mean(price_list)
                    return text,avg_price,sum_amount,color_list
            with open(file_name, "w") as write_file:
                json.dump(data, write_file)
            avg_price=mean(price_list)
            return text,avg_price,sum_amount,color_list
    elif levels == 2:
        data={}
        while True:
            scounter=int (scounter)
            scounter=scounter+1
            scounter =str(scounter)
            try:
                abobus=driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div[1]/div[2]/div/div['+scounter+']') #Ищет верхние кнопки
                abobus.click()
            except selenium.common.exceptions.ElementClickInterceptedException: #При выскакивании рекламного окна
                amogus = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div/div[1]/button')
                amogus.click()
                time.sleep(1)
                counter=int(counter)-1
                counter=str(counter)
                abobus=driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div[1]/div[2]/div/div['+scounter+']')
                abobus.click()
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    with open(file_name) as read_file:
                        comparison = json.load(read_file)
                        print(comparison)
                        print(data)
                        try:
                            comparison = ast.literal_eval(comparison)
                        except ValueError:
                            False
                        try:
                            text = comp(comparison, data)
                        except KeyError:
                            with open(file_name, "w") as write_file:
                                json.dump(data, write_file)
                                print('KeyError')
                except FileNotFoundError:
                    data = json.dumps(data)
                    with open(file_name, "w") as write_file:
                        json.dump(data, write_file)
                        text='Новый товар в парсинге!'
                        print('Запись нового файла!')
                with open(file_name, "w") as write_file:
                    json.dump(data, write_file)
                # try:
                return text,avg_price,sum_amount,color_list
                # except UnboundLocalError:
                #     text='Запись нового файла!'
            amount_list,price_list,levels,color_list=scan()
            name1=str(scounter)+"amount"
            name2=str(scounter)+"price"
            name3=str(scounter)+"color"
            if int(scounter)==1:
                avg_price=mean(price_list)
            else:
                price_list.append(avg_price)
                avg_price=mean(price_list)
                price_list.pop()
            data[name1]=amount_list
            data[name2]=price_list
            data[name3]=color_list
            data['sum_amount']=sum_amount
@bot.message_handler(commands=['Start','start','START'])
def send_welcome(message):
	print(stop_x)
	bot.reply_to(message, "Привет! Я Мистер Парсер! Я ещё всему учусь, так что снисходительнее пожалуйста.")
	time.sleep(1)
	bot.send_message(message.chat.id,"p.s. Если кнопки управления не появляются, введите команду КОМАНДЫ,а что бы подписаться на рассылку /Subscribe")
@bot.message_handler(commands=['help','Help','HELP'])
def send_command(message):
    bot.send_message(message.chat.id, "Доступные на данный момент команды-")
    bot.send_message(message.chat.id,"/Subscribe-Подписка на уведомления парсера")
    bot.send_message(message.chat.id, "/Start-Вывод первого сообщения")
    bot.send_message(message.chat.id, "/Mailing-Вывод данных из Google таблиц")
    bot.send_message(message.chat.id, "/Button-Вывод клавиатуры")
@bot.message_handler(commands=['Subscribe','subscribe','SUBSCRIBE'])
def Podpiska(message):
    bot.send_message(message.chat.id,"Спасибо за подписку на уведомления парсера!")
    with open('User_Id.txt','a+') as read_file:
        print(message.chat.id, file=read_file)

@bot.message_handler(commands=['DOOM'])
def DOOM_MESSAGE(message):
    bot.send_message(message.chat.id,"Таки происходит уведомление всех")
    for i in open('User_Id.txt','r').readlines():
        bot.send_message(i,'Тестирование рассылки, возможно вы первый и последний кто её видит')

@bot.message_handler(commands=['Mailing','mailing','MAILING'])
def mailing(message):
    GC = gspread.service_account(
        filename='C:\Program Files\pythonforgays-5b08b4475518.json')
    counter = 1
    bot.send_message(message.chat.id, 'Начинаю сбор данных!')
    while True:
        time.sleep(0.8)
        counter=counter+1
        worksheett = 'KazanExpress'
        SH = GC.open(worksheett)
        worksheet = SH.get_worksheet(0)
        worksheet_Inspector = worksheet.cell(counter, 1).value
        if worksheet_Inspector == None:
            return
        text = (
                "НАЗВАНИЕ ТОВАРА-" + str(worksheet.cell(counter, 2).value) +
                "\nПРОДАВЕЦ- " + str(worksheet.cell(counter, 3).value) +
                "\nСРЕДНЯЯ ЦЕНА- " + str(worksheet.cell(counter, 4).value) +
                "\nОБЩЕЕ КОЛИЧЕСТВО-" + str(worksheet.cell(counter, 5).value) +
                "\nВРЕМЯ ПОСЛЕДНЕГО ОБНОВЛЕНИЯ-" + str(worksheet.cell(counter, 6).value)
        )
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types='text')
def message_reply(message):
    def kazan():
        gc = pygsheets.authorize(
            service_account_file='C:\Program Files\pythonforgays-5b08b4475518.json')
        GC = gspread.service_account(
            filename='C:\Program Files\pythonforgays-5b08b4475518.json')
        counter = 2
        worksheett = 'KazanExpress'
        SH = GC.open(worksheett)
        worksheet = SH.get_worksheet(0)
        while True:
            global stop_x
            if stop_x == True:
                return (print("Прекращаю парсинг..."))
            else:
                values_list = worksheet.row_values(counter)
                url = values_list[0]
                text,avg_price,sum_amount,color_list = KazanExpress(url)
                if text != []:
                    if type(text)==str:
                        text = (
                                "Уведомление!" +
                                "\nНАЗВАНИЕ ТОВАРА-" + str(worksheet.cell(counter, 2).value) +
                                "\nПРОДАВЕЦ- " + str(worksheet.cell(counter, 3).value) +
                                "\nУВЕДОМЛЕНИЕ- " + text
                        )
                        bot.send_message(message.chat.id, text)
                    elif type(text)==list:
                        for i in range(len(text)):
                            Notification=text[i]
                            try:
                                color=color_list[i]
                            except:
                                color=color_list
                            for User in open('User_Id.txt', 'r').readlines():
                                Notification_text = (
                                        "Уведомление!" +
                                        "\nНАЗВАНИЕ ТОВАРА-" + str(worksheet.cell(counter, 2).value) +
                                        "\nПРОДАВЕЦ- " + str(worksheet.cell(counter, 3).value) +
                                        "\nУВЕДОМЛЕНИЕ- " + Notification
                                )
                                bot.send_message(User, Notification_text)
                all_times =pendulum.now(tz='Europe/Samara')
                update_time= str(all_times.format('HH:mm:ss'))
                worksheet.update_cell(counter,6,update_time)
                worksheet.update_cell(counter, 5, sum_amount)
                worksheet.update_cell(counter, 4, avg_price)
                print(update_time)
                counter=counter+1
                worksheet_Inspector=worksheet.cell(counter,1).value
                print(worksheet_Inspector)
                if worksheet_Inspector == None :
                     counter=2
                     print('Обнуление',counter)
                time.sleep(111)
    if message.text=="Остановить парсинг KazanExpress":
        bot.send_message(message.chat.id,"Прекращаю парсинг...")
        global stop_x
        stop_x = True
        print('ОСТАНОВКА ПАРСИНГА ИЗВНЕ')
        return stop_x
    elif message.text=="Парсинг KazanExpress":
        bot.send_message(message.chat.id,"Начинаю парсинг")
        stop_x = False
        kazan()
        return stop_x
    elif message.text=="Команды" or "команды" or "Кнопки" or "кнопки" or "КОМАНДЫ":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Парсинг KazanExpress")
        markup.add(item1)
        item2=types.KeyboardButton("Остановить парсинг KazanExpress")
        markup.add(item2)
        bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    elif message.text=="Сбор":
        get_users()
    elif message.text=="Отправка":
        send_message_to_users('Hello world!')
@bot.message_handler(commands=['button','Button','BUTTON'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Парсинг KazanExpress")
    markup.add(item1)
    item2=types.KeyboardButton("Остановить парсинг KazanExpress")
    markup.add(item2)
    item3 = types.KeyboardButton("Получение данных")
    markup.add(item3)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

print("Процесс включения успешен, начинаю работу...")

bot.infinity_polling()
