import sys
from time import sleep
import pygame
import json
from settings import Settings
from achtergrond import Background
from game_stats import GameStats
from scoreboard import Scoreboard
from easy_button import EasyButton
from medium_button import MediumButton
from hard_button import HardButton
from ship import Ship
from bullet import Bullet
from alien import Alien
import sounds

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width()
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		# Create an instance to store game statistics.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.achterground = Background(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# Make the Play buttons.
		self.play_easy_button = EasyButton(self, "Easy mode")
		self.play_medium_button = MediumButton(self, "Medium mode")
		self.play_hard_button = HardButton(self, "Hard mode")


	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

	
	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_easy_play_button(mouse_pos)
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_medium_play_button(mouse_pos)
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_hard_play_button(mouse_pos)


	def _check_easy_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Easy Modus Button."""
		button_clicked = self.play_easy_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()
			# Reset the game settings.
			self.settings.initialize_easy_dynamic_settings()


	def _check_medium_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Medium Modus Button."""
		button_clicked = self.play_medium_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()
			# Reset the game settings.
			self.settings.initialize_medium_dynamic_settings()
			

	def _check_hard_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Hard Modus Button."""
		button_clicked = self.play_hard_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()
		    # Reset the game settings.
			self.settings.initialize_hard_dynamic_settings()

	def _check_keydown_events(self, event):
		"""Respond to keypresses."""
		if event.key == pygame.K_UP:
			self.ship.moving_top = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_bottom = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p:
			self._start_game()

	def _start_game(self):
		# Reset the game statistics.
		self.stats.reset_stats()
		self.stats.game_active = True
		self.sb.prep_images()

		# Get rid of any remaining aliens and bullets.
		self.aliens.empty()
		self.bullets.empty()

		# Create a new fleet and center the ship.
		self._create_fleet()
		self.ship.center_ship()

		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)
		

	def _check_keyup_events(self, event):
		"""Respond to key releases."""
		if event.key == pygame.K_UP:
			self.ship.moving_top = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_bottom = False	

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
			sounds.bullet_sound.play()

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
		# Update bullet positions.
		self.bullets.update()

		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.x >= self.settings.screen_width:
				self.bullets.remove(bullet)
		
		self._check_bullet_alien_collisions()


	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions."""
		# Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		self.sb.prep_images()
		sounds.hit_sound.play()
		self.sb.check_high_score()
		self._start_new_level()

	def _start_new_level(self):
		pass

	def _update_aliens(self):
		pass

	def _check_aliens_bottom(self):
		pass

	def _ship_hit(self):
		pass

	def _create_fleet(self):
		pass

	def _create_alien(self):
		pass

	def _check_fleet_edges(self):
		pass

	def _change_fleet_direction(self):
		pass

	def _update_screen(self):
		pass





if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()