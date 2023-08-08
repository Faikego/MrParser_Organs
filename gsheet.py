import telebot
from telebot import types
import pygsheets
import gspread
import time
import requests
from bs4 import BeautifulSoup
import selenium
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import ast
from statistics import mean


gc = pygsheets.authorize(service_account_file='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
GC = gspread.service_account(filename='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
scounter = 4
counter = 2
worksheett = 'KazanExpress'
#options = Options()
#options.add_argument("--headless=new")
service = Service(executable_path='C:\chromedriver\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

def boba(url):
    sum_amount=0
    mnus = len(url) - 7
    mnus = url[mnus:]
    file_name = mnus + '.json'
    global driver
    driver.get(url)
    time.sleep(13)
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
                #print(name)
                try:
                    list_y = comparison[name]
                    list_x = data[name]
                except:
                    print('Конец сравнения!')
                    #print(text)
                    return text
                i=0
                InspectorSecond=True
                while InspectorSecond==True:
                    try:
                        y = list_y[i]
                        x = list_x[i]
                        i = i + 1
                        if int(x) > int(y) + 9:
                                text.append('У конкурента изменение количества!' + str(y) + '-->' + str(x))
                                print('У конкурента изменение количества!' + str(y) + '-->' + str(x))
                    except IndexError:
                        try:
                            InspectorSecond=False
                        except UnboundLocalError:
                            print('Проблемы в сравнении!')
                            return text
                name = str(counter) + 'price'
                #print(name)
                list_y = comparison[name]
                list_x = data[name]
                InspectorSecond=True
                i=0
                while InspectorSecond==True:
                    try:
                        y = list_y[i]
                        x = list_x[i]
                        i = i + 1
                        if int(x) != int(y):
                                text.append('У конкурента изменение цены!' + str(y) + '-->' + str(x))
                                print('У конкурента изменение цены!' + str(y) + '-->' + str(x))
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
        while True:
            try:
                counter = int(counter) + 1
                counter = str(counter)
                amogus = driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div[2]/div[2]/div/div[' + counter + ']')
                levels=2
                amogus.click()
                time.sleep(0.4)
                amount = driver.find_element(By.CLASS_NAME, "available-amount").text
                price = driver.find_element(By.CLASS_NAME, "currency").text
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
                except selenium.common.exceptions.ElementClickInterceptedException:
                    amogus = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/button')
                    amogus.click()
                    time.sleep(1)
                    counter = int(counter) - 1
                    counter = str(counter)
                except:
                    return amount_list,price_list,levels
            except:
                 return amount_list,price_list,levels
    amount_list, price_list,levels = scan()
    print('Количество настроек-',levels)
    if levels == 0:
        amount_list=[]
        price_list=[]
        amount=driver.find_element(By.CLASS_NAME, "available-amount").text
        price=driver.find_element(By.CLASS_NAME, "currency").text
        y = price.find(',')
        if y != -1:
            y=y+1
            price = price[:y]
            print(price)
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
        data = {"1amount": amount_list, "1price": price_list}
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
                text = 'Запись нового файла!'
                print(text)
                return text
        with open(file_name, "w") as write_file:
            json.dump(data, write_file)
        avg_price = price
        sum_amount = amount
        return text,avg_price,sum_amount
    if levels == 1: #Для одинарных товаров
            data={"1amount":amount_list,"1price":price_list}
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
                    text='Запись нового файла!'
                    avg_price=mean(price_list)
                    sum_amount=sum(price_list)
                    return text,avg_price,sum_amount
            with open(file_name, "w") as write_file:
                json.dump(data, write_file)
            avg_price=mean(price_list)
            sum_amount=sum(amount_list)
            return text,avg_price,sum_amount
    elif levels == 2:
        data={}
        while True:
            scounter=int (scounter)
            scounter=scounter+1
            scounter =str(scounter)
            try:
                abobus=driver.find_element(By.XPATH,'//*[@id="product-info"]/div[2]/div[2]/div[1]/div[2]/div/div['+scounter+']')
                abobus.click()
            except selenium.common.exceptions.ElementClickInterceptedException:
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
                        print('Запись нового файла!')
                with open(file_name, "w") as write_file:
                    json.dump(data, write_file)
                return text,avg_price,sum_amount
            amount_list,price_list,levels=scan()
            name1=str(scounter)+"amount"
            name2=str(scounter)+"price"
            name1=str(name1)
            name2=str(name2)
            if int(scounter)==1:
                avg_price=mean(price_list)
            else:
                price_list.append(avg_price)
                avg_price=mean(price_list)
                price_list.pop()
            sum_amount=sum(amount_list)+sum_amount
            data[name1]=amount_list
            data[name2]=price_list
    return text,avg_price,sum_amount

tex,avg_price,sum_amount=boba('https://kazanexpress.ru/product/portativnaya-kolonka-zqs-2188847?erid=2Vtzqv8XjBc')
print('------------------------------------------------------------------------------------Вывод----------------------------------------------------------------------------------------------------------')
print('TЕКСТ-',tex)
print('СРЕДНЯЯ ЦЕНА-',avg_price)
print('ОБЩЕЕ КОЛИЧЕСТВО ТОВАРА',sum_amount)

#0 уровней-https://kazanexpress.ru/product/tverdyj-dezodorant-muzhskoj-2050484
#1 уровень-https://kazanexpress.ru/product/dnevnik-shkolnyj-1-11-klass-tverdaya-oblozhka-1847879
#2 уровень-https://kazanexpress.ru/product/velosipedki-zhenskie-sportivnye-chernye-1847553
#Большая цена-https://kazanexpress.ru/product/portativnaya-kolonka-zqs-2188847?erid=2Vtzqv8XjBc



# def google ():
#     gc = pygsheets.authorize(service_account_file='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
#     GC = gspread.service_account(filename='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
#     scounter = 4
#     counter = 2
#     worksheett = 'KazanExpress'
#     SH = GC.open(worksheett)
#     worksheet = SH.get_worksheet(0)
#     sh = gc.open(worksheett)
#     while True:
#         values_list = worksheet.row_values(counter)
#         url=values_list[0]
#         def Parsing(url):
#             driver = webdriver.ChromiumEdge()
#             driver.get(url)
#             time.sleep(13)
#             amount = driver.find_element(By.CLASS_NAME, "available-amount").text
#             price = driver.find_element(By.CLASS_NAME, "currency").text
#             amount = amount[9:]
#             amount = int(amount)
#             print(amount)
#             return amount,price
#             driver.close()
#         value,price=Parsing(url)
#         worksheet.update_cell(counter,scounter,value)
#         worksheet.update_cell(counter,3,price)
#         scounter=scounter+1
#         if scounter == 6 :
#             scounter = 4
#         counter=counter+1
#         if counter > 6:
#             counter=2
#             print('Новый цикл')





