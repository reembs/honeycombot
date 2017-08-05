from functools import wraps
from config import configfile

import locale

locale.setlocale(locale.LC_ALL, "")


def n_dots(number):
    number = locale.format("%d", number, grouping=True)
    return number


def invalid_command(bot, update):
    text = "This command is invalid"
    update.message.reply_text(text=text, quote=True)


def only_admin(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.from_user.id not in configfile.admins:
            invalid_command(bot, update, *args, **kwargs)
            return
        return func(bot, update, *args, **kwargs)

    return wrapped
