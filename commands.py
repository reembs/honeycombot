from telegram import ParseMode
from telegram import MessageEntity
from telegram import ParseMode

import utils
import database
import keyboards
import constants


def commands_query_handler(bot, update):
    if update.callback_query:
        query = update.callback_query
        if query.data == 'start_survey':
            chat_id = update.effective_chat.id
            bot.send_message(chat_id=chat_id, text=constants.get_survey_question_text, parse_mode=ParseMode.HTML,
                             reply_markup=keyboards.force_reply())


def help_command(bot, update):
    keyboard = keyboards.see_commands()
    text = "A bot for groups"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


@utils.only_admin
def stats(bot, update):
    update.message.reply_text(text=database.stats_text(), parse_mode=ParseMode.HTML)
