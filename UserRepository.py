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

def add_dog(dog):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    arguments = (dog.name, dog.human_id)

    sql = """
    INSERT INTO dogs (name, human_id)
    VALUES (?, ?)
    """

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        conn.close()
        return "Dog created successfully"
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

def get_all():
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "SELECT * FROM users"

    if (query.execute(sql)):
        rows = query.fetchall()
        users = []
        for row in rows:
            user = User(row[0], row[1], row[2])
            users.append(user)
        query.close()
        conn.commit()
        conn.close()
        return users

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

def modify_by_id(id, age):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    user = get_by_id(id)
    if not user:
        return None

    sql = "UPDATE users SET age = ? WHERE id = ?"

    arguments = (age, id)

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        user_modified = get_by_id(id)
        conn.close()
        return user_modified
