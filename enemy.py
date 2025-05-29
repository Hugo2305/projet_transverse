import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.health = 100

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.health, 5))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)

    def tirer(self, joueur):
        angle = random.randint(20, 60)
        power = random.randint(30, 50)
        return angle, power
