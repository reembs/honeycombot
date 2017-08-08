class Sessions:
    sessions = {}

    def wrap_session_creation(self, bot_module):
        def wrapper(bot, update):
            response = bot_module.handle_command(bot, update)
            if response:
                self.sessions[update.effective_chat.id] = {
                    'module': bot_module,
                    'data': response
                }

        return wrapper

    def wrap_message_session(self, bot_module):
        def wrapper(bot, update):
            if update.effective_chat.id in self.sessions:
                session = self.sessions[update.effective_chat.id]
                try:
                    bot_module.handle_message(session['data'], bot, update)
                except SessionDiscard:
                    del self.sessions[update.effective_chat.id]

        return wrapper

    def wrap_message_callback(self, bot_module):
        def wrapper(bot, update):
            if update.effective_chat.id in self.sessions:
                session = self.sessions[update.effective_chat.id]
                try:
                    bot_module.handle_callback(session['data'], bot, update)
                except SessionDiscard:
                    del self.sessions[update.effective_chat.id]

        return wrapper


class SessionDiscard(Exception):
    pass
