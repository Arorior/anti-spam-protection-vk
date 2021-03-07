import os
import json


class BaseFile:
    def __init__(self, peer_id, name=None):
        self.peer_id = peer_id
        self.name = name

    def create_chat(self):
        data = {'need_captcha': False, }
        with open(f'data/{self.peer_id}/{self.peer_id}.json', 'x') as base:
            json.dump(data, base)

    def create(self):
        if not self.is_exists():
            data = {'is_captcha': True, }
            with open(f'data/{self.peer_id}/{self.name}.json', 'x') as base:
                json.dump(data, base)

    def is_exists(self):
        if os.path.exists(f'data/{self.peer_id}/{self.name}.json'):
            return True

    def load(self):
        if not self.is_exists():
            self.create()
        if self.name is not None:
            name = self.name
        else:
            name = self.peer_id
        with open(f'data/{self.peer_id}/{name}.json', 'x') as base:
            return json.load(base)

    def upload(self, data):
        if not self.is_exists():
            self.create()
        if self.name is not None:
            name = self.name
        else:
            name = self.peer_id
        with open(f'data/{self.peer_id}/{name}.json', 'x') as base:
            json.dump(data, base)
