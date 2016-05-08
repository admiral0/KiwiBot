from telegram.ext import Updater
from os import getenv
import logging
import sqlite3
from quotes import Quotes
from dbutil import minimigrate
from bot_commands import quote_dispatch, help_message

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

conn_string = 'data/data.sqlite3'

def main():
    bot_api = getenv('KIWI_BOT_API_KEY')
    updater = Updater(bot_api)

    dp = updater.dispatcher

    dp.addTelegramCommandHandler("help", help_message)
    dp.addTelegramCommandHandler("quote", quote_dispatch)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    conn = sqlite3.connect(conn_string)
    minimigrate(conn)
    conn.close()
    Quotes(conn_string)
    main()
