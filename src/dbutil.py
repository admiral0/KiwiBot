
def minimigrate(con):
    """
    Stupid migration SQL script. Will create necessary tables
    :param sqlite3.Connection con: Sqlite Connection
    """
    c = con.cursor()
    c.executescript("""
            CREATE TABLE IF NOT exists quotes (chat_id VARCHAR(128), author VARCHAR(128), quote TEXT);
            DROP TABLE IF EXISTS quotes_index;
            CREATE VIRTUAL TABLE quotes_index USING fts4(id, chat_id, author, quote);
            INSERT INTO quotes_index SELECT rowid, chat_id, author, quote FROM quotes;
    """)
    con.commit()
