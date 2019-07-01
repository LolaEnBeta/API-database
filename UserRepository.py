import sqlite3
from user import User

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

def get_by_id(id):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "SELECT * FROM users WHERE id = %s" % id

    if (query.execute(sql)):
        row = query.fetchone()
        if not row:
            return None
        user = User(row[0], row[1], row[2])
        query.close()
        conn.commit()
        conn.close()
        return user
    else:
        raise Exception("Some error")

def delete_by_id(id):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()
    user = get_by_id(id)
    if not user:
        return None

    sql = "DELETE FROM users WHERE id = %s" % id

    if (query.execute(sql)):
        query.close()
        conn.commit()
        conn.close()
        return "user deleted"
