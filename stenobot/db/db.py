# From Solaris: https://github.com/parafoxia/Solaris
# TODO Exception handling

from stenobot.models.note import Note
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

        # Remove.
        stored = await self.column("SELECT GuildID FROM guild_config")
        member_of = [g.id for g in self.bot.guilds]
        removals = [(g_id,) for g_id in set(stored) - set(member_of)]
        await self.executemany("DELETE FROM guild_config WHERE GuildID = ?", removals)

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
            self._calls += 1
            return notes
        except Exception as ex:
            err = sys.exc_info()[0]          

    async def delete_note(self, userId, noteId):
        del_sql = """DELETE 
                        FROM notes 
                        WHERE UserId = ?
                            AND Id = ?"""
        values = (userId, noteId)
        try:
            await self.cxn.execute(del_sql, values)
        except Exception as ex:
            err = sys.exc_info()[0]
        else:
            self._calls += 1            

    async def get_books(self, userId):
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
            self._calls += 1
            return books
        except Exception as ex:
            err = sys.exc_info()[0]

    async def set_current_book(self, guildId, userId, name):
        curBook = await self.record("SELECT currentNotebook FROM members WHERE guildId = ? AND userId = ?", (guildId, userId))
        if (curBook is None):
            await self.execute("INSERT INTO members (guildId, userId, currentNotebook) VALUES (?, ?, ?)", (guildId, userId, name))
        else:
            await self.execute("UPDATE members SET currentNotebook = ? WHERE guildId = ? AND userId = ?", (name, guildId, userId))

    async def get_current_book(self, guildId, userId):
        return await self.record("SELECT currentNotebook from members where guildId = ? and userId = ?", (guildId, userId))
       
    async def del_book(self, userId, notebook):
        count_sql = """SELECT count(*) Count
                        FROM notes
                        WHERE Notebook = ? 
                            and UserId = ?"""
        delete_sql = """DELETE 
                        FROM notes
                        WHERE Notebook = ? 
                            and UserId = ?"""
        values = (notebook.strip().lower(), userId)
        try:
            cur = await self.cxn.execute(count_sql, values)
            row = await cur.fetchone()
            count = row[0]
            if count > 0:
                await self.cxn.execute(delete_sql, values)
            self._calls += 1  
            return count
        except Exception as ex:
            err = sys.exc_info()[0]  
               
