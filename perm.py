import pygame
from os import path


def get_file(name):
	return path.join(path.dirname(path.realpath(__file__)), name)

class Perm:

	def __init__(self):
		self.ban = ['david.minet']
		self.admin = []
		self.mute = []

	def banir(self, str):
		with open(get_file('perm/ban.txt'), 'a') as f:
			f.writelines(str + '|')

	def muter(self, str):
		with open(get_file('perm/mute.txt'), 'a') as f:
			f.writelines(str + '|')

	def adminer(self, str):
		with open(get_file('perm/admin.txt'), 'a') as f:
			f.writelines(str + '|')

	def read_file(self, file):
		with open(get_file('perm/' + file + '.txt'), 'r') as f:
			s = f.read()
		return s

	def update(self):
		self.ban = ['david.minet']
		self.admin = []
		self.mute = []

		l=self.read_file('ban').split('|')
		for b in range(len(l)-1):
			self.ban.append(l[b])

		l=self.read_file('mute').split('|')
		for m in range(len(l)-1):
			self.mute.append(l[m])

		l=self.read_file('admin').split('|')
		for a in range(len(l)-1):
			self.admin.append(l[a])