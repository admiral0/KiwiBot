from telegram import Updater
from os import getenv
import logging
import sqlite3
from quotes import Quotes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

conn = None
qmgr = None


def help_message(bot, update):
    bot.sendMessage(update.message.chat_id, text='RTFM.')


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Ciao!')


def quote_dispatch(bot,update,args):
    if len(args) == 0:
        bot.sendMessage(update.message.chat_id, text='usage /quote add|random|search')
    elif args[0] == 'add':
        return quotes_add(bot, update, args)
    elif args[0] == 'random':
        return quotes_random(bot,update)
    else:
        bot.sendMessage(update.message.chat_id, text='usage /quote add|random|search')


def quotes_add(bot, update, args):
    if len(args) < 3:
        bot.sendMessage(update.message.chat_id, text='usage /quote add <author> <quote>')
    else:
        qmgr.add(str(update.message.chat_id), args[1], ' '.join(args[2:]))


def quotes_random(bot,update):
    mq = qmgr.random(update.message.chat_id)
    if mq is None:
        bot.sendMessage(update.message.chat_id, "Non trovo nessuna quote")
    bot.sendMessage(update.message.chat_id, mq[2] + "\n\n" + mq[1])


def minimigrate(con):
    c = con.cursor()
    c.execute("""
            CREATE TABLE if not exists quotes (chat_id VARCHAR(128), author VARCHAR(128), quote TEXT);
    """)


def main():

    botapi = getenv('KIWI_BOT_API_KEY')
    updater = Updater(botapi)

    dp = updater.dispatcher

    dp.addTelegramCommandHandler("help", help_message)
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("quote", quote_dispatch)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    conn = sqlite3.connect('data/data.sqlite3')
    minimigrate(conn)
    qmgr = Quotes(conn)
    main()
