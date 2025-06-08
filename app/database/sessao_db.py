import sqlite3

async def get_db():
    connection = sqlite3.connect('bancosqlite.db')
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        connection.close()
