import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""A class to manage the ship."""

	def __init__(self, ai_game):
		"""Initialize the ship and set its starting position."""
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.setting = ai_game.settings

		# Load the ship image and get its rect.
		self.image = pygame.image.load('images/rocket.bmp')
		self.rect = self.image.get_rect()

		# Start each new ship at the bottom center of the screen.
		self.rect.midleft = self.screen_rect.midleft

		# Store a decimal value for the ship's horizontal position.
		self.x = float(self.rect.x)

		# Movement flag
		self.moving_top = False
		self.moving_bottom = False

	
	def update(self):
		"""Update the ship's position based on movement flags."""
		# Update the ship's x value, not the rect.
		if self.moving_top and self.rect.top > 0:
			self.y -= self.settings.ship_speed
		if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.settings.ship_speed

		# Update rect object from self.x.
		self.rect.x = self.x
		self.rect.y = self.y 
	
	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)
	
	def center_ship(self):
		"""Center the ship on the screen."""
		self.rect.midleft = self.screen_rect.midleft
		self.y = float(self.rect.y)
