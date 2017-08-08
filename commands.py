from telegram import ParseMode


def help_command(bot, update):
    text = "A bot for groups"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

