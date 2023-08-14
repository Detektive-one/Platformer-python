import pygame

class CollisionBlock:
    def __init__(self, screen, y_offset=0):  # Add y_offset as an optional parameter
        self.screen = screen
        self.block_size = 16
        self.scale_factor = 4
        self.y_offset = y_offset  # Store the y-offset value
        self.positions = []  # List to store positions of drawn blocks

    def draw(self, x, y):
        scaled_block_size = self.block_size * self.scale_factor

        # Use y_offset in the calculation of the y-coordinate
        y_position = (y + self.y_offset) * scaled_block_size

        self.positions.append((x * scaled_block_size, y_position))  # Store the position
        pygame.draw.rect(self.screen, (255, 204, 203), (x * scaled_block_size, y_position, scaled_block_size, scaled_block_size))



