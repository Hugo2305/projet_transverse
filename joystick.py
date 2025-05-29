import pygame
import math

class Joystick:
    def __init__(self, base_pos):
        self.base_image = pygame.image.load("assets/joystick_base.png")
        self.knob_image = pygame.image.load("assets/joystick_knob.png")
        self.base_rect = self.base_image.get_rect(center=base_pos)
        self.knob_rect = self.knob_image.get_rect(center=base_pos)
        self.active = False
        self.angle = 0
        self.power = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.base_rect.collidepoint(event.pos):
                self.active = True
                self.update_knob(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False
            self.knob_rect.center = self.base_rect.center
            self.angle = 0
            self.power = 0
        elif event.type == pygame.MOUSEMOTION and self.active:
            self.update_knob(event.pos)

    def update_knob(self, pos):
        dx = pos[0] - self.base_rect.centerx
        dy = pos[1] - self.base_rect.centery
        dist = math.hypot(dx, dy)
        max_dist = 40
        angle_rad = math.atan2(-dy, dx)
        self.angle = math.degrees(angle_rad)
        self.power = min(dist / max_dist, 1) * 50

        if dist > max_dist:
            dx = max_dist * math.cos(angle_rad)
            dy = -max_dist * math.sin(angle_rad)

        self.knob_rect.center = (self.base_rect.centerx + dx, self.base_rect.centery + dy)

    def draw(self, screen):
        screen.blit(self.base_image, self.base_rect)
        screen.blit(self.knob_image, self.knob_rect)

    def get_angle_power(self):
        return self.angle, self.power
