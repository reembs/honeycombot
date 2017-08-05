from config import configfile

from telegram import Bot

GET_ME = Bot(configfile.bot_token).getMe()

start_survey_text = 'Start a survey'
get_survey_question_text = 'Enter a survey question'
enter_survey_option = 'Enter a survey answer, type "done" or "!" to finish'
