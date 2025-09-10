import pygame

def show_score(window, score):
    font = pygame.font.SysFont(None, 35)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(text, [0, 0])
