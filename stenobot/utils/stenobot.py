import common
import sys
from datetime import datetime
from discord.ext import commands
from stenobot.models.note import Note

class Stenobot():
    def __init__(self, bot):
        self.bot = bot

    async def get_open_book(self, guildId, userId):
        try:
            book = await self.bot.db.field("SELECT open_notebook FROM members WHERE guildId = ? and userId = ?", guildId, userId)
            return book
        except Exception as ex:
            print("Stenobot class: " + str(sys.exc_info()[0]))
            raise            
    
    async def set_open_book(self, guildId, userId, name):
        book = await self.get_open_book(guildId, userId)
        try:
            if (book is not None):
                await self.bot.db.execute("UPDATE members SET open_notebook = ? WHERE guildId = ? and userId = ?", name, guildId, userId)
            else:
                await self.bot.db.execute("INSERT INTO members (guildId, userId, open_notebook) VALUES (?, ?, ?)", guildId, userId, name)
            await self.bot.db.commit()
            # Insert a dummy record for this notebook name so that get_books includes the active notebook even if it is empty
            notes, notebook = await self.get_notes(guildId, userId, name)
            if len(notes) == 0:
                await self.insert_note(guildId, self.bot.user.id, F"{name} - empty note", name)
                await self.bot.db.commit()
        except Exception as ex:
            print("Stenobot class: " + str(sys.exc_info()[0]))
            raise

    async def insert_note(self, guildId, userId, text, notebook=None):  
        try:
            if notebook is None:
                if (notebook := await self.get_open_book(guildId, userId)) is None:
                    notebook = common.DEFAULT_NOTEBOOK
            insert_sql = "INSERT INTO 'notes' ('Time', 'UserId', 'Notebook', 'Text') VALUES(?, ?, ?, ?);"
            count = await self.bot.db.execute(insert_sql, datetime.now(), userId, notebook.strip().lower(), text)
            await self.bot.db.commit()
            return count
        except Exception as ex:
            print("Stenobot class: " + str(sys.exc_info()[0]))
            raise    

    async def get_notes(self, guildId, userId, notebook=None):
        try:
            if notebook is None:
                if (notebook := await self.get_open_book(guildId, userId)) is None:
                    notebook = common.DEFAULT_NOTEBOOK
            select_sql = "SELECT NoteId, Time, Text FROM notes WHERE UserId = ? and Notebook = ?;"
            rows = await self.bot.db.records(select_sql, userId, notebook.strip().lower())
            notes = []
            for row in rows:
                notes.append(Note(row[0], row[1], row[2]))
            return notes, notebook
        except Exception as ex:
            print("Stenobot class: " + str(sys.exc_info()[0]))
            raise 
        
    async def delete_note(self, userId, noteId):
        del_sql = "DELETE FROM notes WHERE UserId = ? AND NoteId = ?"
        try:
            await self.bot.db.execute(del_sql, userId, noteId)
            await self.bot.db.commit()
        except Exception as ex:
            print("Stenobot class: " + str(sys.exc_info()[0]))
            raise   

    async def get_books(self, userId):
        # Also need notes with the bot's user id to include dummy notes just for book names.
        select_sql = "SELECT count(*) Num, Notebook FROM notes WHERE UserId = ? OR UserId = ? GROUP BY Notebook"
        try:
            rows = await self.bot.db.records(select_sql, userId, self.bot.user.id)
            books = []
            for row in rows:
                books.append((row[0], row[1]))
            return books
        except Exception as ex:
            print("Stenobot class: " + str(sys.exc_info()[0]))
            raise           

    async def del_book(self, userId, notebook):
        count_sql = "SELECT count(*) Count FROM notes WHERE Notebook = ? and UserId = ?"
        delete_sql = "DELETE FROM notes WHERE Notebook = ? and UserId = ?"
        values = (notebook.strip().lower(), userId)
        try:
            row = await self.bot.db.execute(count_sql, values)
            count = row[0] if row is not None else 0
            if count > 0:
                await self.bot.db.execute(delete_sql, values)
                await self.bot.db.commit()
            return count
        except Exception as ex:
            print("Stenobot class: " + str(sys.exc_info()[0]))
            raise    