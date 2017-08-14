from modules.base_module import BaseModule
from telegram import ForceReply, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from session import SessionDiscard
import database
import time
import requests

import urllib,json,os

# the token of the bot you get from t.me/botfather (type: str)
giphy_token = os.environ.get('GIPHY_TOKEN')


class CatModule(BaseModule):
    bot_module_name = 'randcat'
    name = 'random key'
    welcome_text = 'hi!'

    def __init__(self):
        BaseModule.__init__(self)


    def create(self):
        pass


    def handle_command(self, bot, update):
        url = self.get_random_gif_url()
        bot.sendDocument(chat_id= update.effective_chat.id, document=url)
        return

    def handle_message(self, session, bot, update):
        pass


    def handle_callback(self, session, bot, update):
        pass


    def handle_async_callback(self, bot, update, query):
        pass

    def get_random_gif_url(self):

        token = os.environ.get('GIPHY_TOKEN')
        request_url = "https://api.giphy.com/v1/gifs/random?api_key=" + token + "&tag=kittens&rating=G"

        resp = requests.get(request_url)
        data = json.loads(resp.content)
        return data['data']['image_original_url']



