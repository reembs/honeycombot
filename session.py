import re

import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

import config.configfile
import users


def time_from_time_tup(time_tuple):
    return int(time.mktime(time_tuple))


class Sessions:
    sessions = {}
    modules = None

    def __init__(self, modules):
        self.modules = modules

    def wrap_session_creation(self, bot_module):
        def wrapper(bot, update):
            self.before_processing(bot, update)
            response = bot_module.handle_command(bot, update)
            if response:
                self.sessions[update.effective_chat.id] = {
                    'module': bot_module,
                    'data': response
                }

        return wrapper

    def wrap_message_session(self):
        def wrapper(bot, update):
            self.before_processing(bot, update)
            if update.effective_chat.id in self.sessions:
                session = self.sessions[update.effective_chat.id]
                try:
                    session['module'].handle_message(session['data'], bot, update)
                except SessionDiscard:
                    del self.sessions[update.effective_chat.id]

        return wrapper

    def wrap_message_callback(self):
        def wrapper(bot, update):
            query_data = None
            if update.callback_query:
                query_data = update.callback_query.data
                if query_data:
                    now = int(time.time())
                    users.add_user_db(update.effective_user.id, update.effective_user.username, now)
                    users.add_user_group(update.effective_user.id,
                                         update.effective_chat.id,
                                         update.effective_chat.title,
                                         now)

            if query_data:
                match = re.match('m\[(.*)\](.+)', query_data)
                if match:
                    module_name = match.group(1)
                    relevant_modules = list(filter(lambda m: m.bot_module_name == module_name, self.modules))
                    if len(relevant_modules) == 1:
                        relevant_modules[0].handle_async_callback(bot, update, match.group(2))
                        return

            if update.effective_chat.id in self.sessions:
                session = self.sessions[update.effective_chat.id]
                try:
                    session['module'].handle_callback(session['data'], bot, update)
                except SessionDiscard:
                    del self.sessions[update.effective_chat.id]

        return wrapper

    def before_processing(self, bot, update):
        user_id = update.effective_message.from_user.id
        username = update.effective_message.from_user.username
        int_time = time_from_time_tup(update.message.date.timetuple())
        if update.effective_chat.type != "private":
            chat_id = update.effective_chat.id
            chat_name = update.effective_chat.title
            users.add_user_group(user_id, chat_id, chat_name, int_time)
            if update.message and update.message.text:
                text = "Address me privately, please"
                update.effective_message.reply_text(text=text, reply_markup=self.create_private_summon())
            update.message = None
        users.add_user_db(user_id, username, int_time)

    def create_private_summon(self):
        bot_link = "https://t.me/{}".format(Bot(config.configfile.bot_token).getMe().username)
        button0 = InlineKeyboardButton(text="Private chat", url=bot_link)
        buttons_list = [[button0]]
        keyboard = InlineKeyboardMarkup(buttons_list)
        return keyboard


class SessionDiscard(Exception):
    pass
