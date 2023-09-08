#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3
import datetime


def update_user_consent(user_id, consent):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        'UPDATE user_preferences SET consent=?, consent_date=? WHERE user_id=?',
        (consent, current_date, user_id))

    conn.commit()
    conn.close()
    
    
def create_table():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_preferences (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT,
        voice TEXT,
        consent TEXT,
        consent_date TEXT,
        counter INTEGER
    )
    ''')

    conn.commit()
    conn.close()

    
# Call the function to create the table.
create_table()


def add_columns_if_not_exist():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    # Check if 'consent' column exists
    cursor.execute("PRAGMA table_info(user_preferences)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'consent' not in columns:
        cursor.execute('ALTER TABLE user_preferences ADD COLUMN consent TEXT')

    if 'consent_date' not in columns:
        cursor.execute(
            'ALTER TABLE user_preferences ADD COLUMN consent_date TEXT')

    conn.commit()
    conn.close()


add_columns_if_not_exist()


def get_db_connection():
    conn = sqlite3.connect('bot_data.db',
                           timeout=5)  # Increase timeout to 30 seconds
    return conn


def update_user_counter(user_id, counter):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE user_preferences SET counter=? WHERE user_id=?',
                   (counter, user_id))

    conn.commit()
    conn.close()
    
    
def user_exists(user_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM user_preferences WHERE user_id = ?',
                   (user_id, ))
    result = cursor.fetchone()
    conn.close()

    return result is not None



def insert_user_data(user_id, user_name, chat_id):

    if user_exists(user_id):
        #         bot.send_message(chat_id, f"User with ID: {user_id} already exists!")
        return

    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    # Inserting the user_id and user_name without voice_preference for now.
    cursor.execute(
        'INSERT OR IGNORE INTO user_preferences (user_id, user_name) VALUES (?, ?)',
        (user_id, user_name))

    # Now, we'll send back the user_id and user_name to the given chat_id to verify.
    #     bot.send_message(chat_id, f"Saved user_id: {user_id}, user_name: {user_name}")

    conn.commit()
    conn.close()

    
    

def update_user_voice(user_id, voice):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE user_preferences SET voice=? WHERE user_id=?',
                   (voice, user_id))

    conn.commit()
    conn.close()


def get_user_voice(user_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT voice FROM user_preferences WHERE user_id = ?',
                   (user_id, ))
    voice = cursor.fetchone()
    conn.close()

    return voice[0] if voice else None


def get_user_counter(user_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT counter FROM user_preferences WHERE user_id = ?',
                   (user_id, ))
    voice = cursor.fetchone()
    conn.close()

    return voice[0] if voice else None

