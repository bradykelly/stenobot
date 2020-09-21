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

def set_prefix(prefix):
    """
    Sets the global command prefix
    """
    update_sql = """UPDATE config
                        SET command_prefix = "
                        WHERE Id = 1"""
    values = (prefix)
    cursor = None
    try:
        conn, cursor = open_cursor()
        cursor.execute(update_sql, values)
        conn.commit()
    except Exception as ex:
        err = sys.exc_info()[0]
    finally:
        close_cursor(cursor)

def get_books(userId):
    """
    List all notebooks for a given user
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

    def del_notebook(userId, notebook):
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
                ret = cursor.execute(delete_sql, values)
            return count
        except Exception as e:
            err = sys.exc_info()[0]
        finally:
            close_cursor(cursor)  