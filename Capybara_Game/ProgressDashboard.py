import pygame
import os
import json

class ProgressDashboard:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)
        self.button_font = pygame.font.SysFont(None, 36)
        self.background_img = pygame.image.load(os.path.join('assets', 'dashboard_bg.png'))
        self.button_color = (0, 100, 0)
        self.button_hover_color = (0, 150, 0)
        self.button_rects = {
            'Menu': pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50)
        }
        self.stats = self.load_stats()
        self.past_games = self.load_past_games()
        self.totals = self.calculate_totals()
        self.prizes = self.load_prizes()
        self.running = True

    def load_stats(self):
        if os.path.exists('stats.json'):
            with open('stats.json', 'r') as f:
                return json.load(f)
        return {
            'total_games': 0,
            'total_wins': 0,
            'total_losses': 0,
            'total_time_played': 0,
            'highest_score': 0,
            'total_oranges_collected': 0
        }

    def load_past_games(self):
        if os.path.exists('past_games.json'):
            with open('past_games.json', 'r') as f:
                return json.load(f)
        return []

    def load_prizes(self):
        if os.path.exists('prizes.json'):
            with open('prizes.json', 'r') as f:
                return json.load(f)
        return []

    def calculate_totals(self):
        return {
            'total_money_earned': sum(game['money_earned'] for game in self.past_games),
            'total_levels_completed': sum(game['levels_completed'] for game in self.past_games),
            'total_difficulty': sum(game['difficulty_score'] for game in self.past_games),
            'average_score': self.stats['highest_score'] / max(self.stats['total_games'], 1),
        }

    def draw_dashboard(self):
        self.window.blit(self.background_img, (0, 0))
        title_text = self.font.render("Player Progress Dashboard", True, (255, 255, 255))
        self.window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        stats_y_start = 100
        self.draw_stat(f"Total Games: {self.stats['total_games']}", stats_y_start)
        self.draw_stat(f"Total Wins: {self.stats['total_wins']}", stats_y_start + 40)
        self.draw_stat(f"Total Losses: {self.stats['total_losses']}", stats_y_start + 80)
        self.draw_stat(f"Total Time Played: {self.format_time(self.stats['total_time_played'])}", stats_y_start + 120)
        self.draw_stat(f"Highest Score: {self.stats['highest_score']}", stats_y_start + 160)
        self.draw_stat(f"Total Oranges Collected: {self.stats['total_oranges_collected']}", stats_y_start + 200)

        totals_y_start = 350
        self.draw_stat(f"Total Money Earned: {self.totals['total_money_earned']}", totals_y_start)
        self.draw_stat(f"Total Levels Completed: {self.totals['total_levels_completed']}", totals_y_start + 40)
        self.draw_stat(f"Total Difficulty Score: {self.totals['total_difficulty']}", totals_y_start + 80)
        self.draw_stat(f"Average Score: {self.totals['average_score']:.2f}", totals_y_start + 120)

        self.draw_past_games(520)
        self.draw_prizes(680)

        pygame.draw.rect(self.window, self.button_color, self.button_rects['Menu'])
        menu_text = self.button_font.render("Menu", True, (255, 255, 255))
        self.window.blit(menu_text, (self.button_rects['Menu'].x + 15, self.button_rects['Menu'].y + 10))