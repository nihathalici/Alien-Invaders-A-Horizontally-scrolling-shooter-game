import pygame

# initialize pygame mixer
pygame.mixer.pre_init(frequency=44100, size=32, channels=1, buffer=2**12)
pygame.mixer.init()

bullet_sound = pygame.mixer.Sound('assets/ezreal_mysticshot.wav')
pygame.mixer.music.load("assets/ezreal_mysticshot.wav")

hit_sound = pygame.mixer.Sound('assets/collision.wav')
pygame.mixer.music.load('assets/collision.wav')