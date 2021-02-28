import os
import random
from threading import Thread

import captcha.captcha as cpt
from saya import Vk

from basefile import BaseFile
from captcha.captcha import Captcha
from vkm import MethodsVK

_data = open('.data', 'r').read().split('\n')
TOKEN, GROUP_ID = _data


class Main(Vk):
    def __init__(self):
        Vk.__init__(self, token=TOKEN, group_id=GROUP_ID)

    def message_new(self, msg):
        message = msg['object']['message']
        if not os.path.exists(f'data/{message["peer_id"]}/'):
            os.mkdir(f'data/{message["peer_id"]}')
            BaseFile(peer_id=message['peer_id']).create_chat()
        if 'action' in message:
            self.type_new_action(message)
        else:
            self.type_new_message(message)

    def type_new_action(self, msg):
        if msg['action']['type'] in ('chat_invite_user', ''):
            Captcha(msg, vk).send_captcha()

    def type_new_message(self, msg):
        base = BaseFile(peer_id=msg['peer_id'], name=msg['from_id'])
        vkm = MethodsVK(vk, msg['peer_id'])
        data = base.load()
        text = msg['text']

        if text != '' and data['is_captcha']:
            if text == data['ans']:
                data['is_captcha'] = False
                message = "Капча пройдена, личность подтверждена."
                vk.messages.send(message=message, peer_id=msg['peer_id'],
                                 random_id=random.randint(1, 273635637238293))
            else:
                data['retr'] -= 1
                if data['retr'] == 0:
                    data['is_captcha'] = True
                    data['time'] = 0
                    data['ans'] = False
                    vkm.kick_user(msg['from_id'])

    def is_admin(self):
        pass


if __name__ == '__main__':
    vk = Main()
    print("Started...")
    Thread(target=cpt.check_time, args=(vk,)).start()
    vk.start_listen()
