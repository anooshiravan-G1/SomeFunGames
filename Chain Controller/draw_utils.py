import pygame

def draw_background(window, width, height, segment_size):
    beige = (245, 245, 220)
    window.fill(beige)

def draw_snake(window, chain, segment_size):
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    head = chain.segments[0]
    pygame.draw.circle(window, red, (head.x + segment_size // 2, head.y + segment_size // 2), segment_size // 2)
    
    eye_radius = segment_size // 4
    eye_offset_x = segment_size // 4
    eye_offset_y = segment_size // 8
    pygame.draw.circle(window, white, (head.x + eye_offset_x, head.y + eye_offset_y), eye_radius)
    pygame.draw.circle(window, white, (head.x + segment_size - eye_offset_x, head.y + eye_offset_y), eye_radius)
    pygame.draw.circle(window, black, (head.x + eye_offset_x, head.y + eye_offset_y), eye_radius // 2)
    pygame.draw.circle(window, black, (head.x + segment_size - eye_offset_x, head.y + eye_offset_y), eye_radius // 2)
    
    for i, segment in enumerate(chain.segments[1:], start=1):
        color = yellow if i % 2 == 0 else red
        pygame.draw.circle(window, color, (segment.x + segment_size // 2, segment.y + segment_size // 2), segment_size // 2)

def draw_item(window, item, segment_size):
    red = (255, 0, 0)
    black = (0, 0, 0)
    
    pygame.draw.circle(window, red, (item.x + segment_size // 2, item.y + segment_size // 2), segment_size // 2)
    pygame.draw.rect(window, black, (item.x + segment_size // 4, item.y - segment_size // 4, segment_size // 2, segment_size // 4))

def draw_score(window, score):
    font = pygame.font.Font(None, 35)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(text, (10, 10))
