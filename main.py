import pygame
from os import path
from writer import Writer
from message import Message
from msg_reader import Reader
from perm import Perm
import getpass
pygame.init()

def get_file(name):
	return path.join(path.dirname(path.realpath(__file__)), name)

pygame.display.set_caption('NSIGNAL')
screen = pygame.display.set_mode((800,600))

pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

font = pygame.font.SysFont(None, 25)

bg = pygame.image.load(get_file('assets\\bg.png'))

writer = Writer()

reader = Reader(screen)
reader.update_all_msg()

running = True

def get_long():
	l = []
	for msg in reader.all_msg:
		l.append(msg.longueur*20 + 50)
	return sum(l)

scroll = 450 - get_long()

perm = Perm()

while running:

	reader.update_all_msg()

	perm.update()

	if str(getpass.getuser()) in perm.ban:
		exit()

	screen.blit(bg, (0,0))

	for message in reader.all_msg:
		message.update_pos(reader.all_msg[:message.id_m], scroll)

	for i in range(len(reader.all_msg)):
		screen.blit(reader.all_msg[len(reader.all_msg)-i-1].image, reader.all_msg[len(reader.all_msg)-i-1].rect)
		screen.blit(reader.all_msg[len(reader.all_msg)-i-1].author.image, reader.all_msg[len(reader.all_msg)-i-1].author.rect)
		reader.all_msg[len(reader.all_msg)-i-1].write()

	if len(writer.cont[writer.current_line]) >= 46 and len(writer.cont)!=5:
		writer.current_line+=1
		writer.cont.append([])

	if len(writer.cont) ==5 and len(writer.cont[writer.current_line]) >= 46:
		writer.can_write = False
	else:
		writer.can_write = True

	screen.blit(writer.image, (0,500))
	for i in range(len(writer.cont)):
		screen.blit(font.render(''.join(writer.cont[i]), True, (255,255,255)), (50,500 + i*20))

	pygame.display.flip()

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False
			pygame.quit()

		elif event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL):
				text = pygame.scrap.get(pygame.SCRAP_TEXT)[:-1].strip().decode("ISO-8859-1")
				first, *rest = text.splitlines()
				writer.cont[writer.current_line].append(first)
				writer.cont.append(rest)
				writer.current_line += len(rest)

			if writer.can_write and event.key not in [pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_KP_ENTER] and event.unicode not in ['|', '§', "", ""]:
				writer.cont[writer.current_line].append(event.unicode)

			elif event.key == pygame.K_BACKSPACE:
				if len(writer.cont[writer.current_line])>=1:
					writer.cont[writer.current_line].pop()
				else:
					if writer.current_line > 0:
						writer.cont.pop()
						writer.current_line -= 1
						writer.cont[writer.current_line].pop()

			elif event.key == pygame.K_KP_ENTER and writer.current_line < 5:
				writer.current_line += 1
				writer.cont.append([])

			elif event.key == pygame.K_ESCAPE:
				writer.current_line = 0
				writer.cont = [[]]

			elif event.key == pygame.K_RETURN and writer.cont != [[]] and str(getpass.getuser()) not in perm.mute:

				if str(getpass.getuser()) in perm.admin and ''.join(writer.cont[0]) == '/clear':
					reader.vider_file()
				else:
					if str(getpass.getuser()) == 'joachim.fevre' and ''.join(writer.cont[0]) == '/ban' and len(writer.cont) > 1 and ''.join(writer.cont[1]) != 'joachim.fevre':
						print(True)
						perm.banir(''.join(writer.cont[1]))
					elif str(getpass.getuser()) in perm.admin and ''.join(writer.cont[0]) == '/mute' and len(writer.cont) > 1 and ''.join(writer.cont[1]) != 'joachim.fevre':
						print(True)
						perm.muter(''.join(writer.cont[1]))
					elif str(getpass.getuser()) in perm.admin and ''.join(writer.cont[0]) == '/admin' and len(writer.cont) > 1:
						perm.adminer(''.join(writer.cont[1]))
					m = reader.create_msg(writer.cont, str(getpass.getuser()))
					writer.current_line = 0
					writer.cont = [[]]
					scroll = 450 - get_long()
					reader.write_msg(m)

			if event.key == pygame.K_UP:
				scroll += 50
			if event.key == pygame.K_DOWN:
				scroll -= 50
			if event.key == pygame.K_LEFT:
				scroll = 0
			if event.key == pygame.K_RIGHT:
				scroll = 450 - get_long()