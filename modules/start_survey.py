from modules.base_module import BaseModule
from telegram import ForceReply, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from session import SessionDiscard
import database
import time


# noinspection PyMethodMayBeStatic
def format_opts(opts):
    f = ""
    for opt in opts:
        f += opt + "\n"
    return f


class StartSurveyModule(BaseModule):
    start_survey_text = 'Start a survey'
    get_survey_question_text = 'Enter a survey question'
    enter_survey_option = 'Enter a survey answer, type "done" or "!" to finish'

    bot_module_name = 'survey'
    name = 'Create Survey'

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
        },
        'send': {
            'sendPressed': True
        },
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
            'sendPressed': False,
            'userId': update.effective_message.from_user.id,
            'userName': update.effective_message.from_user.name,
        }

    def prompt(self, session, bot, chat_id):
        if not session['question']:
            bot.send_message(chat_id=chat_id, text=self.get_survey_question_text, parse_mode=ParseMode.HTML)
        elif not session['options_completed']:
            self.send_get_option_msg(bot, chat_id)

        if session['sendPressed']:
            res_set = database.query_r('SELECT group_name, group_id FROM user_groups WHERE user_id=?', session['userId'])
            bot.send_message(chat_id=chat_id, text="Where should the survey be posted?", parse_mode=ParseMode.HTML, reply_markup=
                             self.create_send_choice_keyboard(session, res_set))

        else:
            bot.send_message(chat_id=chat_id, text="What would you like to do next?", parse_mode=ParseMode.HTML, reply_markup=
                             self.create_options_keyboard(session))

    def handle_message(self, session, bot, update):
        message = update.message
        chat_id = update.effective_chat.id

        if not session['question']:
            if message and message.text:
                session['question'] = message.text
        elif not session['options_completed']:
            survey_option = message.text
            if survey_option.lower() not in ['!', 'done']:
                session['options'].append(survey_option)
            else:
                session['options_completed'] = True

        self.prompt(session, bot, chat_id)

    def send_get_option_msg(self, bot, chat_id):
        bot.send_message(chat_id=chat_id, text=self.enter_survey_option, parse_mode=ParseMode.HTML)

    def handle_async_callback(self, bot, update, query):
        if update.callback_query and query and query.startswith('opt_ans_'):
            answered = False
            try:
                uid = update.effective_user.id
                gid = update.effective_chat.id
                opt_id = int(query.split('opt_ans_')[1])

                sid, t_gid = database.query_r('SELECT s.survey_id, s.group_id'
                                              '  FROM survey_options o, surveys s '
                                              ' WHERE o.survey_id = s.survey_id '
                                              '   AND option_id=?', opt_id)[0]

                answered = True
                if t_gid == gid:
                    rows = database.query_r(
                        'SELECT s.answer_id'
                        '  FROM survey_answers s, survey_options o '
                        ' WHERE s.user_id = ? AND s.survey_id = ?'
                        '   AND o.option_id=s.option_id', uid, sid)

                    if not rows:
                        database.query_w('INSERT INTO survey_answers (option_id, survey_id, user_id) '
                                         'VALUES (?, ?, ?)', opt_id, sid, uid)
                        action = 'submitted'
                    else:
                        database.query_w('UPDATE survey_answers SET option_id=? '
                                         ' WHERE answer_id=?', opt_id, rows[0][0])
                        action = 'updated'

                    bot.answerCallbackQuery(update.callback_query.id, text='Your selection was {}'.format(action))
                else:
                    bot.answerCallbackQuery(update.callback_query.id, text='Failure to submit')
            finally:
                if not answered:
                    bot.answerCallbackQuery(update.callback_query.id)

    def handle_callback(self, session, bot, update):
        if update.callback_query:
            try:
                chat_id = update.effective_chat.id
                query_data = update.callback_query.data

                if query_data == 'send_back':
                    session['sendPressed'] = False
                elif query_data.startswith('send_'):
                    gid = int(query_data.split('_')[1])

                    sid = database.insert_auto_inc(
                        'INSERT INTO surveys (user_id, group_id, survey_question, created, valid) '
                        'VALUES (?, ?, ?, ?, 1)', session['userId'], gid, session['question'], int(time.time()))

                    opt_ids = []
                    for opt in session['options']:
                        opt_ids.append(database.insert_auto_inc(
                            'INSERT INTO survey_options (survey_id, option_text) '
                            'VALUES (?, ?)', sid, opt))

                    bot.send_message(gid, session['userName'] + " has created a new survey: " + session['question'],
                                     reply_markup=self.display_survey_to_group(session, opt_ids))
                    return

                data = self.callback_dict[query_data]
                if 'discard' in data:
                    raise SessionDiscard()
                elif 'preview' in data:
                    bot.send_message(
                        chat_id=chat_id,
                        text="Question: {}\nOptions:\n{}".format(
                            session['question'], format_opts(session['options'])), parse_mode=ParseMode.HTML)
                else:
                    session.update(data)

                self.prompt(session, bot, chat_id)
            finally:
                bot.answerCallbackQuery(update.callback_query.id)

    def create(self):
        pass

    def create_send_choice_keyboard(self, session, res_set):
        buttons_list = []

        for name, gid in res_set:
            buttons_list.append([
                InlineKeyboardButton(text=name, callback_data='send_' + str(gid))
            ])

        return InlineKeyboardMarkup(buttons_list)

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

        if session['question'] and session['options_completed']:
            buttons_list.append(
                InlineKeyboardButton(text='Send', callback_data='send')
            )

        return InlineKeyboardMarkup([buttons_list])

    def display_survey_to_group(self, session, opt_ids):
        buttons_list = []

        for i, opt in enumerate(session['options']):
            buttons_list.append([
                InlineKeyboardButton(text=opt, callback_data='m[{}]opt_ans_{}'.format(self.bot_module_name, opt_ids[i]))
            ])

        return InlineKeyboardMarkup(buttons_list)
