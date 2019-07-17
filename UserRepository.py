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

def get_by(id):
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

def remove(id):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()
    user = get_by(id)
    if not user:
        return None

    sql = "DELETE FROM users WHERE id = %s" % id

    if (query.execute(sql)):
        query.close()
        conn.commit()
        conn.close()
        return "user deleted"

def modify(id, age):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    user = get_by(id)
    if not user:
        return None

    sql = "UPDATE users SET age = ? WHERE id = ?"

    arguments = (age, id)

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        user_modified = get_by(id)
        conn.close()
        return user_modified

def get_user_dog_relation(user):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = """SELECT users.id, users.name, dogs.id, dogs.name
    FROM users
    JOIN dogs
    ON users.id=dogs.human_id
    WHERE users.id= %s""" % user.id

    if (query.execute(sql)):
        row = query.fetchall()
        if not row:
            return None
        query.close()
        conn.commit()
        conn.close()
        return row
