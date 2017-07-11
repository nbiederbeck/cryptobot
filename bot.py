import re
from bs4 import BeautifulSoup
import requests
# from IPython import embed
import telepot
from time import sleep

token = '443609818:AAG65ovh6ywr-XyuXy53KHS5ZP1oPrTyf8o'
bot = telepot.Bot(token)
currencies = [
        'bitcoin',
        'ethereum',
        ]


def price(currency):
    '''Returns up-to-date price of currency.'''
    url = 'http://www.finanzen.net/devisen/{currency}-euro-kurs'.format(currency=currency)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find("div", {"class": "col-xs-5 col-sm-4 text-sm-right text-nowrap"})
    x = r'[0-9]*\.*[0-9]{1,3}\,[0-9]{1,4}'
    price = re.findall(pattern=x, string=str(div))[0]
    answer = '{curr} price is {price} EUR'.format(curr=currency, price=price)
    return answer


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if msg['text'] == '/bitcoin' or msg['text'] == '/ethereum':
        bot.sendMessage(chat_id=chat_id, text=price(msg['text'][1:]))
    # elif msg['text'] == '/start':
    else:
        bot.sendMessage(chat_id=chat_id, text='Use either /bitcoin or /ethereum')


# Keep the bot listening and running
print('listening ...')
bot.message_loop(handle)
while True:
    sleep(10)
    # for currency in currencies:
    #     bot.sendMessage(chat_id=chat_id, text=price(currency))
    # sleep(600)
