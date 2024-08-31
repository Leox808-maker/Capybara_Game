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

    def draw_stat(self, text, y):
        stat_text = self.small_font.render(text, True, (255, 255, 255))
        self.window.blit(stat_text, (WIDTH // 2 - stat_text.get_width() // 2, y))

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours}h {minutes}m {seconds}s"

    def draw_past_games(self, start_y):
        past_games_title = self.font.render("Past Game Stats", True, (255, 255, 255))
        self.window.blit(past_games_title, (WIDTH // 2 - past_games_title.get_width() // 2, start_y))
        for i, game in enumerate(self.past_games[-5:]):
            game_text = self.small_font.render(
                f"Game {len(self.past_games) - i}: Score={game['score']}, Money={game['money_earned']}, Levels={game['levels_completed']}",
                True, (255, 255, 255)
            )
            self.window.blit(game_text, (WIDTH // 2 - game_text.get_width() // 2, start_y + 40 + i * 30))

    def draw_prizes(self, start_y):
        prizes_title = self.font.render("Collected Prizes", True, (255, 255, 255))
        self.window.blit(prizes_title, (WIDTH // 2 - prizes_title.get_width() // 2, start_y))
        for i, prize in enumerate(self.prizes[-5:]):
            prize_text = self.small_font.render(f"{prize}", True, (255, 255, 255))
            self.window.blit(prize_text, (WIDTH // 2 - prize_text.get_width() // 2, start_y + 40 + i * 30))

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
        return None

    def dashboard_loop(self):
        while self.running:
            self.draw_dashboard()
            action = self.handle_input()
            if action == 'menu':
                return 'menu'
            pygame.display.update()


def show_progress_dashboard(window):
    progress_dashboard = ProgressDashboard(window)
    result = progress_dashboard.dashboard_loop()
    if result == 'menu':
        return 'menu'


if __name__ == '__main__':
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Capybara Collector')
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    result = show_progress_dashboard(WINDOW)
    if result == 'menu':
        #
        pass