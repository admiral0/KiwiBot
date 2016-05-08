from quotes import Quotes
import logging

logger = logging.getLogger(__name__)


def quote_dispatch(bot, update, args):
    assert Quotes.instance is not None
    if len(args) == 0:
        bot.sendMessage(update.message.chat_id, text='usage /quote add|random|search')
    elif args[0] == 'add':
        return quotes_add(bot, update, args)
    elif args[0] == 'random':
        return quotes_random(bot, update)
    elif args[0] == 'search':
        return quotes_search(bot, update, ' '.join(args[1:]))
    elif args[0] == 'read':
        return quotes_read(bot, update, args[1])
    else:
        bot.sendMessage(update.message.chat_id, text='usage /quote add|random|search')


def quotes_add(bot, update, args):
    if len(args) < 3:
        bot.sendMessage(update.message.chat_id, text='usage /quote add <author> <quote>')
    else:
        Quotes.instance.refresh_connection()
        logger.info((str(update.message.chat_id), args))
        Quotes.instance.add(str(update.message.chat_id), args[1], ' '.join(args[2:]))
        Quotes.instance.conn.close()
        bot.sendMessage(update.message.chat_id, text='Quote aggiunto.')


def quotes_random(bot, update):
    Quotes.instance.refresh_connection()
    mq = Quotes.instance.random(update.message.chat_id)
    Quotes.instance.conn.close()
    if mq is None:
        bot.sendMessage(update.message.chat_id, text="No quotes.")
    else:
        bot.sendMessage(update.message.chat_id, text=mq[2] + "\n\n" + mq[1])


def quotes_search(bot, update, arg):
    Quotes.instance.refresh_connection()
    amq = Quotes.instance.search(update.message.chat_id, arg)
    Quotes.instance.conn.close()
    if len(amq) == 0:
        bot.sendMessage(update.message.chat_id, text="Nessun risultato")
    else:
        res = 'Risultati contenenti "{}": {}'
        ris = []
        for mq in amq:
            ris.append(mq[0])
        bot.sendMessage(update.message.chat_id, text=res.format(arg, str(ris)))


def quotes_read(bot, update, rowid):
    Quotes.instance.refresh_connection()
    mq = Quotes.instance.get(update.message.chat_id, rowid)
    Quotes.instance.conn.close()
    if mq is None:
        bot.sendMessage(update.message.chat_id, text='Errore: Quote inesistente')
    else:
        bot.sendMessage(update.message.chat_id, text=mq[2] + "\n" + mq[1])
