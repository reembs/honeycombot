class BaseModule:
    bot_module_name = None
    name = None

    def __init__(self):
        pass

    def create(self):
        pass

    def handle_command(self, bot, update):
        return None

    def handle_message(self, session, bot, update):
        pass

    def handle_callback(self, session, bot, update):
        pass

    def handle_async_callback(self, bot, update, query):
        pass
