import sqlite3

conn = sqlite3.connect("sqlite3/database.db")
query = conn.cursor()

sql = '''CREATE TABLE IF NOT EXISTS human_dog (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    human_id INTEGER NOT NULL,
    dog_id INTEGER NOT NULL
)'''

if (query.execute(sql)):
    print("Table created succesfully")
else:
    print("An error has ocurred")

query.close()
conn.commit()
conn.close()
