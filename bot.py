import re
import requests
import telepot
from time import sleep
from bs4 import BeautifulSoup
from yaml import load
from os import getpid
with open('/home/pi/Git/RaspberryPiBot/temp/process_ids.txt', 'a') as f:
    f.write(str(getpid())+'\n')
# from IPython import embed

with open('config.yaml') as f:
    config = load(f)

token = config['token']
bot = telepot.Bot(token)

currencies = [  # supported cryptocurrencies
    'bitcoin',
    'ethereum',
    ]
commands = [  # implemented telegram commands
    '/start',
    '/bitcoin',
    '/ethereum',
    ]

# fallback answer if messges are not understood
guide = 'Use either '
for command in commands:
    if command != commands[-1]:
        guide += command + ' or '
    else:
        guide += command + '.'


def get_price(currency):
    '''Returns up-to-date price of currency.'''

    url = 'http://www.finanzen.net/devisen/{currency}-euro-kurs'.format(
        currency=currency)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find(
        "div", {"class": "col-xs-5 col-sm-4 text-sm-right text-nowrap"})

    x = r'[0-9]*\.*[0-9]{1,3}\,[0-9]{1,4}'
    price = re.findall(pattern=x, string=str(div))[0]

    answer = '{curr} price is {price} EUR'.format(curr=currency, price=price)
    return answer


def fallback(chat_id):
    '''Send fallback message if something is not quite right.'''
    bot.sendMessage(chat_id=chat_id, text=guide)


def handle(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)

    if chat_id == 322086570:
        admin = True
    else:
        admin = False

    if content_type == 'text':
        message = msg['text']
    else:
        fallback(chat_id)
        return

    if message.startswith('/'):
        command = message[1:]
    else:
        fallback(chat_id)
        return

    if command in currencies:
        bot.sendMessage(chat_id=chat_id, text=get_price(command))
    else:
        fallback(chat_id)
        return

    return


# Keep the bot listening and running
print('listening ...')
bot.message_loop(handle)
# sleep(24 * 60 * 60 - 1)

while True:
    sleep(10)
    # for currency in currencies:
    #     bot.sendMessage(chat_id=chat_id, text=price(currency))
    # sleep(600)
