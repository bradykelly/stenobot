import sqlite3
import sys
from sqlite3.dbapi2 import Cursor
from datetime import datetime

DEFAULT_NOTEBOOK = "Main"

sqlite_connection = None
cursor = None   

def open_cursor():
    sqlite_connection = sqlite3.connect("notebooks.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = sqlite_connection.cursor()
    return cursor.connection, cursor

def close_cursor(cursor):
    cursor.close()
    if (cursor.connection):
        cursor.connection.close()

def insert_note(userId, text, notebook=None):
    if notebook is None:
        notebook = DEFAULT_NOTEBOOK
    insert_sql = """INSERT INTO 'notes' 
                    ('Time', 'UserId', 'Notebook', 'Text') 
                    VALUES(?, ?, ?, ?);"""
    values = (datetime.now(), userId, notebook.lower(), text)
    cursor = None
    try:
        conn, cursor = open_cursor()
        cursor.execute(insert_sql, values)
        conn.commit()
    except:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor)

