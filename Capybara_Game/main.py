import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Capybara Collector')

WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

capybara_x = WIDTH // 2
capybara_y = HEIGHT - 50
capybara_speed = 5
orange_speed = 3
score = 0
money = 0
time_elapsed = 0
orange_list = []

def draw_capybara():
    pygame.draw.rect(WINDOW, BLACK, (capybara_x, capybara_y, 50, 30))

def draw_oranges():
    for orange in orange_list:
        pygame.draw.circle(WINDOW, ORANGE, orange, 20)

def draw_score():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    money_text = font.render(f"Money: ${money}", True, BLACK)
    time_text = font.render(f"Time: {int(time_elapsed)}s", True, BLACK)
    WINDOW.blit(score_text, (10, 10))
    WINDOW.blit(money_text, (10, 50))
    WINDOW.blit(time_text, (10, 90))

def menu():
    WINDOW.fill(WHITE)
    font = pygame.font.SysFont(None, 74)
    title_text = font.render('Capybara Collector', True, BLACK)
    WINDOW.blit(title_text, (WIDTH // 4, HEIGHT // 4))

    font = pygame.font.SysFont(None, 48)
    menu_items = ['Start Game', 'Options', 'Levels', 'Customization', 'Collectibles', 'Reset Progress', 'Quit']
    for i, item in enumerate(menu_items):
        menu_text = font.render(item, True, BLACK)
        WINDOW.blit(menu_text, (WIDTH // 4, HEIGHT // 2 + i * 50))

    pygame.display.update()

def handle_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def game_loop():
    global capybara_x, capybara_y, orange_list, score, money, time_elapsed
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()