import pygame
from player import Player
from enemy import Enemy
from joystick import Joystick
from physics import get_trajectory_points
from level_manager import LevelManager
from chifoumi import run_chifoumi
from utils import detect_collision

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def afficher_menu():
    font = pygame.font.SysFont(None, 60)
    btn_font = pygame.font.SysFont(None, 40)
    play_rect = pygame.Rect(300, 350, 200, 60)

    while True:
        screen.fill((20, 20, 30))
        titre = font.render("🏹 BOWMASTER DUEL", True, (255, 255, 255))
        screen.blit(titre, (200, 150))
        pygame.draw.rect(screen, (50, 150, 255), play_rect)
        play_txt = btn_font.render("JOUER", True, (255, 255, 255))
        screen.blit(play_txt, (play_rect.x + 50, play_rect.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and play_rect.collidepoint(event.pos):
                return

        pygame.display.flip()
        clock.tick(60)

afficher_menu()
starter = run_chifoumi(screen)
tour_actuel = starter if starter in ["player", "enemy"] else "player"

joueur = Player(100, 550)
ennemi = Enemy(700, 550)
joystick = Joystick((100, 500))
level = LevelManager()
projectile_points = []
frame_tir = 0
running = True

while running:
    screen.fill((50, 50, 100))
    level.draw_background(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if tour_actuel == "player":
            joystick.handle_event(event)
        if event.type == pygame.KEYDOWN and tour_actuel == "player":
            if event.key == pygame.K_SPACE:
                joueur.angle, joueur.power = joystick.get_angle_power()
                projectile_points = get_trajectory_points(joueur.rect.centerx, joueur.rect.centery, joueur.angle, joueur.power)
                if detect_collision(projectile_points, ennemi.rect):
                    ennemi.health -= 20
                tour_actuel = "enemy"
                frame_tir = 0

    keys = pygame.key.get_pressed()
    if tour_actuel == "player":
        joueur.update(keys)
    else:
        joueur.apply_gravity()
        if frame_tir == 0:
            angle, power = ennemi.tirer(joueur)
            projectile_points = get_trajectory_points(ennemi.rect.centerx, ennemi.rect.centery, angle, power)
            if detect_collision(projectile_points, joueur.rect):
                joueur.health -= 20
        frame_tir += 1
        if frame_tir > 100:
            tour_actuel = "player"
            projectile_points = []

    joueur.draw(screen)
    ennemi.draw(screen)
    if tour_actuel == "player":
        joystick.draw(screen)
    for pt in projectile_points:
        pygame.draw.circle(screen, (255, 0, 0), (int(pt[0]), int(pt[1])), 3)

    if joueur.health <= 0 or ennemi.health <= 0:
        running = False

    if tour_actuel == "player" and level.check_level_complete(joueur) and ennemi.health <= 0:
        if level.next_level():
            joueur.rect.midbottom = (100, 550)
            ennemi.rect.midbottom = (700, 550)
            ennemi.health = 100
            joueur.health = 100
            projectile_points = []
            tour_actuel = "player"
        else:
            screen.fill((0, 0, 0))
            text = pygame.font.SysFont(None, 60).render("🎉 Tu as fini le jeu !", True, (255, 255, 255))
            screen.blit(text, (220, 280))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    pygame.display.flip()
    clock.tick(60)
