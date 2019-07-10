import sqlite3
from dog import Dog

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

def get_dog_by_id(id):
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

def get_all_dogs():
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "SELECT * FROM dogs"

    if (query.execute(sql)):
        rows = query.fetchall()
        dogs_list = []
        for row in rows:
            dog = Dog(row[0], row[1], row[2])
            dogs_list.append(dog)
        query.close()
        conn.commit()
        conn.close()
        return dogs_list
    else:
        raise Exception("Some error")

def remove_dog_by_id(id):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    dog = get_dog_by_id(id)
    if not dog:
        return None

    sql = "DELETE FROM dogs WHERE id = %s" % id

    if (query.execute(sql)):
        query.close()
        conn.commit()
        conn.close()
        return "dog deleted"

def modify_dog_by_id(id, name, human_id):
    conn = sqlite3.connect("sqlite3/database.db")
    query = conn.cursor()

    sql = "UPDATE dogs SET name = ?, human_id = ? WHERE id = ?"
    arguments = (name, human_id, id)

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        conn.close()
        dog_modified = get_dog_by_id(id)
        return dog_modified
