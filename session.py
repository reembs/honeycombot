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
            if update.effective_message and update.effective_message.text and update.effective_chat.type != "private":
                text = "Address me privately, please"
                update.effective_message.reply_text(text=text, reply_markup=self.create_private_summon())
                return

            response = bot_module.handle_command(bot, update)
            if response:
                self.sessions[update.effective_chat.id] = {
                    'module': bot_module,
                    'data': response
                }

        return wrapper

    def update_user_group(self, chat, user, int_time):
        if user:
            user_id = user.id
            users.add_user_db(user_id, self.get_user_naming(user), int_time)
            if chat and chat.type != "private":
                chat_id = chat.id
                chat_name = chat.title
                users.add_user_group(user_id, chat_id, chat_name, int_time)

    def before_processing(self, bot, update):
        if update.effective_message and update.effective_message.from_user:
            int_time = time_from_time_tup(update.effective_message.date.timetuple())
            self.update_user_group(update.effective_chat, update.effective_message.from_user, int_time)

    def wrap_message_session(self, bot, update):
        self.before_processing(bot, update)
        if update.effective_chat.id in self.sessions:
            session = self.sessions[update.effective_chat.id]
            try:
                session['module'].handle_message(session['data'], bot, update)
            except SessionDiscard:
                del self.sessions[update.effective_chat.id]

    def wrap_message_callback(self):
        def wrapper(bot, update):
            if update.effective_user:
                self.update_user_group(update.effective_chat, update.effective_user, int(time.time()))

            if update.callback_query:
                query_data = update.callback_query.data
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

    def create_private_summon(self):
        bot_link = "https://t.me/{}".format(Bot(config.configfile.bot_token).getMe().username)
        button0 = InlineKeyboardButton(text="Private chat", url=bot_link)
        buttons_list = [[button0]]
        keyboard = InlineKeyboardMarkup(buttons_list)
        return keyboard

    def get_user_naming(self, user):
        if user.username:
            if user.last_name:
                return user.username + " (" + user.first_name + " " + user.last_name + ')'
            return user.username + " (" + user.first_name + ')'
        else:
            if user.last_name:
                return user.first_name + " " + user.last_name
            return user.first_name


class SessionDiscard(Exception):
    pass
