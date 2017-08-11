import sqlite3

from config import configfile


def connect():
    conn = sqlite3.connect(configfile.db_name)
    c = conn.cursor()
    return (conn, c)


def query_w(query, *params):
    conn, c = connect()
    try:
        return c.execute(query, params)
    finally:
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
    query = "CREATE TABLE IF NOT EXISTS user_groups(" \
            "user_id INTEGER, " \
            "group_id INTEGER, " \
            "group_name VARCHAR, " \
            "joined INTEGER, " \
            "UNIQUE(user_id, group_id) ON CONFLICT REPLACE)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS user_groups_index on user_groups (user_id, group_id)"
    query_w(query)


# create the database
create_db()
