import re
import requests
import telepot
from time import sleep
from bs4 import BeautifulSoup
import yaml
from os import getpid
import locale
from IPython import embed
import sys

locale.setlocale(
    category=locale.LC_ALL,
    locale='de_DE.UTF-8',
    )

try:
    with open('/home/pi/Git/RaspberryPiBot/temp/process_ids.txt', 'a') as f:
        f.write(str(getpid())+'\n')
except FileNotFoundError as e:
    # print(e)
    print('File `process_ids.txt` not found. '
            'Should not be a concern, because testing is not done on Raspberry Pi.')

try:
    with open('/home/pi/Git/cryptobot/config.yaml') as f:
        config = yaml.load(f)
except FileNotFoundError as e:
    # print(e)
    print('Config file in cryptobot directory not found, trying current directory.')
    try:
        with open('config.yaml') as f:
            config = yaml.load(f)
    except FileNotFoundError as e:
        # print(e)
        sys.exit('No config file found. Aborting ...')

token = config['token']
bot = telepot.Bot(token)

currencies = [  # supported cryptocurrencies
    'bitcoin',
    'ethereum',
    ]
commands = [  # implemented telegram commands
    '/start',
    '/bitcoin',
    '/bitcoin <value>',
    '/ethereum',
    '/ethereum <value>',
    '/mycoins',
    '/mycoins add <btc-amount> <eth-amount>',
    ]

# fallback answer if messages are not understood
guide = 'Usage:\n'
for command in commands:
    if command != commands[-1]:
        guide += "- {}\n".format(command)
    else:
        guide += '- {}'.format(command)


def get_price(currency):
    '''Returns up-to-date price of currency.'''

    url = 'http://www.finanzen.net/devisen/{currency}-euro-kurs'.format(
        currency=currency)
    try:
        response = requests.get(url)
    except Exception as e:
        return 0  # there HAS TO BE a better way, but for now this needs to work

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
    text_answer = 'Price for {amount} {curr} is {value} EUR'.format(curr=currency, amount=amount, value=value)
    return text_answer


class Wallet():
    """A coin wallet. Stored are only the amounts per chat_id."""
    def __init__(self, wallet_location):
        self = self
        with open(wallet_location) as f:
            self.wallet = yaml.load(f)
    def get_value(self, chat_id):
        # wallet = yaml.load('wallet.yaml')
        try:
            current_wallet = self.wallet[chat_id]
        except:
            return 0
        value = get_value('bitcoin', current_wallet['bitcoin'])
        value += get_value('ethereum', current_wallet['ethereum'])
        return value
    def set_value(self, chat_id, do, btc_amount, eth_amount):
        # wallet = yaml.load('wallet.yaml')
        try:
            current_wallet = self.wallet[chat_id]
        except:
            current_wallet = dict()
        if do == 'set':
            current_wallet['bitcoin'] = btc_amount
            current_wallet['ethereum'] = eth_amount
            self.wallet[chat_id] = current_wallet
            with open('wallet.yaml', 'w') as f:
                yaml.dump(self.wallet, stream=f)
        else:
            current_wallet['bitcoin'] += btc_amount
            current_wallet['ethereum'] += eth_amount
            self.wallet[chat_id] = current_wallet
            with open('wallet.yaml', 'w') as f:
                yaml.dump(self.wallet, stream=f)
        return True

wallet = Wallet(wallet_location='wallet.yaml')



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
            command[1] = command[1].replace(',', '.')
            bot.sendMessage(chat_id=chat_id, text=answer(command[0],float(command[1])))
        elif len(command) ==1:
            bot.sendMessage(chat_id=chat_id, text=answer(command[0]))
        else:
            bot.sendMessage(chat_id=chat_id, text='You have typed too many arguments.')
            fallback(chat_id)
            return
    elif command[0] == 'mycoins':
        if len(command) == 1:
            euros = wallet.get_value(chat_id)
            bot.sendMessage(chat_id=chat_id, text='Your coins are worth {euros} EUR.'.format(euros=euros))
        else:
            do = command[1]  # should be one of add/set
            btc_amount = command[2]
            eth_amount = command[3]
            update = wallet.set_value(chat_id, do, float(btc_amount), float(eth_amount))
            if update:
                bot.sendMessage(chat_id=chat_id, text='Your coins are up to date!')
    else:
        fallback(chat_id)
        return
    return


# Keep the bot listening and running
print('listening ...')
bot.message_loop(handle)

while True:
    sleep(10)
    # to send price information every `n` minutes check documentation of `telepot`
    # because there is a preimplemented function
