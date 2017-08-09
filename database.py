import sqlite3

from config import configfile


def connect():
    conn = sqlite3.connect(configfile.db_name)
    c = conn.cursor()
    return (conn, c)


def query_w(query, *params):
    conn, c = connect()
    c.execute(query, params)
    conn.commit()
    conn.close()


def insert_auto_inc(query, *params):
    conn, c = connect()
    try:
        c.execute(query, params)
        conn.commit()
        return c.lastrowid
    finally:
        conn.close()


def query_r(query, *params, one=False):
    conn, c = connect()
    c.execute(query, params)
    try:
        if not one:
            return c.fetchall()
        else:
            return c.fetchone()
    finally:
        conn.close()


def create_db():
    query = "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, user_name VARCHAR, last_activity INTEGER)"
    query_w(query)
    query = "CREATE TABLE IF NOT EXISTS user_groups(user_id INTEGER PRIMARY KEY, group_id INTEGER, group_name VARCHAR, joined INTEGER)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS user_groups_index on user_groups (user_id, group_id)"
    query_w(query)
    query = "CREATE TABLE IF NOT EXISTS surveys(survey_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, group_id INTEGER, survey_question VARCHAR, created INTEGER, valid TINYINT)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS surveys_user_id_index on surveys (user_id)"
    query_w(query)
    query = "CREATE TABLE IF NOT EXISTS survey_options(option_id INTEGER PRIMARY KEY AUTOINCREMENT, survey_id INTEGER, option_text VARCHAR)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS survey_options_survey_id_index on survey_options (survey_id)"
    query_w(query)
    query = "CREATE TABLE IF NOT EXISTS survey_answers(answer_id INTEGER PRIMARY KEY AUTOINCREMENT, option_id INTEGER, survey_id INTEGER, user_id INTEGER)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS survey_answers_survey_id_index on survey_options (survey_id)"
    query_w(query)


def add_user_group(user_id, group_id, group_name, joined_time):
    query = "UPDATE OR IGNORE user_groups SET group_name = ? WHERE user_id = ? AND group_id = ?"
    query_w(query, group_name, user_id, group_id)
    query = "INSERT OR IGNORE INTO user_groups(user_id,group_id,group_name,joined) VALUES (?, ?, ?, ?)"
    query_w(query, user_id, group_id, group_name, joined_time)


def add_user_db(user_id, username, time):
    # try to update or ignore
    query = "UPDATE OR IGNORE users SET last_activity = ?, user_name = ? WHERE user_id = ?"
    query_w(query, time, username, user_id)
    # try to add or ignore
    query = "INSERT OR IGNORE INTO users(user_id, last_activity) VALUES (?, ?)"
    query_w(query, user_id, time)

# create the database
create_db()
