import re


class Sessions:
    sessions = {}
    modules = None

    def __init__(self, modules):
        self.modules = modules

    def wrap_session_creation(self, bot_module):
        def wrapper(bot, update):
            response = bot_module.handle_command(bot, update)
            if response:
                self.sessions[update.effective_chat.id] = {
                    'module': bot_module,
                    'data': response
                }

        return wrapper

    def wrap_message_session(self):
        def wrapper(bot, update):
            if update.effective_chat.id in self.sessions:
                session = self.sessions[update.effective_chat.id]
                try:
                    session['module'].handle_message(session['data'], bot, update)
                except SessionDiscard:
                    del self.sessions[update.effective_chat.id]

        return wrapper

    def wrap_message_callback(self):
        def wrapper(bot, update):
            if update.effective_chat.id in self.sessions:
                session = self.sessions[update.effective_chat.id]
                try:
                    session['module'].handle_callback(session['data'], bot, update)
                except SessionDiscard:
                    del self.sessions[update.effective_chat.id]
            else:
                if update.callback_query:
                    query_data = update.callback_query.data
                    match = re.match('m\[(.*)\](.+)', query_data)
                    if match:
                        module_name = match.group(1)
                        for m in self.modules:
                            if m.bot_module_name == module_name:
                                m.handle_async_callback(bot, update, match.group(2))
                                break
        return wrapper


class SessionDiscard(Exception):
    pass
