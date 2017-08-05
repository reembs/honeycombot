# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017  Dario dariomsn@hotmail.it

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import time
from config import configfile
import utils


def connect():
    conn = sqlite3.connect("database/" + configfile.db_name)
    c = conn.cursor()
    return (conn, c)


def query_w(query, *params):
    conn, c = connect()
    c.execute(query, params)
    conn.commit()
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
    query = "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, last_activity INTEGER)"
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


def add_survay(user_id, group_id, survey_question):
    pass


def add_user_group(user_id, group_id, group_name, joined_time):
    query = "UPDATE OR IGNORE user_groups SET group_name = ? WHERE user_id = ? AND group_id = ?"
    query_w(query, group_name, user_id, group_id)
    query = "INSERT OR IGNORE INTO user_groups(user_id,group_id,group_name,joined) VALUES (?, ?, ?, ?)"
    query_w(query, user_id, group_id, group_name, joined_time)


def add_user_db(user_id, time):
    # try to update or ignore
    query = "UPDATE OR IGNORE users SET last_activity = ? WHERE user_id = ?"
    query_w(query, time, user_id)
    # try to add or ignore
    query = "INSERT OR IGNORE INTO users(user_id, last_activity) VALUES (?, ?)"
    query_w(query, user_id, time)


def stats_text():
    query = "SELECT count(user_id) FROM users"
    total = query_r(query, one=True)[0]

    interval24h = time.time() - 60 * 60 * 24
    query = "SELECT count(user_id) FROM users WHERE last_activity > ?"
    last24h = query_r(query, interval24h, one=True)[0]

    interval7d = time.time() - 60 * 60 * 24 * 7
    query = "SELECT count(user_id) FROM users WHERE last_activity > ?"
    last7d = query_r(query, interval7d, one=True)[0]

    text = "<b>Total users:</b> {0}\n<b>Last7days:</b> {1}\n<b>Last24h:</b> {2}"
    text = text.format(utils.n_dots(total), utils.n_dots(last7d), utils.n_dots(last24h))
    return text


# create the database
create_db()