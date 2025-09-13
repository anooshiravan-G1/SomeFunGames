import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)

# Gameplay
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 1

# Power-up durations (in frames @ 60 FPS)
POWERUP_DURATION = {
    "rapid_fire": 300,  # 5 seconds
    "multi_shot": 300,
    "shield": 600,  # 10 seconds
}

# Enemy shooting delay range
ENEMY_SHOOT_DELAY_MIN = 120
ENEMY_SHOOT_DELAY_MAX = 300

# Spawn chance
POWERUP_SPAWN_CHANCE = 0.1
ENEMY_SPAWN_CHANCE = 0.02

# UI
FONT_SIZE_LARGE = 74
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 28


ENEMY_BASE_SPEED = 1.0  # Base speed for Wave 1
ENEMY_SPEED_INCREASE = 0.15
