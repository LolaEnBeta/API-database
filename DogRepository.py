import sqlite3
from dog import Dog

def add(dog):
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

def get_by(id):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "SELECT * FROM dogs WHERE id = %s" % id

    if (query.execute(sql)):
        row = query.fetchone()
        if not row:
            return None

        dog = Dog(row[0], row[1], row[2])

        query.close()
        conn.commit()
        conn.close()
        return dog
    else:
        raise Exception("Some error")

def get_all():
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "SELECT * FROM dogs"

    if (query.execute(sql)):
        rows = query.fetchall()
        dogs_list = [Dog(row[0], row[1], row[2]) for row in rows]
        query.close()
        conn.commit()
        conn.close()
        return dogs_list
    else:
        raise Exception("Some error")

def remove(dog):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "DELETE FROM dogs WHERE id = %s" % dog.id

    if (query.execute(sql)):
        query.close()
        conn.commit()
        conn.close()

def modify(id, name, human_id):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "UPDATE dogs SET name = ?, human_id = ? WHERE id = ?"
    arguments = (name, human_id, id)

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        conn.close()
        dog_modified = get_by(id)
        return dog_modified

def get_dog_user_relation(dog):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = """SELECT dogs.id, dogs.name, users.id, users.name
    FROM dogs
    LEFT JOIN users
    ON dogs.human_id = users.id
    WHERE dogs.id= %s""" % dog.id

    if (query.execute(sql)):
        row = query.fetchall()
        if not row:
            return None
        query.close()
        conn.commit()
        conn.close()
        return row
