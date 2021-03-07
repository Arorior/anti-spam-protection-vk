import os
import random
from threading import Thread

import captcha.captcha as cpt
from saya import Vk

from basefile import BaseFile
from captcha.captcha import Captcha
from vkm import MethodsVK
from settings import ChatSettings

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
            if BaseFile(peer_id=msg['peer_id']).load()['need_captcha']:
                Captcha(msg, vk).send_captcha()

    def type_new_message(self, msg):
        base = BaseFile(peer_id=msg['peer_id'], name=msg['from_id'])
        vkm = MethodsVK(vk, msg['peer_id'])
        data = base.load()
        text = msg['text']
        split = text.split(' ')

        if data['is_captcha']:
            if text.lower() == data['ans']:
                data['is_captcha'] = False
                message = "Капча пройдена, личность подтверждена."
                vk.messages.send(message=message, peer_id=msg['peer_id'],
                                 random_id=random.randint(1, 273635637238293))
            else:
                data['retr'] -= 1
                if data['retr'] == 1:
                    message = "Предупреждение: Вспомните о капче, ведь у вас осталась 1 попытка..."
                    vk.messages.send(message=message, peer_id=msg['peer_id'],
                                     random_id=random.randint(1, 273635637238293))
                if data['retr'] == 0:
                    data['is_captcha'] = True
                    data['time'] = 0
                    data['ans'] = False
                    vkm.kick_user(msg['from_id'])

        else:
            if split[0] in ('!setting', '!change', '!set', '!настройки'):
                if not self.is_admin():
                    message = 'Данную команду могут выполнять только администраторы'
                    vk.messages.send(message=message, peer_id=msg['peer_id'],
                                     random_id=random.randint(1, 273635637238293))
                    return
                message = ChatSettings(msg['peer_id'], split).get_text()

                vk.messages.send(message=message, peer_id=msg['peer_id'],
                                 random_id=random.randint(1, 273635637238293))

        base.upload(data)

    def is_admin(self):
        return True


if __name__ == '__main__':
    vk = Main()
    print("Started...")
    Thread(target=cpt.check_time, args=(vk,)).start()
    vk.start_listen()
