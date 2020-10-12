# From Solaris: https://github.com/parafoxia/Solaris
# TODO Exception handling

from chatnotebot.models.note import Note
import sys
import common
from os import path
from aiosqlite import connect
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime


class Database:
    def __init__(self, bot):
        self.bot = bot
        self.db_path = f"{self.bot._dynamic}/notebooks.db"
        self.build_path = f"{self.bot._static}/build.sql"
        self._calls = 0

        self.bot.scheduler.add_job(self.commit, CronTrigger(second=0))

    async def connect(self):
        if not path.isdir(self.bot._dynamic):
            # If this directory does not exist, we need to create it.
            from os import makedirs

            makedirs(self.bot._dynamic)

        self.cxn = await connect(self.db_path)
        await self.execute("pragma journal_mode=wal")
        await self.executescript(self.build_path)
        await self.commit()

    async def commit(self):
        if self.bot.ready.ok:
            await self.execute("UPDATE bot SET Value = CURRENT_TIMESTAMP WHERE Key = 'last commit'")

        await self.cxn.commit()

    async def close(self):
        await self.commit()
        await self.cxn.close()

    async def sync(self):
        # Insert.
        await self.executemany("INSERT OR IGNORE INTO guild_config (GuildID) VALUES (?)", [(g.id,) for g in self.bot.guilds])
        await self.executemany(
            "INSERT OR IGNORE INTO gateway (GuildID) VALUES (?)", [(g.id,) for g in self.bot.guilds]
        )
        await self.executemany("INSERT OR IGNORE INTO warn (GuildID) VALUES (?)", [(g.id,) for g in self.bot.guilds])

        # Remove.
        stored = await self.column("SELECT GuildID FROM guild_config")
        member_of = [g.id for g in self.bot.guilds]
        removals = [(g_id,) for g_id in set(stored) - set(member_of)]
        await self.executemany("DELETE FROM guild_config WHERE GuildID = ?", removals)
        await self.executemany("DELETE FROM gateway WHERE GuildID = ?", removals)
        await self.executemany("DELETE FROM warn WHERE GuildID = ?", removals)

        # Commit.
        await self.commit()

    async def field(self, sql, *values):
        cur = await self.cxn.execute(sql, tuple(values))
        self._calls += 1

        if (row := await cur.fetchone()) is not None:
            return row[0]

    async def record(self, sql, *values):
        cur = await self.cxn.execute(sql, tuple(values))
        self._calls += 1

        return await cur.fetchone()

    async def records(self, sql, *values):
        cur = await self.cxn.execute(sql, tuple(values))
        self._calls += 1

        return await cur.fetchall()

    async def column(self, sql, *values):
        cur = await self.cxn.execute(sql, tuple(values))
        self._calls += 1

        return [row[0] for row in await cur.fetchall()]

    async def execute(self, sql, *values):
        cur = await self.cxn.execute(sql, tuple(values))
        self._calls += 1

        return cur.rowcount

    async def executemany(self, sql, valueset):
        cur = await self.cxn.executemany(sql, valueset)
        self._calls += 1  # NOTE: Should this be `len(valueset)`?

        return cur.rowcount

    async def executescript(self, path):
        with open(path, "r", encoding="utf-8") as script:
            await self.cxn.executescript(script.read())
        self._calls += 1  # NOTE: Should this be different?

    async def insert_note(self, userId, text, notebook=None):   
        '''
        Insert a note into a named notebook or the default notebook
        ''' 
        if notebook is None:
            notebook = common.DEFAULT_NOTEBOOK
        insert_sql = """INSERT INTO 'notes' 
                        ('Time', 'UserId', 'Notebook', 'Text') 
                        VALUES(?, ?, ?, ?);"""
        values = (datetime.now(), userId, notebook.strip().lower(), text)
        cur = None
        try:
            cur = await self.cxn.execute(insert_sql, values)
        except:
            err = sys.exc_info()[0]
        else:
            self._calls += 1      

        return cur.rowcount

    async def get_notes(self, userId, notebook=None):
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
        try:
            cur = await self.cxn.execute(select_sql, values)
            rows = await cur.fetchall()
            notes = []
            for row in rows:
                note = Note(row[0], row[1], row[2])
                notes.append(note)
            return notes
        except Exception as ex:
            err = sys.exc_info()[0]

    async def delete_note(self, userId, noteId):
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
            await self.ctx.execute(del_sql, values)
        except Exception as ex:
            err = sys.exc_info()[0]

    async def get_books(self, userId):
        """
        List all notebooks for a given member
        """
        select_sql = """SELECT count(*) Num, Notebook 
                        FROM notes
                        WHERE UserId = ?
                        GROUP BY Notebook"""
        values = (userId, )
        try:
            cur = await self.cxn.execute(select_sql, values)
            rows = await cur.fetchall()
            books = []
            for row in rows:
                books.append((row[0], row[1]))
            return books
        except Exception as ex:
            err = sys.exc_info()[0]
       
    def del_book(self, userId, notebook):
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
            self.cxn.execute(count_sql, values)
            row = cursor.fetchone()
            count = row["Count"]
            if count > 0:
                self.cxn.execute(delete_sql, values)
            return count
        except Exception as e:
            err = sys.exc_info()[0]       
