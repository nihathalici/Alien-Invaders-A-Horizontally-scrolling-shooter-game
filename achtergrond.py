import pygame

class Background:
	"""A class to manage the background."""

	def __init__(self, ai_game):
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.settings = ai_game.settings

		# Load the background image and get its rect.
		self.image = pygame.image.load('images/background2.jpg')
		self.rect = self.image.get_rect()

		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
	
	def blitme(self):
		"""Draw background image."""
		self.screen.blit(self.image, self.rect)
