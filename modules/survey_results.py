from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

import database
from modules.base_module import BaseModule


class SurveyResultsModule(BaseModule):
    bot_module_name = 'results'
    name = 'Survey Results'

    def __init__(self):
        BaseModule.__init__(self)

    def handle_command(self, bot, update):
        chat_id = update.effective_chat.id
        res_set = database.query_r('SELECT s.survey_id, s.group_id, s.survey_question, us.group_name '
                                   '  FROM surveys s, user_groups us '
                                   ' WHERE s.group_id = us.group_id '
                                   '   AND us.user_id = ?', update.effective_user.id)

        if res_set:
            bot.send_message(chat_id=chat_id, text="What survey to display?", parse_mode=ParseMode.HTML,
                             reply_markup=self.get_surveys_markup(res_set))
        else:
            bot.send_message(chat_id=chat_id, text="No surveys found")

    def handle_message(self, session, bot, update):
        pass

    def handle_async_callback(self, bot, update, query):
        if update.callback_query and query and query.startswith('+'):
            answered = False
            try:
                uid = update.effective_user.id
                gid = update.effective_chat.id
                survey_id = int(query.split('+')[1])
                answers = database.query_r(
                    'SELECT so.option_text, u.user_name '
                    'FROM survey_answers a, users u, survey_options so '
                    'WHERE u.user_id = a.user_id '
                    '  AND so.option_id = a.option_id '
                    '  AND a.survey_id = ?', survey_id)

                summary = {}
                for option, user in answers:
                    if option not in summary:
                        summary[option] = 0
                    summary[option] += 1

                msg = "For this survey, the following votes were recorded: \n"
                for option, user in answers:
                    msg += "{} voted for {}\n".format(user, option)

                msg += "In summary, the votes total to:\n"
                for i, option in enumerate(summary):
                    msg += "{} votes for {}\n".format(summary[option], option)

                bot.send_message(chat_id=gid, text=msg)
            finally:
                if not answered:
                    bot.answerCallbackQuery(update.callback_query.id)

    def handle_callback(self, session, bot, update):
        if update.callback_query:
            try:
                chat_id = update.effective_chat.id
                query_data = update.callback_query.data
            finally:
                bot.answerCallbackQuery(update.callback_query.id)

    def create(self):
        database.query_w(
            "CREATE TABLE IF NOT EXISTS surveys(survey_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "user_id INTEGER, group_id INTEGER, survey_question VARCHAR, created INTEGER, valid TINYINT)")

        database.query_w("CREATE INDEX IF NOT EXISTS surveys_user_id_index on surveys (user_id)")

        database.query_w(
            "CREATE TABLE IF NOT EXISTS survey_options(option_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "survey_id INTEGER, option_text VARCHAR)")

        database.query_w("CREATE INDEX IF NOT EXISTS survey_options_survey_id_index on survey_options (survey_id)")

        database.query_w("CREATE TABLE IF NOT EXISTS survey_answers(answer_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "option_id INTEGER, survey_id INTEGER, user_id INTEGER)")

        database.query_w("CREATE INDEX IF NOT EXISTS survey_answers_survey_id_index on survey_options (survey_id)")

    def get_surveys_markup(self, res_set):
        buttons_list = []
        for survey_id, group_id, survey_question, group_name in res_set:
            buttons_list.append([
                InlineKeyboardButton(text="'{}' over at '{}'".format(survey_question, group_name),
                                     callback_data='m[{}]+{}'.format(self.bot_module_name, survey_id))
            ])
        return InlineKeyboardMarkup(buttons_list)
