import datetime
import random
import json
import os

from saya import Uploader

from basefile import BaseFile
from vkm import MethodsVK


def check_time(vk):
    while True:
        try:
            files = [i for i in list(os.walk('data'))[1][2]]
        except IndexError:
            continue
        for file in files:
            file = int(file.replace('.json', ''))
            if file > 2000000000:
                chat = file
                continue
            try:
                base = BaseFile(chat, file)
                data = base.load()
            except:
                print(21)
            time = datetime.datetime.fromisoformat(str(datetime.datetime.now())).timestamp()

            if 'time' in data:
                if data['time'] <= time:
                    vkm = MethodsVK(vk, chat)
                    vkm.kick_user(file)
                    os.remove(f'data/{chat}/{file}.json')


class Captcha:
    def __init__(self, message, vk):
        self.msg = message
        if message is not None:
            self.from_id = message['action']['member_id']
            self.peer_id = message['peer_id']
            self.date = message['date']
            self.vk = vk

    def load_captcha(self):
        if os.path.exists('captcha/captcha-image/data.json'):
            with open('captcha/captcha-image/data.json', 'r') as data:
                return json.load(data)

    def send_captcha(self):
        base = BaseFile(peer_id=self.peer_id, name=self.from_id)
        chat_data = BaseFile(peer_id=self.peer_id).load()
        data = base.load()
        data['time'] = self.date + chat_data['time_until_kick'] * 60
        data['is_captcha'] = True
        data['retr'] = chat_data['try_number']
        captcha_data = self.load_captcha()['captcha']
        captcha = random.choice(captcha_data)
        resp = self.vk.uploader.message_photo(captcha['photo'], peer_id=self.peer_id)
        file = Uploader.format(resp, 'photo')
        data['ans'] = captcha['ans']
        text = f"""
Anti Spam Bot Protection!
 
Введите код с картинки, приложенной снизу, для подтверждения того что вы не бот, иначе вы будете исключены
Установленное время до авто-кика: {chat_data['time_until_kick']} минут(ы)
        """
        self.vk.messages.send(message=text, attachment=file, peer_id=self.peer_id,
                              random_id=random.randint(1, 1093984730912))
        base.upload(data)
