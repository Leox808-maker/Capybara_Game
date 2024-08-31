import pygame
import sys


class LevelScreen:
    def __init__(self, window):
        self.window = window
        self.font_large = pygame.font.SysFont(None, 74)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)
        self.selected_level = 1
        self.selected_difficulty = "Normal"
        self.menu_items = ['Level 1', 'Level 2', 'Level 3', 'Difficulty: Normal', 'Settings', 'Back to Menu']
        self.current_selection = 0

    def draw_screen(self):
        self.window.fill(WHITE)
        title_text = self.font_large.render('Select Level', True, BLACK)
        self.window.blit(title_text, (WIDTH // 4, HEIGHT // 6))
        for i, item in enumerate(self.menu_items):
            color = BLACK if i != self.current_selection else ORANGE
            menu_text = self.font_medium.render(item, True, color)
            self.window.blit(menu_text, (WIDTH // 4, HEIGHT // 3 + i * 50))
        pygame.display.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_selection = (self.current_selection - 1) % len(self.menu_items)
                if event.key == pygame.K_DOWN:
                    self.current_selection = (self.current_selection + 1) % len(self.menu_items)
                if event.key == pygame.K_RETURN:
                    self.handle_selection()
                if event.key == pygame.K_ESCAPE:
                    return 'menu'

    def handle_selection(self):
        if self.menu_items[self.current_selection].startswith('Level'):
            self.selected_level = int(self.menu_items[self.current_selection].split()[1])
            return 'start_level'
        elif self.menu_items[self.current_selection].startswith('Difficulty'):
            self.cycle_difficulty()
        elif self.menu_items[self.current_selection] == 'Settings':
            return 'settings'
        elif self.menu_items[self.current_selection] == 'Back to Menu':
            return 'menu'

    def cycle_difficulty(self):
        if self.selected_difficulty == "Easy":
            self.selected_difficulty = "Normal"
        elif self.selected_difficulty == "Normal":
            self.selected_difficulty = "Hard"
        elif self.selected_difficulty == "Hard":
            self.selected_difficulty = "Easy"
        self.menu_items[3] = f'Difficulty: {self.selected_difficulty}'


def levels_screen(window):
    level_screen = LevelScreen(window)
    while True:
        level_screen.draw_screen()
        result = level_screen.handle_input()
        if result == 'menu':
            return
        elif result == 'start_level':
            start_level(level_screen.selected_level, level_screen.selected_difficulty)
        elif result == 'settings':
            settings_screen(window)


def start_level(level, difficulty):
    print(f"Starting Level {level} with {difficulty} difficulty")

def settings_screen(window):
    print("Accessing Settings")

if __name__ == '__main__':
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Capybara Collector')
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)
    levels_screen(WINDOW)