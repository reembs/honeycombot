import logging

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

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


def invalid_command(bot, update):
    text = "I don't know what that means"
    update.message.reply_text(text=text, quote=True)


def main():
    updater = Updater(token=configfile.bot_token)
    dp = updater.dispatcher

    bot_modules = [SurveyResultsModule(), SurveyResultsModule()]

    for bot_module in bot_modules:
        bot_module.create()

    sessions = Sessions(bot_modules)

    for bot_module in bot_modules:
        if not bot_module.bot_module_name:
            raise Exception('Invalid handlers detected')
        dp.add_handler(CommandHandler(bot_module.bot_module_name, sessions.wrap_session_creation(bot_module)))

    dp.add_handler(CommandHandler(('start', 'help'), help_command))
    dp.add_handler(CallbackQueryHandler(sessions.wrap_message_callback()))
    dp.add_handler(MessageHandler(Filters.command, invalid_command))
    dp.add_handler(MessageHandler(~Filters.command, sessions.wrap_message_session(), edited_updates=True))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
