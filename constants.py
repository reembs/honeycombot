from config import configfile

from telegram import Bot

GET_ME = Bot(configfile.bot_token).getMe()

