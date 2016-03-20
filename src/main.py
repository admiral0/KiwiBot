from telegram import Updater
from os import getenv
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def help_message(bot, update):
    bot.sendMessage(update.message.chat_id, text='Nothing to see here yet.')


def main():
    botapi = getenv('KIWI_BOT_API_KEY')
    updater = Updater(botapi)

    dp = updater.dispatcher

    dp.addTelegramCommandHandler("help", help_message)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
