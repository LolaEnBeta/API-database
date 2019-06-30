
class User(object):
    def __init__(self, name, age, id=None):
        self.name = name
        self.age = age
        self.id = id

    def to_json(self, user):
        return {"id": user[0], "name": self.name, "age": self.age}

    def to_json_2(self):
        return {"id": self.id, "name": self.name, "age": self.age}