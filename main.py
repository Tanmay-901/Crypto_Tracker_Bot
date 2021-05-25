import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from os import environ

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',     #take time,level,name
                    level=logging.INFO)
logger = logging.getLogger(__name__)
print("Bot started...")

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


def add_coin(update, context):
    c = str(update.effective_message.text)[5:]
    if c in main_list and c not in coinlist:
        coinlist.append(c)
        print("added: ", c)
        c = ""
    elif c not in main_list:
        update.message.reply_text("\nInvalid Input!!!\nUnsupported Coin-name ")
        update.message.reply_text("😒")
        print(c, "not in list")
    elif c in coinlist:
        update.message.reply_text("\nCoin Already being tracked ")
        update.message.reply_text("😎")
        print(c, "already present")


def remove_coin(update, context):
    c = str(update.effective_message.text)[8:]
    print("remove request:", c)
    if c in coinlist:
        coinlist.remove(c)
        update.message.reply_text(coinlist)
    else:
        update.message.reply_text("\nCoin is not being tracked already ")


def fetch_price(update, context):
    print(coinlist)
    a = "%2C".join(coinlist)
    # a = coinlist[0]
    print(a)
    pricelist = []

    fetch = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={a}&vs_currencies=inr").json()
    price_data = list(fetch.items())
    for coin, price in price_data:
        # pricelist.append(str(coin) + ": ₹" + str(fetch[coin]['inr'] * 1.115))
        pricelist.append(str(coin) + ":" + str(fetch[coin]['inr'] * 1.115) + "\n")
    update.message.reply_text(pricelist)
    print(pricelist)



def start_command(update, context):
    name = update.message.from_user.first_name
    reply = "Hi!! {} Please add coins to track:".format(name)
    update.message.reply_text(reply)


def help_command(update, context):
    update.message.reply_text("Go and ask google for help!")


def show_coins(update, context):
    update.message.reply_text(coinlist)


def take_input(update, context):
    text = str(update.message.text)
    print(text)


# def error_handling(update, context):
#     print(f"Update {update} caused error: {context.error}")


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

    # dp.add_error_handler(error_handling)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    Telegram_API_KEY = environ['Telegram_API_KEY']
    coinlist = []
    main()
