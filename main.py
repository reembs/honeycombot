import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import commands
import messages
import utils
from config import configfile

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

SLEEP_TIME_SECS = 5


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    #  define the updater
    updater = Updater(token=configfile.bot_token)

    # define the dispatcher
    dp = updater.dispatcher

    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), -1)
    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command))
    dp.add_handler(CallbackQueryHandler(commands.commands_query_handler))
    dp.add_handler(CommandHandler('stats', commands.stats))
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command))
    # messages
    dp.add_handler(MessageHandler(~Filters.command, messages.process_message, edited_updates=True))

    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
