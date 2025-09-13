# main.py

import pygame
from game import SpaceInvadersGame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN


def show_main_menu():
    """Display the main menu before launching the game."""
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders - Main Menu")

    clock = pygame.time.Clock()
    running = True

    font_large = pygame.font.Font(None, 74)  # Now safe to use
    font_medium = pygame.font.Font(None, 36)

    while running:
        screen.fill(BLACK)

        # Title
        title = font_large.render("SPACE INVADERS", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # Menu options
        options = [
            ("Start Game", "S"),
            ("How to Play", "H"),
            ("Quit", "Q"),
        ]

        for i, (text, key) in enumerate(options):
            option_text = font_medium.render(f"{text} ({key})", True, WHITE)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 60))
            screen.blit(option_text, option_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Start
                    pygame.quit()  # Close the menu window
                    game = SpaceInvadersGame()
                    game.run()  # This will re-init display & font internally
                    return
                elif event.key == pygame.K_h:  # How to Play
                    show_instructions(screen, font_medium)
                elif event.key == pygame.K_q:  # Quit
                    running = False

        clock.tick(60)

    pygame.quit()


def show_instructions(screen, font):
    """Show instructions screen."""
    instructions = [
        "HOW TO PLAY:",
        "",
        "• Use LEFT/RIGHT arrow keys or A/D to move.",
        "• Press SPACE to shoot.",
        "• Collect power-ups: Yellow=Rapid Fire, Blue=Multi-Shot, Purple=Shield.",
        "• Defeat all enemies to advance waves.",
        "• Don't let enemies reach the bottom!",
        "",
        "Press any key to return...",
    ]

    running = True
    while running:
        screen.fill(BLACK)

        for i, line in enumerate(instructions):
            text = font.render(line, True, WHITE)
            screen.blit(text, (50, 100 + i * 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False


if __name__ == "__main__":
    show_main_menu()
