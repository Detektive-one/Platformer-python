import pygame 

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size,color):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.color = color
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift
		
	def get_color(self):
		return self.color
		
		
    