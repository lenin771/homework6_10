import requests
from bs4 import BeautifulSoup
from datetime import date
import telebot
from cfg import TOKEN
from random import randint

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message, res=False):
	current_date = date.today() 
	bot.send_message(message.chat.id, f'курсы валют ЦБ РФ на {current_date}')
	bot.send_message(message.chat.id, 'Введите индекс валюты "USD" "EUR" "GBP" "CHF"')
	

@bot.message_handler(content_types=["text"])
def handle_text(message):
	url = 'http://www.finmarket.ru/currency/rates/'
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	USD_string = str(soup.find_all(class_='value')[0])
	EUR_string = str(soup.find_all(class_='value')[1])
	GBP_string = str(soup.find_all(class_='value')[2])
	CHF_string = str(soup.find_all(class_='value')[3])
	if message.text == 'USD':
		bot.send_message(message.chat.id, USD_string[USD_string.find('>')+1:USD_string.find('</div>'):].replace(',', '.'))
	elif message.text == 'EUR':
		bot.send_message(message.chat.id, EUR_string[EUR_string.find('>')+1:EUR_string.find('</div>'):].replace(',', '.'))
	elif message.text == 'GBP':
		bot.send_message(message.chat.id, 
        GBP_string[USD_string.find('>')+1:USD_string.find('</div>'):].replace(',', '.'))    
	elif message.text == 'CHF':
		bot.send_message(message.chat.id, 
        CHF_string[EUR_string.find('>')+1:EUR_string.find('</div>'):].replace(',', '.'))
	else:
		bot.send_message(message.chat.id, 'Некоректный ввод')
		
bot.infinity_polling()

