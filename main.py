import logging
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
import os
from os import environ
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',     #take time,level,name
                    level=logging.INFO)
logger = logging.getLogger(__name__)

main_list = ['usdt', 'btc', 'bchold', 'ltc', 'xrp', 'dash', 'eth', 'trx', 'eos', 'zil', 'ncash', 'bat', 'gnt',
     'storm', 'req', 'sub', 'nuls', 'icx', 'omg', 'poly', 'iost', 'snt', 'npxs', 'cs', 'fun', 'poe', 'theta',
     'dent', 'qkc', 'stq', 'zco', 'hot', 'ocn', 'noah', 'banca', 'wrx', 'matic', 'bch', 'bnb', 'btt', 'yfi',
     'uni', 'link', 'sxp', 'ada', 'atom', 'xlm', 'xem', 'zec', 'busd', 'yfii', 'doge', 'dot', 'vet', 'easy',
     'crv', 'ren', 'enj', 'mana', 'hbar', 'uma', 'chr', 'paxg', '1inch', 'etc', 'uft', 'dock', 'fil', 'win',
     'tko', 'push', 'avax', 'luna', 'xvg', 'sc', 'ftt', 'dgb', 'cvc', 'cake', 'ez', 'bzrx', 'ftm', 'hnt', 'ark',
     'ctsi', 'kmd', 'coti', 'iotx', 'shib', 'rlc', 'trb', 'reef', 'icp', 'ont', 'xvs', 'zrx']


def get_price_from_file():
    coinlist = []
    coin_record = open("coins.txt", "r")
    ls = coin_record.readlines()
    for item in ls:
        coinlist.append(item.strip())
    coin_record.close()
    # print("\nCOIN LIST =>", *self.coinlist)


def send_price_to_file():
    coin_record = open("coins.txt", "w+")
    for item in coinlist:
        coin_record.write(item + '\n')
    coin_record.close()


def start_command(update, context):
    send_price_to_file()
    name = update.message.from_user.first_name
    reply = "Hi!! {} Please add coins to track:".format(name)
    update.message.reply_text(reply)


def help_command(update, context):
    update.message.reply_text('''
Here are some commands you can use with this bot\n
/start : start the bot\n
/help : see commands\n
/add <coin> : add coin to tracking list\n
/remove <coin> : remove coin from tracking list\n
/show : show current coinlist\n
/fetch : fetch prices of coinlist\n
beta version-
/repeat <time interval in min>: send prices automatically after specified interval
''')


def look_for(c):
    get_price_from_file()
    if c in main_list:
        return True
    for x in main_list:
        if x.lower() == c or x.upper() == c:
            return True
    return False


def add_coin(update, context):
    c = str(update.effective_message.text)[5:].lower()
    get_price_from_file()
    if len(c) < 2:
        update.message.reply_text("please send coin name with the command")
        time.sleep(2)
        update.message.reply_text("for example:\n/add Bitcoin")
        return
    elif c in coinlist:
        update.message.reply_text("\nCoin Already being tracked ")
        update.message.reply_text("😎")
    elif look_for(c):
        coinlist.append(c)
        send_price_to_file()
        update.message.reply_text(c + " added ✍🏼")
        c = ""
    else:
        update.message.reply_text("\nInvalid Input!!!\nUnsupported Coin-name ")
        update.message.reply_text("😒")
        print(c, "not in list")


def remove_coin(update, context):
    c = str(update.effective_message.text)[8:].lower()
    if len(c) < 2:
        update.message.reply_text("Please send coin name with the command")
        update.message.reply_text("for example:\n/remove Bitcoin")
        return
    if c in coinlist:
        coinlist.remove(c)
        update.message.reply_text(c + " removed 🤝🏼\nNow tracking: " + " ".join(coinlist))
        send_price_to_file()
    else:
        update.message.reply_text("\nCoin is already not being tracked anyway!! ")
        update.message.reply_text("😏")


def show_coins(update, context):
    get_price_from_file()
    if len(coinlist) == 0:
        update.message.reply_text("No Coin in tracking list!! ")
    else:
        update.message.reply_text(" ".join(coinlist))


def fetch_price(update, context):
    get_price_from_file()
    a = coinlist
    pricelist = []
    fetch = requests.get(f'https://api.wazirx.com/api/v2/market-status').json()
    for i in fetch['markets']:
        if i['quoteMarket'] == 'inr' and i['baseMarket'] in a:
            pricelist.append(str(i['baseMarket'] + " : " + i['buy'] + '\n'))
    a = "".join(pricelist)
    update.message.reply_text(a)


def repeat_fetch(context: telegram.ext.CallbackContext):
    get_price_from_file()
    a = coinlist
    pricelist = []
    fetch = requests.get(f'https://api.wazirx.com/api/v2/market-status').json()
    for i in fetch['markets']:
        if i['quoteMarket'] == 'inr' and i['baseMarket'] in a:
            pricelist.append(str(i['baseMarket'] + " : " + i['buy'] + '\n'))
    a = "".join(pricelist)
    context.bot.send_message(chat_id=context.job.context, text=a)


def take_input(update, context):
    text = list(str(update.message.text).strip().split())
    for x in text:
        x = x.lower()
        if look_for(x):
            fetch = requests.get(f'https://api.wazirx.com/api/v2/market-status').json()
            for i in fetch['markets']:
                if i['quoteMarket'] == 'inr' and i['baseMarket'] in x:
                    a = str(i['baseMarket'] + " : " + i['buy'])
                    update.message.reply_text(a)
            continue


def command_handler(update, context):
    update.message.reply_text(f"Command: {update.message.text} not found!!")


def repeat(update, context):
    interval = str(update.effective_message.text)[8:]
    if len(interval) == 0:
        update.message.reply_text("Please enter time (in minutes) with the command")
        update.message.reply_text("for example:\n/repeat 5")
        return
    context.bot.send_message(chat_id=update.message.chat_id, text='repeater scheduled for {} minutes({} seconds)!'
                             .format(interval, float(interval)*60))
    print('repeater scheduled for {} minutes!'.format(interval))
    context.job_queue.run_repeating(repeat_fetch, float(interval)*60, first=5, context=update.message.chat_id)


def error_handling(update, context):
    print(f"Update {update} caused error: {context.error}")


def main():
    """Start the bot."""
    updater = Updater(token=Telegram_API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("add", add_coin))
    dp.add_handler(CommandHandler("remove", remove_coin))
    dp.add_handler(CommandHandler("show", show_coins))
    dp.add_handler(CommandHandler("fetch", fetch_price))
    dp.add_handler(CommandHandler("repeat", repeat))
    # dp.add_handler(CommandHandler('stop', Stop))
    dp.add_handler(MessageHandler(Filters.command, command_handler))
    dp.add_handler(MessageHandler(Filters.text, take_input))

    dp.add_error_handler(error_handling)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    Telegram_API_KEY = environ['Telegram_API_KEY']
    coinlist = ['btc', 'doge', 'ada', 'dgb', 'zil', 'sxp', 'eth',
                'vet', 'xem', 'iost']
    main()
