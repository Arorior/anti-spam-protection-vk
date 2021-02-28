class MethodsVK:
    def __init__(self, vk, peer_id):
        self.peer_id = peer_id
        self.vk = vk

    def kick_user(self, from_id):
        self.vk.messages.removeChatUser(chat_id=self.peer_id - 2000000000,
                                        user_id=from_id)

