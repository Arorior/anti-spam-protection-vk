import os
import json


class BaseFile:
    def __init__(self, name):
        self.name = name

    def create(self):
        if not self.is_exists():
            data = {}
            with open(f'data/{self.name}.json', 'x') as base:
                json.dump(data, base)

    def is_exists(self):
        if os.path.exists(f'data/{self.name}.json'):
            return True

    def load(self):
        if not self.is_exists():
            self.create()
        with open(f'data/{self.name}.json', 'x') as base:
            return json.load(base)

    def upload(self, data):
        if not self.is_exists():
            self.create()
        with open(f'data/{self.name}.json', 'x') as base:
            json.dump(data, base)
