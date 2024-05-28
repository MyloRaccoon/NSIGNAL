import pygame
from os import path


def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)


class Writer():
    def __init__(self):
        self.image = pygame.image.load(get_file('assets\\writer_block.png'))
        self.can_write = True
        self.n_blocks = 1
        self.cursor_pos = (0, 0)
        self.cont = [[]]
        self.current_line = 0
