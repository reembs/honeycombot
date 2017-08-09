import time

import database
import keyboards


def get_int_time(update):
    return int(time.mktime(update.message.date.timetuple()))


def before_processing(bot, update):
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    int_time = get_int_time(update)
    if update.effective_chat.type != "private":
        chat_id = update.effective_chat.id
        chat_name = update.effective_chat.title
        database.add_user_group(user_id, chat_id, chat_name, int_time)
        keyboard = keyboards.private_chat_kb()
        if update.message and update.message.text:
            text = "Address me privately, please"
            update.effective_message.reply_text(text=text, reply_markup=keyboard)
        update.message = None
    database.add_user_db(user_id, username, int_time)