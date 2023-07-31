import pygsheets
import gspread
import time
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


def google ():
    gc = pygsheets.authorize(service_account_file='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
    GC = gspread.service_account(filename='C:\\Users\\f4lnn\Documents\MrParser\MrParser_Organs\pythonforgays-5b08b4475518.json')
    scounter = 4
    counter = 2
    worksheett = 'KazanExpress'
    SH = GC.open(worksheett)
    worksheet = SH.get_worksheet(0)
    sh = gc.open(worksheett)
    while True:
        values_list = worksheet.row_values(counter)
        url=values_list[0]
        def Parsing(url):
            driver = webdriver.ChromiumEdge()
            driver.get(url)
            time.sleep(13)
            amount = driver.find_element(By.CLASS_NAME, "available-amount").text
            price = driver.find_element(By.CLASS_NAME, "currency").text
            amount = amount[9:]
            amount = int(amount)
            print(amount)
            return amount,price
            driver.close()
        value,price=Parsing(url)
        worksheet.update_cell(counter,scounter,value)
        worksheet.update_cell(counter,3,price)
        scounter=scounter+1
        if scounter == 6 :
            scounter = 4
        counter=counter+1
        if counter > 6:
            counter=2
            print('Новый цикл')

#апдейт содержимого ячейки- wk1.update_value(#,#)

google()
print ('Работа закончена')
