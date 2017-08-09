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
