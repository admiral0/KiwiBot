import sqlite3
import logging

logger = logging.getLogger(__name__)

class Quotes:

    def __init__(self, connstr, conn=None):
        """
        :param sqlite3.Connection conn:
        """
        self.connstring = connstr
        self.conn = conn

    def refresh_connection(self):
        logger.debug('Refreshing connection to database {}'.format(self.connstring))
        self.conn = sqlite3.connect(self.connstring)

    def add(self, chat_id, author, quote):
        logger.debug('Adding a quote "{}" by {} in chat {}'.format(quote, author, chat_id))
        c = self.conn.cursor()
        c.execute("INSERT INTO quotes VALUES (?,?,?);", (chat_id, author, quote))
        rowid = c.lastrowid
        logger.debug('Adding to index - rowid = {}'.format(rowid))
        c.execute('INSERT INTO quotes_index VALUES(?,?,?,?)', (rowid, chat_id, author, quote))
        self.conn.commit()

    def random(self, chat_id):
        c = self.conn.cursor()
        logger.debug('Getting a random quote for chat {}'.format(chat_id))
        c = c.execute("SELECT * FROM quotes WHERE chat_id = ? ORDER BY RANDOM() LIMIT 1;", (chat_id,))
        return c.fetchone()

    def search(self, chat_id, search):
        c = self.conn.cursor()
        logger.debug('Searching quotes in chat {} for "{}"'.format(chat_id, search))
        c.execute("SELECT * FROM quotes_index WHERE chat_id = ? and quote MATCH ?;", (chat_id, search))
        return c.fetchall()
