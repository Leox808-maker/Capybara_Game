import pygame
import sys
import random
import os
import json

class Game:
    def __init__(self, window, level, difficulty):
        self.window = window
        self.level = level
        self.difficulty = difficulty
        self.capybara_img = pygame.image.load(os.path.join('assets', 'capybara.png'))
        self.orange_img = pygame.image.load(os.path.join('assets', 'orange.png'))
        self.apple_img = pygame.image.load(os.path.join('assets', 'apple.png'))
        self.banana_img = pygame.image.load(os.path.join('assets', 'banana.png'))
        self.capybara_x = WIDTH // 2
        self.capybara_y = HEIGHT - 70
        self.capybara_speed = 5
        self.orange_speed = 3 + (level - 1) * 2
        self.score = 0
        self.money = 0
        self.time_elapsed = 0
        self.orange_list = []
        self.bonus_list = []
        self.start_time = pygame.time.get_ticks()
        self.difficulty_multiplier = {'Easy': 0.5, 'Normal': 1, 'Hard': 1.5}[difficulty]
        self.capybara_health = 100
        self.max_health = 100
        self.health_bar_length = 200
        self.health_bar_height = 20
        self.spawn_interval = max(60 - (level - 1) * 5, 10)
        self.spawn_timer = 0
        self.bonus_timer = 0
        self.running = True
        self.sound_effects = {
            'collect': pygame.mixer.Sound(os.path.join('assets', 'collect.wav')),
            'hit': pygame.mixer.Sound(os.path.join('assets', 'hit.wav')),
            'bonus': pygame.mixer.Sound(os.path.join('assets', 'bonus.wav')),
            'bg_music': pygame.mixer.music.load(os.path.join('assets', 'background.mp3'))
        }
        pygame.mixer.music.play(-1)
        self.load_high_scores()
    def load_high_scores(self):
        if os.path.exists('high_scores.json'):
            with open('high_scores.json', 'r') as f:
                self.high_scores = json.load(f)
        else:
            self.high_scores = {'Easy': 0, 'Normal': 0, 'Hard': 0}

    def save_high_scores(self):
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)

    def draw_capybara(self):
        self.window.blit(self.capybara_img, (self.capybara_x, self.capybara_y))

    def draw_oranges(self):
        for orange in self.orange_list:
            self.window.blit(self.orange_img, (orange[0], orange[1]))

    def draw_bonus(self):
        for bonus in self.bonus_list:
            if bonus[2] == 'apple':
                self.window.blit(self.apple_img, (bonus[0], bonus[1]))
            elif bonus[2] == 'banana':
                self.window.blit(self.banana_img, (bonus[0], bonus[1]))

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        money_text = font.render(f"Money: ${self.money}", True, BLACK)
        time_text = font.render(f"Time: {int(self.time_elapsed)}s", True, BLACK)
        health_text = font.render(f"Health: {self.capybara_health}", True, BLACK)
        self.window.blit(score_text, (10, 10))
        self.window.blit(money_text, (10, 50))
        self.window.blit(time_text, (10, 90))
        self.window.blit(health_text, (10, 130))
        self.draw_health_bar()
    def draw_health_bar(self):
        pygame.draw.rect(self.window, BLACK, (10, 160, self.health_bar_length, self.health_bar_height))
        pygame.draw.rect(self.window, (255, 0, 0), (10, 160, self.health_bar_length, self.health_bar_height), 2)
        health_width = int(self.health_bar_length * (self.capybara_health / self.max_health))
        pygame.draw.rect(self.window, (0, 255, 0), (10, 160, health_width, self.health_bar_height))

    def spawn_orange(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            orange_x = random.randint(20, WIDTH - 40)
            self.orange_list.append([orange_x, 0])
            if random.random() < 0.1:  # 10% chance to spawn a bonus
                bonus_type = random.choice(['apple', 'banana'])
                self.bonus_list.append([orange_x, 0, bonus_type])

    def move_oranges(self):
        self.orange_list = [[x, y + self.orange_speed] for x, y in self.orange_list]

    def move_bonus(self):
        self.bonus_list = [[x, y + self.orange_speed * 0.5, t] for x, y, t in self.bonus_list]
    def update_high_scores(self):
        if self.score > self.high_scores[self.difficulty]:
            self.high_scores[self.difficulty] = self.score