import json


class File:
    PATH = "settings.json"

    def __init__(self):
        self.file = open(self.PATH)
        self.attributes = json.load(self.file)
        print(self.attributes)

