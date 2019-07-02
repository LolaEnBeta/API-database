import sqlite3

conn = sqlite3.connect("sqlite3/database.db")

query = conn.cursor()

sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)"""

if (query.execute(sql)):
    print("Table created successfully")
else:
    print("An error has ocurred")

query.close()

conn.commit()

conn.close()
