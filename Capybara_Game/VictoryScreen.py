import pygame
import random
import os


class VictoryScreen:
    def __init__(self, window, score, money, difficulty, high_scores):
        self.window = window
        self.score = score
        self.money = money
        self.difficulty = difficulty
        self.high_scores = high_scores
        self.prizes = ['Golden Capybara Statue', 'Limited Edition T-Shirt', '500 Coins', 'Extra Life', 'Exclusive Hat']
        self.prize_images = {
            'Golden Capybara Statue': pygame.image.load(os.path.join('assets', 'statue.png')),
            'Limited Edition T-Shirt': pygame.image.load(os.path.join('assets', 'tshirt.png')),
            '500 Coins': pygame.image.load(os.path.join('assets', 'coins.png')),
            'Extra Life': pygame.image.load(os.path.join('assets', 'extra_life.png')),
            'Exclusive Hat': pygame.image.load(os.path.join('assets', 'hat.png'))
        }
        self.selected_prize = random.choice(self.prizes)
        self.background_img = pygame.image.load(os.path.join('assets', 'victory_bg.png'))
        self.music = pygame.mixer.music.load(os.path.join('assets', 'victory_music.mp3'))
        pygame.mixer.music.play(-1)
        self.font = pygame.font.SysFont(None, 48)
        self.button_font = pygame.font.SysFont(None, 36)
        self.button_color = (0, 200, 0)
        self.button_hover_color = (0, 255, 0)
        self.button_rects = {
            'Menu': pygame.Rect(WIDTH // 4, HEIGHT - 100, 150, 50),
            'Restart': pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50)
        }
        self.running = True

    def draw_victory_screen(self):
        self.window.blit(self.background_img, (0, 0))
        prize_img = self.prize_images.get(self.selected_prize)
        if prize_img:
            self.window.blit(prize_img,
                             (WIDTH // 2 - prize_img.get_width() // 2, HEIGHT // 2 - prize_img.get_height() // 2))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        money_text = self.font.render(f"Money: ${self.money}", True, (255, 255, 255))
        prize_text = self.font.render(f"Prize: {self.selected_prize}", True, (255, 255, 255))
        self.window.blit(score_text,
                         (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - prize_img.get_height() // 2 - 60))
        self.window.blit(money_text,
                         (WIDTH // 2 - money_text.get_width() // 2, HEIGHT // 2 - prize_img.get_height() // 2 - 20))
        self.window.blit(prize_text,
                         (WIDTH // 2 - prize_text.get_width() // 2, HEIGHT // 2 + prize_img.get_height() // 2 + 20))
        pygame.draw.rect(self.window, self.button_color, self.button_rects['Menu'])
        pygame.draw.rect(self.window, self.button_color, self.button_rects['Restart'])
        menu_text = self.button_font.render("Menu", True, (255, 255, 255))
        restart_text = self.button_font.render("Restart", True, (255, 255, 255))
        self.window.blit(menu_text, (self.button_rects['Menu'].x + 15, self.button_rects['Menu'].y + 10))
        self.window.blit(restart_text, (self.button_rects['Restart'].x + 15, self.button_rects['Restart'].y + 10))

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
        return None

    def update_high_scores(self):
        if self.score > self.high_scores[self.difficulty]:
            self.high_scores[self.difficulty] = self.score

    def victory_loop(self):
        while self.running:
            self.draw_victory_screen()
            action = self.handle_input()
            if action == 'menu':
                pygame.mixer.music.stop()
                return 'menu'
            if action == 'restart':
                pygame.mixer.music.stop()
                return 'restart'
            pygame.display.update()

    def load_leaderboard(self):
        if os.path.exists('leaderboard.json'):
            with open('leaderboard.json', 'r') as f:
                return json.load(f)
        else:
            return {prize: 0 for prize in self.prizes}

    def update_leaderboard(self, prize):
        leaderboard = self.load_leaderboard()
        if prize in leaderboard:
            leaderboard[prize] += 1
        else:
            leaderboard[prize] = 1
        with open('leaderboard.json', 'w') as f:
            json.dump(leaderboard, f)

    def show_victory_screen(window, score, money, difficulty, high_scores):
        victory_screen = VictoryScreen(window, score, money, difficulty, high_scores)
        result = victory_screen.victory_loop()
        if result == 'menu':
            return 'menu'
        elif result == 'restart':
            return 'restart'

    if __name__ == '__main__':
        pygame.init()
        WIDTH, HEIGHT = 800, 600
        WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Capybara Collector')
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        level = 1
        difficulty = 'Normal'
        score = 100
        money = 150
        high_scores = {'Easy': 0, 'Normal': 0, 'Hard': 0}
        result = show_victory_screen(WINDOW, score, money, difficulty, high_scores)
        if result == 'menu':
            #
            pass
        elif result == 'restart':
            #
            pass

        def show_leaderboard(self):
            leaderboard = self.load_leaderboard()
            leaderboard_text = self.font.render("Leaderboard:", True, (255, 255, 255))
            self.window.blit(leaderboard_text, (WIDTH // 2 - leaderboard_text.get_width() // 2, 50))

            for i, (prize, count) in enumerate(leaderboard.items()):
                prize_text = self.font.render(f"{i + 1}. {prize}: {count}", True, (255, 255, 255))
                self.window.blit(prize_text, (WIDTH // 2 - prize_text.get_width() // 2, 100 + i * 40))

            pygame.display.update()
            pygame.time.wait(5000)