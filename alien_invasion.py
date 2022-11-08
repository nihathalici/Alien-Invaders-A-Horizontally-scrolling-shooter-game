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
		self.settings.screen_width = self.screen.get_rect().width
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
					# Watch for keyboard and mouse events.
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
		"""Start a new game when the player clicks Play."""
		button_clicked = self.play_easy_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()
			# Reset the game settings.
			self.settings.initialize_easy_dynamic_settings()

	def _check_medium_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play."""
		button_clicked = self.play_medium_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()
			# Reset the game settings.
			self.settings.initialize_medium_dynamic_settings()

	def _check_hard_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play."""
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

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_images()
			sounds.hit_sound.play()
			self.sb.check_high_score()
			self._start_new_level()

	def _start_new_level(self):
		if not self.aliens:
			# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			# Increase level.
			self.stats.level += 1
			self.sb.prep_images()

	def _update_aliens(self):
		"""
		Check if the fleet is at an edge,
		  then update the positions of all aliens in the fleet.
		"""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Look for aliens hitting the bottom of the screen.
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.left <= screen_rect.left:
				# Treat this the same as if the ship got hit.
				self._ship_hit()
				break

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien."""
		if self.stats.ships_left > 0:
			# Decrement ships_left, and update scoreboard.
			self.stats.ships_left -= 1
			self.sb.prep_images()
			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()
			
			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()
			
			# Pause.
			sleep(1)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _create_fleet(self):
		"""Create the fleet of masters yi."""
		# Create a master yi and find the number of masters yi in a row.
		# Spacing between each masters yi which is equal to one master yi width.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		ship_height = self.ship.rect.width
		available_space_x = (self.settings.screen_height - 3 * alien_width) - ship_height
		number_aliens_x = available_space_x // (1 * alien_height)

		# Determine the number of rows of aliens that fit on the screen.
		available_space_y = self.settings.screen_height - (2 * alien_width)
		number_rows = available_space_y // (2 * alien_width)

		# Create the full fleet of masters yi1
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		# Create a master yi and place it in the row.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.y = alien_height + 2 * alien_height * row_number
		alien.rect.y = alien.y
		alien.rect.x = 650 - alien.rect.width + 2 * alien.rect.width * alien_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.x -= self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.achterground.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Draw the score information
		self.sb.show_score()
		self.ship.blitme()

		# Draw the play button if the game is inactive.
		if not self.stats.game_active:
			self.play_easy_button.draw_easy_button()
			self.play_medium_button.draw_medium_button()
			self.play_hard_button.draw_hard_button()
		
		pygame.display.flip()

if __name__ == '__main__':
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()
