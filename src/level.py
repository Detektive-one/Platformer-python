import pygame 
from tiles import Tile 
from settings import *
from player import Player
from particles import ParticleEffect

class Level:
	def __init__(self,surface):
		
		# level setup
		self.display_surface = surface 
		self.setup_level(level_map)
		self.world_shift = 0
		self.current_x = 0

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False
		self.gameOn = True

		#over
		self.game_over_delay = 600  
		self.game_over_triggered_time = None
        

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				
				if cell == 'X':
					tile = Tile((x,y),tile_size, 'brown')
					self.tiles.add(tile)
				if cell == 'P':
					player_sprite = Player((x,y),self.display_surface,self.create_jump_particles)
					self.player.add(player_sprite)
				if cell == 'D':
					tile = Tile((x,y),tile_size, 'grey')
					self.tiles.add(tile)
				if cell == 'E':
					tile = Tile((x,y),tile_size, 'blue')
					self.tiles.add(tile)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False


	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for tile in self.tiles.sprites():
			if tile.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = tile.rect.top
					player.direction.y = 0
					player.on_ground = True

					if tile.get_color() == 'grey':
						player.live = False		
						self.gameOn = False		
						self.game_over_triggered_time = pygame.time.get_ticks()		
					else:
						player.live = True
				elif player.direction.y < 0:
					player.rect.top = tile.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

	def gameOver(self):
		
		font1 = pygame.font.SysFont('Lucida Sans' , 40)
		font2 = pygame.font.SysFont('Lucida Sans' , 30)
		x = 490
		y = 300
		img = font1.render('Game Over', True, 'blue')
		img2 = font2.render('Press Enter to restart', True, 'blue')
		self.display_surface.blit(img, (x,y))
		self.display_surface.blit(img2, (x-50,y+100))

	
	def run(self):
		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		# level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)
		self.scroll_x()

		current_time = pygame.time.get_ticks()

		# player
		
		if self.gameOn:
			self.player.update()
			self.horizontal_movement_collision()
			self.get_player_on_ground()
			self.vertical_movement_collision()
			self.create_landing_dust()
			self.player.draw(self.display_surface)
		else:
			if current_time - self.game_over_triggered_time < self.game_over_delay:
				self.player.update()
				self.player.draw(self.display_surface)
			# if current_time - self.game_over_triggered_time > self.game_over_delay:
			else:				
				self.gameOver()

				return True
				
                
            
