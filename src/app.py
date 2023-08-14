import pygame, sys, time
from settings import * 
from level import Level


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(screen)
restart = False
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	keys = pygame.key.get_pressed()

	screen.fill('black')
	restart = level.run()

	if restart and keys[pygame.K_RETURN]:
		
		level = Level(screen)
		time.sleep(0.5)
		continue
		
		

	pygame.display.update()
	clock.tick(60)  