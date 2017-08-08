from modules.base_module import BaseModule
from telegram import ForceReply, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from session import SessionDiscard


# noinspection PyMethodMayBeStatic
def format_opts(opts):
    f = ""
    for opt in opts:
        f += opt + "\n"


class SurveysModule(BaseModule):
    start_survey_text = 'Start a survey'
    get_survey_question_text = 'Enter a survey question'
    enter_survey_option = 'Enter a survey answer, type "done" or "!" to finish'

    command_name = 'survey'
    name = 'Surveys'

    callback_dict = {
        'editq': {
            'question': None
        },
        'reseto': {
            'options': [],
            'options_completed': False
        },
        'discard': {
            'discard': True
        },
        'preview': {
            'preview': True
        }
    }

    def __init__(self):
        BaseModule.__init__(self)

    def handle_command(self, bot, update):
        chat_id = update.effective_chat.id
        bot.send_message(chat_id=chat_id, text=self.get_survey_question_text, parse_mode=ParseMode.HTML)
        return {
            'survey_completed': False,
            'options_completed': False,
            'question': None,
            'options': [],
        }

    def handle_message(self, session, bot, update):
        message = update.message
        chat_id = update.effective_chat.id

        if not session['question']:
            if message and message.text:
                session['question'] = message.text
                self.send_get_option_msg(bot, chat_id)
            else:
                bot.send_message(chat_id=chat_id, text=self.get_survey_question_text, parse_mode=ParseMode.HTML)
        elif not session['options_completed']:
            survey_option = message.text
            if survey_option.lower() not in ['!', 'done']:
                session['options'].append(survey_option)
                self.send_get_option_msg(bot, chat_id)
            else:
                session['options_completed'] = True

        bot.send_message(chat_id=chat_id, text="Options", parse_mode=ParseMode.HTML, reply_markup=
        self.create_options_keyboard(session))

    def send_get_option_msg(self, bot, chat_id):
        bot.send_message(chat_id=chat_id, text=self.enter_survey_option, parse_mode=ParseMode.HTML)

    def handle_callback(self, session, bot, update):
        if update.callback_query:
            chat_id = update.effective_chat.id
            data = self.callback_dict[update.callback_query.data]
            if 'discard' in data:
                raise SessionDiscard()
            if 'preview' in data:
                bot.send_message(chat_id=chat_id, text="Question: {}, Options:\n{}".format(session['question'], format_opts(session['options'])), parse_mode=ParseMode.HTML,
                                 reply_markup=self.create_options_keyboard(session))
                bot.send_message(chat_id=chat_id, text="Options", parse_mode=ParseMode.HTML, reply_markup=self.create_options_keyboard(session))
            else:
                session.update(data)

    def create(self):
        pass

    def create_options_keyboard(self, session):
        buttons_list = []

        if session['question']:
            buttons_list.append(
                InlineKeyboardButton(text='Edit Question', callback_data='editq')
            )

        if session['options_completed']:
            buttons_list.append(
                InlineKeyboardButton(text='Reset Options', callback_data='reseto')
            )

        buttons_list.append(
            InlineKeyboardButton(text='Discard Survey', callback_data='discard')
        )

        buttons_list.append(
            InlineKeyboardButton(text='Preview', callback_data='preview')
        )

        keyboard = InlineKeyboardMarkup([buttons_list])

        return keyboard
