from telegram.ext import Updater
from os import getenv
import logging
import sqlite3
from quotes import Quotes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

conn_string = 'data/data.sqlite3'
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
        return quotes_random(bot, update)
    elif args[0] == 'search':
        return quotes_search(bot, update, ' '.join(args[2:]))
    else:
        bot.sendMessage(update.message.chat_id, text='usage /quote add|random|search')


def quotes_add(bot, update, args):
    if len(args) < 3:
        bot.sendMessage(update.message.chat_id, text='usage /quote add <author> <quote>')
    else:
        qmgr.refresh_connection()
        logging.log(25, (str(update.message.chat_id), args))
        qmgr.add(str(update.message.chat_id), args[1], ' '.join(args[2:]))
        qmgr.conn.close()
        bot.sendMessage(update.message.chat_id, text='quote aggiunto.')


def quotes_random(bot,update):
    qmgr.refresh_connection()
    mq = qmgr.random(update.message.chat_id)
    qmgr.conn.close()
    if mq is None:
        bot.sendMessage(update.message.chat_id, text="Non trovo nessuna quote")
    else:
        bot.sendMessage(update.message.chat_id, text=mq[2] + "\n\n" + mq[1])


def quotes_search(bot,update,arg):
    qmgr.refresh_connection()
    amq = qmgr.search(update.message.chat_id, arg)
    qmgr.conn.close()
    if len(amq) == 0:
        bot.sendMessage(update.message.chat_id, text="Non ho trovato nessun quote")
    else:
        for mq in amq:
            bot.sendMessage(update.message.chat_id, text=mq[2] + "\n" + mq[1])

def minimigrate(con):
    c = con.cursor()
    c.executescript("""
            CREATE TABLE IF NOT exists quotes (chat_id VARCHAR(128), author VARCHAR(128), quote TEXT);
            DROP TABLE IF EXISTS quotes_index;
            CREATE VIRTUAL TABLE quotes_index USING fts4(id, chat_id, author, quote);
            INSERT INTO quotes_index SELECT rowid, chat_id, author, quote FROM quotes;
    """)
    con.commit()


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
    conn = sqlite3.connect(conn_string)
    minimigrate(conn)
    conn.close()
    qmgr = Quotes(conn_string)
    main()
