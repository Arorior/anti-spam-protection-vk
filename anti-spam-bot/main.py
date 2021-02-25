from saya import Vk

from basefile import BaseFile
from captcha.captcha import Captcha

_data = open('.data', 'r').read().split('\n')
TOKEN, GROUP_ID = _data


class Main(Vk):
    def __init__(self):
        Vk.__init__(self, token=TOKEN, group_id=GROUP_ID)

    def message_new(self, msg):
        message = msg['object']['message']
        if 'action' in message:
            self.type_new_action(message)
        else:
            self.type_new_message(message)

    def type_new_action(self, msg):
        if msg['action']['type'] in ('chat_invite_user', ''):
            Captcha(msg['peer_id'], vk).send_captcha()


    def type_new_message(self, msg):
        pass

    def is_admin(self):
        pass


if __name__ == '__main__':
    vk = Main()
    print("Started...")
    vk.start_listen()
