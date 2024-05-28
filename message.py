import pygame
from os import path

def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)

class Message():

	def __init__(self, author, cont, id_m, longueur, screen):
		self.id_m = id_m
		self.longueur = longueur
		self.image = pygame.image.load(get_file('assets\\message' + str(longueur) + '.png'))
		self.screen = screen
		self.cont = cont
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		self.author = Author(author, id_m)
		self.font = pygame.font.SysFont(None, 25)

	def update_pos(self, all_msg, scroll):
		l= []
		for msg in all_msg:
			l.append(msg.longueur*20 + 50)
		l = sum(l) 

		self.rect.y = l + 50 + scroll
		self.author.rect.y = l + scroll

	def write(self):
		self.screen.blit(self.font.render(self.author.name, True, (200,200,200)), (50, self.author.rect.y + 30))
		for i in range(len(self.cont)):
			self.screen.blit(self.font.render(''.join(self.cont[i]), True, (255,255,255)), (50, self.rect.y + i*20))

class Author():

	def __init__(self, author, id_m):
		self.image = pygame.image.load(get_file('assets\\autheur.png'))
		self.rect = self.image.get_rect()
		self.name = author + ' :'
		self.string = author
		self.rect.x = 0
		self.rect.y = id_m*100