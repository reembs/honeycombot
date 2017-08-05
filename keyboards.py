from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ForceReply

import constants


def github_link_kb():
    button0 = InlineKeyboardButton(text="Source code", url="https://github.com/91DarioDev/ForwardsCoverBot")
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def private_chat_kb():
    bot_link = "https://t.me/{}".format(constants.GET_ME.username)
    button0 = InlineKeyboardButton(text="Private chat", url=bot_link)
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def force_reply():
    return ForceReply()


def see_commands():
    button0 = InlineKeyboardButton(text=constants.start_survey_text, callback_data="start_survey")
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard
