from json import loads, dumps


class Tokens:
    def __init__(self):
        self.Telegram = ''
        self.chat_id = 0
        with open('tokens', 'r') as f:
            js = loads(f.readline())
            self.Telegram = js["Telegram"]
            self.chat_id = js["Chat_id"]

    def save(self):
        dump = dumps({'Telegram': self.Telegram})
        with open('tokens', 'w') as f:
            f.write(dump)
