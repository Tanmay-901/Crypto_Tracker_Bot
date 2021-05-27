import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from os import environ
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',     #take time,level,name
                    level=logging.INFO)
logger = logging.getLogger(__name__)

main_list = ['Zilliqa', 'Band Protocol', 'Algorand', 'Theta Network', 'iExec RLC', 'Cosmos',
                  'DigiByte', 'Chiliz', 'Terra', 'Theta Fuel', 'Waves', 'Nano', 'IOST', 'Tezos',
                  'VeChain', 'DOT', 'Elrond', 'NEM', 'Filecoin', 'Bitcoin', 'Ethereum', 'Dogecoin',
                  'Ripple', 'Tron', 'Binance Coin', 'Cardano', 'Bitcoin Cash', 'EOS', 'GAS', 'NEO',
                  'Litecoin', 'Chainlink', 'Tether', 'Dash', 'Aave', 'Uniswap', 'True USD', 'USD Coin',
                  'Compound', '0x', 'AdEx', 'Augur', 'Bancor', 'Basic Attention Token', 'Civic', 'Enjin Coin',
                  'Fetch.ai', 'Golem', 'Kyber Network', 'Metal', 'OmiseGO', 'Paxos Standard Token', 'Power Ledger',
                  'DIA', 'Sushi', 'Quantstamp', 'Numeraire', 'yearn.finance', 'Dai', 'Loopring', 'AirSwap',
                  'Republic Protocol', 'Maker', 'QuarkChain', 'Swipe', 'Synthetix Network Token', 'Stellar',
                  'DFI.money', 'Ripio Credit Network', 'Status', 'Storj', 'aelf', 'district0x']


def start_command(update, context):
    name = update.message.from_user.first_name
    reply = "Hi!! {} Please add coins to track:".format(name)
    update.message.reply_text(reply)


def help_command(update, context):
    update.message.reply_text("Go and ask google for help! 😏")
    time.sleep(2)
    update.message.reply_text('''
Just kidding!!\nHere are some commands you can use in this bot\n
/start : start the bot\n
/help : see commands\n
/add <coin> : add coin to tracker\n
/remove <coin> : remove coin from tracker\n
/show : show current coinlist\n
/fetch : fetch prices\n
''')


def look_for(c):
    if c in main_list:
        return True
    for x in main_list:
        if x.lower() == c or x.upper() == c:
            return True
    return False


def add_coin(update, context):
    c = str(update.effective_message.text)[5:]
    if len(c) <= 2:
        update.message.reply_text("Abe Coin name to daal 🤨")
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("for example:\n/add Bitcoin")
        return
    elif c in coinlist:
        update.message.reply_text("\nCoin Already being tracked ")
        update.message.reply_text("😎")
    if look_for(c) and c not in coinlist:
        coinlist.append(c)
        update.message.reply_text(c + " added ✍🏼")
        c = ""
    else:
        update.message.reply_text("\nInvalid Input!!!\nUnsupported Coin-name ")
        update.message.reply_text("😒")
        print(c, "not in list")


def remove_coin(update, context):
    c = str(update.effective_message.text)[8:]
    if len(c) < 2:
        update.message.reply_text("Abe Coin name to daal 🤨")
        time.sleep(2)
        update.message.reply_text("for example:\n/remove Bitcoin")
        return
    if c in coinlist:
        coinlist.remove(c)
        update.message.reply_text(c + " removed 🤝🏼\nNow tracking: " + " ".join(coinlist))
    else:
        update.message.reply_text("\nCoin is already not being tracked anyway!! ")
        update.message.reply_text("😏")


def show_coins(update, context):
    update.message.reply_text(" ".join(coinlist))


def fetch_price(update, context):
    a = "%2C".join(coinlist)
    pricelist = []
    fetch = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={a}&vs_currencies=inr").json()
    price_data = list(fetch.items())
    for coin, price in price_data:
        # print("%.2f" % (fetch[coin]['inr'] * 1.115))
        pricelist.append(str(coin) + " : ₹" + str("%.2f" % (fetch[coin]['inr'] * 1.11)) + "\n")
    a = "".join(pricelist)
    update.message.reply_text(a)


def take_input(update, context):
    text = list(str(update.message.text).strip().split())
    # if " " in text:
    #     text = text.split()
    hi = ["Hi", "hi", "Hii", "hii", "hello", "Hello"]
    bhag = ["bhag", "Bhag", "bhaag", "Bhaag", "Bhag ja", " bhag ja"]
    love = ["Love", "love"]
    print(text)
    if text[0][0] == "/":
        update.message.reply_text("Jaa re")
        time.sleep(2)
        update.message.reply_text("Command not found")
        return
    for i in text:
        if look_for(i):
            fetch = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={i}&vs_currencies=inr").json()
            price_data = list(fetch.items())
            for coin, price in price_data:
                update.message.reply_text(str(coin) + " : ₹" + str("%.2f" % (fetch[coin]['inr'] * 1.11)) + "\n")
                continue
    if any(x in text for x in bhag):
        update.message.reply_text("Bhagau kya abhi 😒")
        return
    elif any(x in text for x in love):
        update.message.reply_text("🙈")
        return
    elif text[0] in hi:
        context.bot.send_message(update.effective_chat.id, "hello!!! 😋")
        return



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
    dp.add_handler(MessageHandler(Filters.text, take_input))

    dp.add_error_handler(error_handling)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    Telegram_API_KEY = environ['Telegram_API_KEY']
    coinlist = []
    main()
