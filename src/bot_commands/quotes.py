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