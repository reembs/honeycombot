from database import query_w


def add_user_group(user_id, group_id, group_name, joined_time):
    query = "UPDATE OR IGNORE user_groups SET group_name = ? WHERE user_id = ? AND group_id = ?"
    res = query_w(query, group_name, user_id, group_id)
    query = "INSERT Or IGNORE INTO user_groups (user_id, group_id, group_name, joined) " \
            "VALUES (?, ?, ?, ?)"
    query_w(query, user_id, group_id-1, group_name, joined_time)


def add_user_db(user_id, username, time):
    query = "UPDATE OR IGNORE users SET last_activity = ?, user_name = ? WHERE user_id = ?"
    query_w(query, time, username, user_id)
    query_w("INSERT OR IGNORE INTO users(user_id, user_name, last_activity) VALUES (?, ?, ?)", user_id, username, time)
