# cryptobot
A telegram bot written in python which gives you different information about some cryptocurrencies.
This bot is named [Crypt0Currency\_Bot][bot].
It currently runs on a Raspberry Pi.

## Usage
*Disclaimer:* You must have german locales (de_DE.UTF-8) installed!
1. Clone this repository
2. Run `make venv` to make a virtual environment using pythons built-in module
   `venv` (make sure to use Python 3)
3. Run `make install` once to install all packages, the same command updates
   all packages.
4. Run `make run` to activate the environment and run the bot.
    - The bot needs a file `config.yaml`, jsut copy `sample_config.yaml` and
      insert your own parameters

## _TODO_
- [x] write usage instructions
- [x] run on raspberry pi
- [x] send prices on message
- [x] have an  answer for every message
- [ ] send message every n minutes
- [ ] send relative changes
- [ ] plot and save some information
- [ ] send plots
- [ ] add functionality for group chats
- [x] convert currencies
  - `/convert 1 btc eur` -> `1 btc is 3500 eur`
    - new functionality is `/bitcoin value`
- [ ] maybe use these websites instead:
  - [BTC-ECHO Bitcoin][1]
  - [BTC-ECHO Ethereum][2]

## Supported Cryptocurrencies
- [Bitcoin][3] from [finanzen.net][4]
- [Ethereum][5] from [finanzen.net][6]
- [IOTA][7] from [finanzen.net][8]

## Collaborators
- [drgh0st][drgh0st]


[bot]: t.me/Crypt0Currency_Bot 'Write me!'
[drgh0st]: https://github.com/drgh0st 'drgh0st'
[1]: https://www.btc-echo.de/bitcoin-kurs/ 'bitcoin-kurs'
[2]: https://www.btc-echo.de/ether-kurs/ 'ether-kurs'
[3]: https://bitcoin.org/ 'bitcoin'
[5]: https://www.ethereum.org/ 'ethereum'
[4]: http://www.finanzen.net/devisen/bitcoin-euro-kurs 'bitcoin-euro-kurs'
[6]: http://www.finanzen.net/devisen/ethereum-euro-kurs 'ethereum-euro-kurs'
[7]: http://iota.org/
[8]: http://www.finanzen.net/devisen/iota-euro-kurs 'iota-euro-kurs'
