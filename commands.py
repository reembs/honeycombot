# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017  Dario dariomsn@hotmail.it

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
