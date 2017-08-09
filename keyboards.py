from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ForceReply

import constants


def private_chat_kb():
    bot_link = "https://t.me/{}".format(constants.GET_ME.username)
    button0 = InlineKeyboardButton(text="Private chat", url=bot_link)
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard
