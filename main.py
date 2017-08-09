import logging

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import messages
import utils
from config import configfile
from modules.start_survey import StartSurveyModule
from modules.survey_results import SurveyResultsModule
from session import Sessions

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def help_command(bot, update):
    text = "A bot for groups"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


def main():
    #  define the updater
    updater = Updater(token=configfile.bot_token)

    # define the dispatcher
    dp = updater.dispatcher

    bmod = StartSurveyModule()
    bmod.create()

    surv_res = SurveyResultsModule()
    surv_res.create()

    bot_modules = [bmod, surv_res]
    sessions = Sessions(bot_modules)

    for bmod in bot_modules:
        if not bmod.bot_module_name:
            raise Exception('Invalid handlers detected')
        dp.add_handler(CommandHandler(bmod.bot_module_name, sessions.wrap_session_creation(bmod)))

    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), -1)

    # commands
    dp.add_handler(CommandHandler(('start', 'help'), help_command))
    dp.add_handler(CallbackQueryHandler(sessions.wrap_message_callback()))

    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command))
    # messages
    dp.add_handler(MessageHandler(~Filters.command, sessions.wrap_message_session(), edited_updates=True))

    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
