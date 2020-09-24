import sqlite3
import sys
from os.path import isfile
from sqlite3 import connect
from datetime import datetime
from note import Note
import common
from apscheduler.triggers.cron import CronTrigger

#TODO: Proper exception handling

DB_PATH = "./data/db/notebooks.db"
BUILD_PATH = "./data/db/build.sql"

sqlite_connection = None
cursor = None   

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        if sqlite_connection:
            sqlite_connection.commit()

#@with_commit
def build():         
    if isfile(BUILD_PATH) and not isfile(DB_PATH):
        scriptexec(BUILD_PATH)

def commit():
    if sqlite_connection:
        sqlite_connection.commit()

def autosave(scheduler):
    scheduler.add_job(commit, CronTrigger(second=0))

def field(command, *values):
    cursor.execute(command, tuple(*values))
    if (fetch := cursor.fetchone()) is not None:
        return fetch[0]

def record(command, *values):
    cursor.execute(command, tuple(*values))
    return cursor.fetchone()

def records(command, *values):
    cursor.execute(command, tuple(*values))
    return cursor.fetchall()

def column(command, *values):
    cursor.execute(command, tuple(*values))
    return [item[0] for item in cursor.fetchall()]

def execute(command, *values):
    cursor.execute(command, tuple(*values))

def execmany(command, valueSet):
    cursor.executemany(command, valueSet)

@with_commit
def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cursor.executescript(script.read())

def open_cursor():
    sqlite_connection = connect(
        DB_PATH, 
        check_same_thread=False, 
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    sqlite_connection.row_factory = sqlite3.Row
    cursor = sqlite_connection.cursor()
    return cursor.connection, cursor

def close_cursor(cursor):
    cursor.close()
    if (cursor.connection):
        cursor.connection.close()

def insert_note(userId, text, notebook=None):   
    '''
    Insert a note into a named notebook or the default notebook
    ''' 
    if notebook is None:
        notebook = common.DEFAULT_NOTEBOOK
    insert_sql = """INSERT INTO 'notes' 
                    ('Time', 'UserId', 'Notebook', 'Text') 
                    VALUES(?, ?, ?, ?);"""
    values = (datetime.now(), userId, notebook.strip().lower(), text)
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
    '''
    Gets all notes in a named notebook or the default notebook
    ''' 
    if notebook is None:
        notebook = common.DEFAULT_NOTEBOOK
    select_sql = """SELECT Id, Time, Text 
                    FROM notes
                    WHERE UserId = ?
                    and Notebook = ?;"""
    values = (userId, notebook.strip().lower())
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
    '''
    Deletes a note by Id from whatever notebook is in
    ''' 
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

def set_prefixes(guildId, guildName, userId, prefixList):
    """
    Sets the command prefixes for a given guild
    """
    upsert_sql = """INSERT INTO guild_config(guildId, name, setAt, setBy, commandPrefixes)
                        VALUES(?, ?, ?, ?, ?)
                        ON CONFLICT(guildId) DO UPDATE SET commandPrefixes = excluded.commandPrefixes;"""
    setAt = datetime.datetime.now()
    prefString = common.CSV_SEPARATOR.join(prefixList)
    values = (guildId, guildName, setAt, userId, prefString)
    cursor = None
    try:
        conn, cursor = open_cursor()
        cursor.execute(upsert_sql, values)
        conn.commit()
    except Exception as ex:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor)

def get_prefixes(guildId):
    """
    Gets the command prefixes for a given guild
    """
    select_sql = """SELECT commandPrefixes 
                    FROM guild_config
                    WHERE guildId = ?;"""
    values = (guildId,)
    cursor = None
    try:
        conn, cursor = open_cursor()
        rows = cursor.fetchone()
        if rows is None:
            return None
        else:
            prefString = rows["commandPrefixes"]
            prefList = prefString.split(common.CSV_SEPARATOR)
            return prefList
    except Exception as ex:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor)

def get_books(userId):
    """
    List all notebooks for a given member
    """
    select_sql = """SELECT count(*) Num, Notebook 
                    FROM notes
                    WHERE UserId = ?
                    GROUP BY Notebook"""
    values = (userId, )
    cursor = None
    try:
        conn, cursor = open_cursor()
        cursor.execute(select_sql, values)
        rows = cursor.fetchall()
        books = []
        for row in rows:
            books.append((row["num"], row["notebook"]))
        return books
    except Exception as e:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor)        

def del_book(userId, notebook):
    """
    Deletes a notebook.
    """
    count_sql = """SELECT count(*) Count
                    FROM notes
                    WHERE Notebook = ? 
                        and UserId = ?"""
    delete_sql = """DELETE 
                    FROM notes
                    WHERE Notebook = ? 
                        and UserId = ?"""
    values = (notebook.strip().lower(), userId)
    cursor = None
    try:
        conn, cursor = open_cursor()
        cursor.execute(count_sql, values)
        row = cursor.fetchone()
        count = row["Count"]
        if count > 0:
            cursor.execute(delete_sql, values)
        return count
    except Exception as e:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor) 