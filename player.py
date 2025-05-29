import pygame

GRAVITY = 0.5
JUMP_STRENGTH = -10

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel_y = 0
        self.on_ground = True
        self.health = 100
        self.angle = 0
        self.power = 0

    def handle_input(self, keys):
        if keys[pygame.K_q]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_z] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= 550:
            self.rect.bottom = 550
            self.vel_y = 0
            self.on_ground = True

    def update(self, keys):
        self.handle_input(keys)
        self.apply_gravity()

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.health, 5))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"{int(self.angle)}° | {int(self.power)} m/s", True, (255, 255, 255))
        screen.blit(text, (self.rect.x, self.rect.y - 25))
