import random
import json
import os

from saya import Uploader


class Captcha:
    def __init__(self, from_id, vk):
        self.from_id = from_id
        self.vk = vk

    def load_captcha(self):
        if os.path.exists('captcha/captcha-image/data.json'):
            with open('captcha/captcha-image/data.json', 'r') as data:
                return json.load(data)

    def send_captcha(self):
        captcha_data = self.load_captcha()['captcha']
        captcha = random.choice(captcha_data)
        resp = self.vk.uploader.message_photo(captcha['photo'], peer_id=self.from_id)
        file = Uploader.format(resp, 'photo')

        self.vk.messages.send(attachment=file, peer_id=self.from_id,
                              random_id=12234567)
