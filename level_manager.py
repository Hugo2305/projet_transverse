import pygame

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.max_levels = 3
        self.backgrounds = {
            1: pygame.image.load("assets/background1.png"),
            2: pygame.image.load("assets/background2.png"),
            3: pygame.image.load("assets/background3.png")
        }
        self.goal_line_x = 750

    def draw_background(self, screen):
        screen.blit(self.backgrounds[self.current_level], (0, 0))

    def check_level_complete(self, player):
        return player.rect.centerx >= self.goal_line_x

    def next_level(self):
        if self.current_level < self.max_levels:
            self.current_level += 1
            return True
        return False
