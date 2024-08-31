import pygame
import os
import json


class PrizeCollectionScreen:
    def __init__(self, window):
        self.window = window
        self.prizes = self.load_prizes()
        self.background_img = pygame.image.load(os.path.join('assets', 'prize_collection_bg.png'))
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)
        self.button_font = pygame.font.SysFont(None, 36)
        self.button_color = (50, 50, 200)
        self.button_hover_color = (100, 100, 255)
        self.button_rects = {
            'Menu': pygame.Rect(WIDTH // 4, HEIGHT - 100, 150, 50),
            'Next': pygame.Rect(WIDTH - 200, HEIGHT - 100, 150, 50),
            'Previous': pygame.Rect(50, HEIGHT - 100, 150, 50)
        }
        self.grid_spacing = 20
        self.prize_grid = self.generate_prize_grid()
        self.current_page = 0
        self.prizes_per_page = 6
        self.running = True

    def load_prizes(self):
        if os.path.exists('prizes.json'):
            with open('prizes.json', 'r') as f:
                return json.load(f)
        return []

    def generate_prize_grid(self):
        rows = 2
        cols = 3
        grid = []
        for i in range(0, len(self.prizes), cols):
            grid.append(self.prizes[i:i + cols])
        return grid

    def draw_prize_collection_screen(self):
        self.window.blit(self.background_img, (0, 0))
        title_text = self.font.render("Your Prize Collection", True, (255, 255, 255))
        self.window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
        start_y = 100
        for row_idx, row in enumerate(self.prize_grid[self.current_page:self.current_page + 1]):
            for col_idx, prize in enumerate(row):
                prize_img = pygame.image.load(os.path.join('assets', f'{prize}.png'))
                prize_x = (col_idx * (prize_img.get_width() + self.grid_spacing)) + (
                            WIDTH // 2 - (prize_img.get_width() * 3 + self.grid_spacing * 2) // 2)
                prize_y = start_y + row_idx * (prize_img.get_height() + self.grid_spacing)
                self.window.blit(prize_img, (prize_x, prize_y))
                prize_name_text = self.small_font.render(prize, True, (255, 255, 255))
                self.window.blit(prize_name_text, (
                prize_x + prize_img.get_width() // 2 - prize_name_text.get_width() // 2,
                prize_y + prize_img.get_height() + 10))

        pygame.draw.rect(self.window, self.button_color, self.button_rects['Menu'])
        pygame.draw.rect(self.window, self.button_color, self.button_rects['Next'])
        pygame.draw.rect(self.window, self.button_color, self.button_rects['Previous'])
        menu_text = self.button_font.render("Menu", True, (255, 255, 255))
        next_text = self.button_font.render("Next", True, (255, 255, 255))
        previous_text = self.button_font.render("Previous", True, (255, 255, 255))
        self.window.blit(menu_text, (self.button_rects['Menu'].x + 15, self.button_rects['Menu'].y + 10))
        self.window.blit(next_text, (self.button_rects['Next'].x + 15, self.button_rects['Next'].y + 10))
        self.window.blit(previous_text, (self.button_rects['Previous'].x + 15, self.button_rects['Previous'].y + 10))

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
                if self.button_rects['Next'].collidepoint(mouse_pos):
                    self.current_page = (self.current_page + 1) % len(self.prize_grid)
                if self.button_rects['Previous'].collidepoint(mouse_pos):
                    self.current_page = (self.current_page - 1) % len(self.prize_grid)
        return NoneD

     def prize_collection_loop(self):
            while self.running:
                self.draw_prize_collection_screen()
                action = self.handle_input()
                if action == 'menu':
                    return 'menu'
                pygame.display.update()

        def save_prizes(self, new_prize):
            self.prizes.append(new_prize)
            with open('prizes.json', 'w') as f:
                json.dump(self.prizes, f)

    def show_prize_collection_screen(window):
        prize_collection_screen = PrizeCollectionScreen(window)
        result = prize_collection_screen.prize_collection_loop()
        if result == 'menu':
            return 'menu'

    if __name__ == '__main__':
        pygame.init()
        WIDTH, HEIGHT = 800, 600
        WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Capybara Collector')
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        result = show_prize_collection_screen(WINDOW)
        if result == 'menu':
            #
            pass
