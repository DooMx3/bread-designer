import json


class File:
    PATH = r"C:\Users\Adrian\PycharmProjects\breadboardCreator\bread_designer\settings.json"

    def __init__(self):
        self.file = open(self.PATH)
        self.attributes = json.load(self.file)
        print(self.attributes)

