class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		# Ship settings
		self.ship_limit = 2

		# Bullet settings
		self.bullet_width = 15
		self.bullet_height = 5
		self.bullet_color = (255, 255, 255)
		self.bullets_allowed = 10

		# Alien settings
		self.fleet_drop_speed = 30

		# fleet direction
		self.fleet_direction = 1

		# How quickly the game speeds up
		self.speedup_scale = 1.1

		# How quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_easy_dynamic_settings()
		self.initialize_medium_dynamic_settings()
		self.initialize_hard_dynamic_settings()

	def initialize_easy_dynamic_settings(self):
		"""Initialize settings for easy modus that change throughout the game."""
		self.ship_speed = 3.5
		self.bullet_speed = -5
		self.alien_speed = 1.5
		self.fleet_direction = 1.5

		# Scoring
		self.alien_points = 50

	def initialize_medium_dynamic_settings(self):
		"""Initialize settings for medium modus that change throughout the game."""
		self.ship_speed = 4
		self.bullet_speed = -4.5
		self.alien_speed = 2
		self.fleet_direction = 2

		# Scoring
		self.alien_points = 50

	def initialize_hard_dynamic_settings(self):
		"""Initialize settings for hard modus that change throughout the game."""
		self.ship_speed = 4.5
		self.bullet_speed = -5
		self.alien_speed = 2.5
		self.fleet_direction = 2.5

		# Scoring
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *=self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
