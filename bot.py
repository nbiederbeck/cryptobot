import re
import requests
import telepot
from time import sleep
from bs4 import BeautifulSoup
from yaml import load
from os import getpid
import locale
from IPython import embed

locale.setlocale(locale.LC_ALL, 'german')

with open('/home/pi/Git/RaspberryPiBot/temp/process_ids.txt', 'a') as f:
    f.write(str(getpid())+'\n')




token = config['token']
bot = telepot.Bot(token)

currencies = [  # supported cryptocurrencies
    'bitcoin',
    'ethereum',
    ]
commands = [  # implemented telegram commands
    '/start',
    '/bitcoin',
    '/bitcoin value',
    '/ethereum',
    '/ethereum value',
    ]

# fallback answer if messages are not understood
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

    #answer = '{curr} price is {price} EUR'.format(curr=currency, price=price)
    #return answer

    return locale.atof(price)

def get_value(currency, amount):
    price = get_price(currency)
    return amount*price

def answer(currency, amount=1):
    value = get_value(currency, amount)
    text_answer = '{curr} price is for {amount} {curr} is {value} EUR'.format(curr=currency, amount=amount, value=value)
    return text_answer

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
        command = msg['text']
    else:
        fallback(chat_id)
        return
    command = command[1:]
    command = command.split()
    if command[0] in currencies:
        if len(command) == 2:
            bot.sendMessage(chat_id=chat_id, text=answer(command[0],float(command[1])))
        elif len(command) ==1:
            bot.sendMessage(chat_id=chat_id, text=answer(command[0]))
        else:
            bot.sendMessage(chat_id=chat_id, text='You have typed too many arguments.')
            fallback(chat_id)
            return
    else:
        fallback(chat_id)
        return
    return


# Keep the bot listening and running
print('listening ...')
#embed()
bot.message_loop(handle)

while True:
    sleep(10)
    # to send price information every `n` minutes check documentation of `telepot`
    # because there is a preimplemented function
