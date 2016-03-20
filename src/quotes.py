import sqlite3


class Quotes:

    def __init__(self, connstr, conn=None):
        self.connstring = connstr
        self.conn = conn

    def refresh_connection(self):
        self.conn = sqlite3.connect(self.connstring)

    def add(self, chat_id, author, quote):
        c = self.conn.cursor()
        c.execute("INSERT INTO quotes VALUES (?,?,?);", (chat_id, author, quote))
        c.commit()

    def random(self, chat_id):
        c = self.conn.cursor()
        c = c.execute("SELECT * FROM quotes WHERE chat_id = ? ORDER BY RANDOM() LIMIT 1;", (chat_id,))
        return c.fetchone()

    def search(self, chat_id, search):
        c = self.conn.cursor()
        search = '%' + search + '%'
        c.execute("SELECT * FROM quotes WHERE chat_id = ? and quote LIKE ?;", (chat_id, search))
        return c.fetchall()
