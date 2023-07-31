import requests
import pendulum
import os
import random
import time
import pyperclip
from selenium import webdriver
#Константы
PUT='F:\LOL\RAS'
TYPEF='.pdf'
URL='http://stmit.ru/wp-content/uploads/'
#SHELL = win32com.client.Dispatch('WScript.Shell')
EXE_PATH = r'C:\Users\f4lln\Documents\Drivers\chromedriver.exe'
#Переменные
space=" "
s= "/"
ss= "\\"
dash='-'
i=0
text='Привет! Я Мистер Парсер! Я ещё всему учусь, так что снисходительнее пожалуйста.'
#Словарь
months={}
months={1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',
        11:'ноября',12:'декабря',}

#Определение даты
day=pendulum.now('Europe/Samara').format('DD')
year=pendulum.tomorrow('Europe/Samara').format('YYYY')
month=pendulum.tomorrow('Europe/Samara').format('MM')
data=year+s+month+s+day
month=int (month)
name_month=months [month]
month=str (month)

