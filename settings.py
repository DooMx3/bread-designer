import json


class File:
    PATH = r"settings.json"

    def __init__(self):
        self.file = open(self.PATH)
        self.attributes = json.load(self.file)
        print(self.attributes)

    def __getitem__(self, item):
        return self.attributes[item]

