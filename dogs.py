
class Dogs(object):
    def __init__(self, id, name, human_id):
        self.id = id
        self.name = name
        self.human_id = human_id

    def to_json(self):
        return {"id": self.id, "name": self.name, "human_id": self.human_id}
