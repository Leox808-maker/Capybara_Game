import pygame
import os
import json
import random


class GameOverScreen:
    def __init__(self, window, score, high_scores, level, difficulty):
        self.window = window
        self.score = score
        self.high_scores = high_scores
        self.level = level
        self.difficulty = difficulty
        self.background_img = pygame.image.load(os.path.join('assets', 'game_over_bg.png'))
        self.font = pygame.font.SysFont(None, 48)
        self.button_font = pygame.font.SysFont(None, 36)
        self.button_color = (200, 0, 0)
        self.button_hover_color = (255, 0, 0)
        self.button_rects = {
            'Menu': pygame.Rect(WIDTH // 4, HEIGHT - 100, 150, 50),
            'Restart': pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50),
            'Tips': pygame.Rect(WIDTH // 4 + 200, HEIGHT - 100, 150, 50)
        }
        self.tips = [
            "Try to move quickly to catch more oranges!",
            "Don't forget to collect bonus items for extra points!",
            "Higher levels offer better rewards!",
            "Watch out for falling items!",
            "Keep an eye on your score to beat the high score!"
        ]
        self.running = True
        self.music = pygame.mixer.music.load(os.path.join('assets', 'game_over_music.mp3'))
        pygame.mixer.music.play(-1)
        self.update_high_scores()
        self.save_game_state()

    def draw_game_over_screen(self):
        self.window.blit(self.background_img, (0, 0))
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = self.font.render(f"High Score: {self.high_scores[self.difficulty]}", True, (255, 255, 255))
        self.window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
        self.window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 4 + 60))
        self.window.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 4 + 120))
        pygame.draw.rect(self.window, self.button_color, self.button_rects['Menu'])
        pygame.draw.rect(self.window, self.button_color, self.button_rects['Restart'])
        pygame.draw.rect(self.window, self.button_color, self.button_rects['Tips'])
        menu_text = self.button_font.render("Menu", True, (255, 255, 255))
        restart_text = self.button_font.render("Restart", True, (255, 255, 255))
        tips_text = self.button_font.render("Tips", True, (255, 255, 255))
        self.window.blit(menu_text, (self.button_rects['Menu'].x + 15, self.button_rects['Menu'].y + 10))
        self.window.blit(restart_text, (self.button_rects['Restart'].x + 15, self.button_rects['Restart'].y + 10))
        self.window.blit(tips_text, (self.button_rects['Tips'].x + 15, self.button_rects['Tips'].y + 10))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.button_rects['Menu'].collidepoint(mouse_pos):
                    self.running = False
                    return 'menu'
                if self.button_rects['Restart'].collidepoint(mouse_pos):
                    self.running = False
                    return 'restart'
                if self.button_rects['Tips'].collidepoint(mouse_pos):
                    self.show_tips()
        return None

    def update_high_scores(self):
        if self.score > self.high_scores[self.difficulty]:
            self.high_scores[self.difficulty] = self.score
            self.save_high_scores()


