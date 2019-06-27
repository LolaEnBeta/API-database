
class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_json(self, user):
        return {"id": user[0], "name": self.name, "age": self.age}
