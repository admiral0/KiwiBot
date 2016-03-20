from telegram import Updater
from os import getenv


def help_message(bot, update):
    bot.sendMessage(update.message.chat_id, text='Nothing to see here yet.')


def main():
    botapi = getenv('KIWI_BOT_API_KEY')
    updater = Updater(botapi)

    dp = updater.dispatcher
''
    dp.addTelegramCommandHandler("help", help_message)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
