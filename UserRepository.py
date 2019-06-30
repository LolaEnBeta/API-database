import sqlite3

def add(user):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    arguments = (user.name, user.age)

    sql = """
    INSERT INTO users (name, age)
    VALUES (?, ?)
    """

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        conn.close()
        return "User created successfully"
    else:
        return "An error has ocurred"