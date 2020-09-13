import sqlite3
import sys
from datetime import datetime
from note import Note
import common

#TODO: Proper exception handling

sqlite_connection = None
cursor = None   

def open_cursor():
    sqlite_connection = sqlite3.connect("notebooks.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    sqlite_connection.row_factory = sqlite3.Row
    cursor = sqlite_connection.cursor()
    return cursor.connection, cursor

def close_cursor(cursor):
    cursor.close()
    if (cursor.connection):
        cursor.connection.close()

def insert_note(userId, text, notebook=None):    
    if notebook is None:
        notebook = common.DEFAULT_NOTEBOOK
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

def get_notes(userId, notebook=None):
    if notebook is None:
        notebook = common.DEFAULT_NOTEBOOK
    select_sql = """SELECT Id, Time, Text 
                    FROM notes
                    WHERE UserId = ?
                    and Notebook = ?;"""
    values = (userId, notebook.lower())
    cursor = None
    try:
        conn, cursor = open_cursor()
        cursor.execute(select_sql, values)
        rows = cursor.fetchall()
        notes = []
        for row in rows:
            note = Note(row["id"], row["time"], row["text"])
            notes.append(note)
        return notes
    except:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor)

def delete_note(userId, noteId):
    del_sql = """DELETE 
                    FROM notes 
                    WHERE UserId = ?
                        AND Id = ?"""
    values = (userId, noteId)
    cursor = None
    try:
        conn, cursor = open_cursor()
        cursor.execute(del_sql, values)
        conn.commit()
    except Exception as ex:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor)

