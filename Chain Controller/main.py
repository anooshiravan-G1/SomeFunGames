import pygame
import random
import json
import os
from chain import Chain
from item import Item
from obstacle import Obstacle
from utils import show_score
from draw_utils import draw_background, draw_snake, draw_item, draw_score
from menu import main_menu

# Initialize pygame
pygame.init()

# Set up display
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chain Collector")

# Set up game clock
clock = pygame.time.Clock()
fps = 10

# Segment size
segment_size = 20

# High scores file
high_scores_file = "high_scores.json"


# Load high scores
def load_high_scores():
    if os.path.exists(high_scores_file):
        with open(high_scores_file, "r") as file:
            return json.load(file)
    return []


# Save high scores
def save_high_scores(scores):
    with open(high_scores_file, "w") as file:
        json.dump(scores, file)


# Show high scores
def show_high_scores(window, width, height):
    high_scores = load_high_scores()
    menu_font = pygame.font.Font(None, 74)
    text_color = (0, 0, 0)
    background_color = (245, 245, 220)
    small_font = pygame.font.Font(None, 50)

    window.fill(background_color)

    title_surface = menu_font.render("High Scores", True, text_color)
    window.blit(title_surface, (width // 4, height // 8))

    for i, score in enumerate(high_scores[:5], start=1):
        score_surface = small_font.render(f"{i}. {score}", True, text_color)
        window.blit(score_surface, (width // 4, height // 4 + i * 50))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return


# Main game loop
def main_game():
    chain = Chain(width, height, segment_size)
    item = Item(width, height, segment_size)
    obstacles = [Obstacle(width, height, segment_size) for _ in range(5)]

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and chain.direction != (1, 0):
                    chain.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT and chain.direction != (-1, 0):
                    chain.set_direction((1, 0))
                elif event.key == pygame.K_UP and chain.direction != (0, 1):
                    chain.set_direction((0, -1))
                elif event.key == pygame.K_DOWN and chain.direction != (0, -1):
                    chain.set_direction((0, 1))

        # Move the chain
        chain.move()

        # Check for item collection
        if chain.segments[0].x == item.x and chain.segments[0].y == item.y:
            chain.grow()
            item.respawn()
            score += 1

        # Check for collisions
        if chain.check_collision():
            running = False

        # Draw everything
        draw_background(window, width, height, segment_size)
        draw_snake(window, chain, segment_size)
        draw_item(window, item, segment_size)
        draw_score(window, score)

        # Update display
        pygame.display.update()

        # Control game speed
        clock.tick(fps)

    high_scores = load_high_scores()
    high_scores.append(score)
    high_scores = sorted(high_scores, reverse=True)[:5]
    save_high_scores(high_scores)


# Main loop
while True:
    choice = main_menu(window, width, height)
    if choice == "play":
        main_game()
    elif choice == "records":
        show_high_scores(window, width, height)
    elif choice == "quit":
        break

pygame.quit()
