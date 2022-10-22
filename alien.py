import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to represent a single alien in the fleet."""

	def __init__(self, ai_game):
		"""Initialize the alien and set its starting position."""
		pass

	def check_edges(self):
		"""Return True if alien is at edge of screen."""
		pass

	def update(self):
		"""Move the alien to the top or bottom."""
		pass
