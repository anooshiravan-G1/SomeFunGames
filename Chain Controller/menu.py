import pygame

def main_menu(window, width, height):
    menu_font = pygame.font.Font(None, 74)
    text_color = (0, 0, 0)
    background_color = (245, 245, 220)
    menu_items = ["1. Play", "2. Show Records"]
    
    selected = None
    
    while selected is None:
        window.fill(background_color)
        
        for i, item in enumerate(menu_items):
            text_surface = menu_font.render(item, True, text_color)
            window.blit(text_surface, (width // 4, height // 4 + i * 100))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = "play"
                elif event.key == pygame.K_2:
                    selected = "records"
    
    return selected
