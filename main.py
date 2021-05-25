import logging
import requests
import constraints as co
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',     #take time,level,name
                    level=logging.INFO)
logger = logging.getLogger(__name__)
print("Bot started...")
coinlist = []

# class Editlist:
#
#     def __init__(self):
#         self.coinlist_action = ""
#         self.coinlist = []
#         self.edit = 0
#         self.removable = ""
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

def edit_list():
    print("\nCOIN LIST =>", coinlist)
    while 1:
        coinlist_action = input("\nEnter 1 to add coin || 2 to remove coin || 3 to proceed: ")
        if coinlist_action == "1":
            add_coin()
        elif coinlist_action == "2":
            remove_coin()
        elif coinlist_action == "3":
            coinlist_action = ""
            break
    return coinlist


def take_input():
    while 1:
        c = input("\nEnter New Coin or 'N' to Proceed: ")
        if c == "n":
            break
        else:
            if c in main_list and c not in coinlist:
                coinlist.append(c)
                c = ""
            elif c not in main_list:
                print("\nInvalid Input!!!   Please check the spelling and enter Case sensitive input :)")
                continue
            elif c in coinlist:
                print("\nCoin Already Present")
                continue

def add_coin(update, context):
    while 1:
        update.message.reply_text("\nEnter New Coin or 'N' to Proceed: ")
        c = str(update.message.text)
        if c == "n":
            break
        else:
            if c in main_list and c not in coinlist:
                coinlist.append(c)
                c = ""
            elif c not in main_list:
                update.message.reply_text("\nInvalid Input!!!\nPlease check the spelling and enter Coin-name :)")
                continue
            elif c in coinlist:
                update.message.reply_text("\nCoin Already Present")
                continue

def remove_coin(update, context):
    update.message.reply_text("\nCOIN LIST =>", coinlist)
    while 1:
        update.message.reply_text("\nEnter coin name from the list to be removed or enter 'n' if done: ")
        removable = str(update.message.text)
        if removable == 'n':
            break
        elif removable in coinlist:
            coinlist.remove(removable)
            update.message.reply_text("\nCOIN LIST =>", coinlist)
        else:
            continue

def fetch_price():
    coinlist = ['bitcoin', 'Dogecoin', 'Ethereum']
    coinlist = "%2C".join(coinlist)
    pricelist = []

    fetch = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coinlist}&vs_currencies=inr").json()
    price_data = list(fetch.items())
    for coin, price in price_data:
        pricelist.append(str(coin) + ": ₹" + str(fetch[coin]['inr'] * 1.115))
    return pricelist


def start_command(update, context):
    name = update.message.from_user.first_name
    reply = "Hi!! {} Please add coins to track:".format(name)
    update.send_message(chat_id=update.message.chat_id, text=reply)

def help_command(update, context):
    update.message.reply_text("Go and ask google for help!")

def take_input(update, context):
    # update.message.reply_text("Hey! Please add coins to \nTrack: ")
    text = str(update.message.text)
    print(text)


def error_handling(update, context):
    print(f"Update {update} caused error: {context.error}")


def main():
    """Start the bot."""
    updater = Updater(token=co.Telegram_API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("add", add_coin))
    dp.add_handler(CommandHandler("remove", remove_coin))
    dp.add_handler(CommandHandler("fetch", fetch_price))
    dp.add_handler(MessageHandler(Filters.text, take_input))

    dp.add_error_handler(error_handling)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
