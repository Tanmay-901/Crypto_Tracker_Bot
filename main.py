import logging
import constraints as co
import Editlist as el
from telegram.ext import *

print("Bot started...")
# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)


def start_command(update, context):
    update.message.reply_text("Hey! Please add coins to \nTrack: ")
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Hey! Please add coins to \ntrack:")

def help_command(update, context):
    update.message.reply_text("If you need help, you should ask google for it!")

def take_input(update, context):
    text = str(update.message.text)
    response = el.Editlist.take_input(text)
    update.message.reply_text(response)

def error_handling(update, context):
    print(f"Update {update} caused error: {context.error}")


def main():
    """Start the bot."""
    updater = Updater(token=co.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(CommandHandler(Filters.text, take_input))

    dp.add_error_handler(error_handling)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
