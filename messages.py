from telegram import ParseMode

import database
import keyboards

import html
import time
import constants


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


def process_message(bot, update):
    message = update.message

    if message.reply_to_message:
        chat_id = update.effective_chat.id
        if message.reply_to_message.text == constants.get_survey_question_text:
            survey_question = message.text
            bot.send_message(chat_id=chat_id, text=constants.enter_survey_option, parse_mode=ParseMode.HTML,
                             reply_markup=keyboards.force_reply())
        elif message.reply_to_message.text == constants.enter_survey_option:
            survey_option = message.text
            if survey_option.lower() not in ['!', 'done']:
                bot.send_message(chat_id=chat_id, text=constants.enter_survey_option, parse_mode=ParseMode.HTML,
                                 reply_markup=keyboards.force_reply())

            # elif message.voice:
            #     media = message.voice.file_id
            #     duration = message.voice.duration
            #     caption = message.caption
            #     message.reply_voice(voice=media, duration=duration, caption=caption)
            #
            # elif message.photo:
            #     media = message.photo[-1].file_id
            #     caption = message.caption
            #     message.reply_photo(photo=media, caption=caption)
            #
            # elif message.sticker:
            #     media = message.sticker.file_id
            #     message.reply_sticker(sticker=media)
            #
            # elif message.document:
            #     media = message.document.file_id
            #     filename = message.document.file_name
            #     caption = message.caption
            #     message.reply_document(document=media, filename=filename, caption=caption)
            #
            # elif message.audio:
            #     media = message.audio.file_id
            #     duration = message.audio.duration
            #     performer = message.audio.performer
            #     title = message.audio.title
            #     caption = message.caption
            #     message.reply_audio(audio=media, duration=duration, performer=performer, title=title, caption=caption)
            #
            # elif message.video:
            #     media = message.video.file_id
            #     caption = message.caption
            #     duration = message.video.duration
            #     message.reply_video(video=media, duration=duration, caption=caption)
            #
            # elif message.contact:
            #     phone_number = message.contact.phone_number
            #     first_name = message.contact.first_name
            #     last_name = message.contact.last_name
            #     message.reply_contact(phone_number=phone_number, first_name=first_name, last_name=last_name)
            #
            # elif message.venue:
            #     longitude = message.venue.location.longitude
            #     latitude = message.venue.location.latitude
            #     title = message.venue.title
            #     address = message.venue.address
            #     foursquare_id = message.venue.foursquare_id
            #     message.reply_venue(longitude=longitude, latitude=latitude, title=title, address=address, foursquare_id=foursquare_id)
            #
            # elif message.location:
            #     longitude = message.location.longitude
            #     latitude = message.location.latitude
            #     message.reply_location(latitude=latitude, longitude=longitude)
            #
            # elif message.video_note:
            #     media = message.video_note.file_id
            #     length = message.video_note.length
            #     duration = message.video_note.duration
            #     message.reply_video_note(video_note=media, length=length, duration=duration)
            #
            # elif message.game:
            #     text = "Sorry, telegram doesn't allow to echo this message"
            #     message.reply_text(text=text, quote=True)
            #
            # else:
            #     text = "Sorry, this kind of media is not supported yet"
            #     message.reply_text(text=text, quote=True)
