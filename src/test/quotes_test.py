import sqlite3
from main import minimigrate
from quotes import Quotes

connection = sqlite3.connect(":memory:")
minimigrate(connection)


def test_add():
    q = Quotes(':memory:', connection)
    q.add("test_id", "author", "text")
    c = connection.cursor()
    c.execute(
        'SELECT * from quotes WHERE chat_id=? and author = ? and quote = ?',
        ('test_id', 'author', 'text')
              )
    assert c.fetchone() is not None
    return "Quotes adding works"


def test_random():
    q = Quotes(':memory:', connection)
    q.add('a', 'b', 'c')
    assert q.random('a') is not None


def test_search():
    q = Quotes(':memory:', connection)
    q.add('test', 'antani', 'cacca')
    assert q.search('test', 'cacca')[0][1] == 'antani'
