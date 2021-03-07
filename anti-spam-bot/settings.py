import basefile


class ChatSettings:
    def __init__(self, chat_id, text):
        self.split = text
        self.base = basefile.BaseFile(chat_id)

        if self.get_type() == 'set':
            self.to_set()
        elif self.get_type() == 'change':
            self.re_text = self.to_change()
        else:
            self.re_text = 'Невозможно произвести действие'

    def get_text(self):
        return self.re_text

    def get_type(self):
        if len(self.split) - 1 == 1:
            return 'change'
        elif len(self.split) - 1 == 2:
            return 'set'

    def to_change(self):
        split = self.split
        params = {'need_captcha': ['captcha', 'капча']}
        for param in params:
            if split[1] in params[param]:
                data = self.base.load()
                if param not in data:
                    data[param] = False
                data[param] = not data[param]
                self.base.upload(data)
                return f'Параметр {split[1]} был успешно изменен на {data[param]}'
        return 'Нельзя изменить данный обьект, так как он не сущетсвует в списке'

    def to_set(self):
        pass
