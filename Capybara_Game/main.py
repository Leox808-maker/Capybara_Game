import os

import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Capybara Oranges')

WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

ASSET_DIR = 'assets'
CAPYBARA_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'capybara.png'))
ORANGE_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'orange.png'))

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            capybara_x -= capybara_speed
        if keys[pygame.K_RIGHT]:
            capybara_x += capybara_speed

        if capybara_x < 0:
            capybara_x = 0
        if capybara_x > WIDTH - CAPYBARA_IMG.get_width():
            capybara_x = WIDTH - CAPYBARA_IMG.get_width()

        if random.randint(1, 20) == 1:
            orange_x = random.randint(20, WIDTH - 20)
            orange_list.append([orange_x, 0])

        orange_list = [[x, y + orange_speed] for x, y in orange_list]

        new_orange_list = []
        for x, y in orange_list:
            if y > HEIGHT:
                continue
            if capybara_x < x < capybara_x + CAPYBARA_IMG.get_width() and capybara_y < y < capybara_y + CAPYBARA_IMG.get_height():
                score += 1
                money += 15
            else:
                new_orange_list.append([x, y])
        orange_list = new_orange_list

        time_elapsed = (pygame.time.get_ticks() - start_time) / 1000

        WINDOW.fill(WHITE)
        draw_capybara()
        draw_oranges()
        draw_score()
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    while True:
        menu()
        handle_menu()
        game_loop()