import pygame
import random

CHOICES = ["rock", "paper", "scissors"]

def load_chifoumi_images():
    return {
        "rock": pygame.image.load("assets/rock.png"),
        "paper": pygame.image.load("assets/paper.png"),
        "scissors": pygame.image.load("assets/scissors.png"),
    }

def random_chifoumi():
    return random.choice(CHOICES)

def determine_winner(player_choice, enemy_choice):
    if player_choice == enemy_choice:
        return "draw"
    if (player_choice == "rock" and enemy_choice == "scissors") or \
       (player_choice == "paper" and enemy_choice == "rock") or \
       (player_choice == "scissors" and enemy_choice == "paper"):
        return "player"
    return "enemy"

def run_chifoumi(screen):
    images = load_chifoumi_images()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    player_choice = random_chifoumi()
    enemy_choice = random_chifoumi()
    winner = determine_winner(player_choice, enemy_choice)

    timer = 0
    done = False

    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(images[player_choice], (200, 200))
        screen.blit(images[enemy_choice], (500, 200))

        pygame.draw.rect(screen, (0, 255, 0), (200, 200, 100, 100), 3)
        pygame.draw.rect(screen, (255, 0, 0), (500, 200, 100, 100), 3)

        text = font.render(f"{'Égalité' if winner == 'draw' else 'Joueur' if winner == 'player' else 'Ennemi'} commence !", True, (255, 255, 255))
        screen.blit(text, (250, 100))

        pygame.display.flip()
        clock.tick(60)

        timer += 1
        if timer > 180:
            done = True

    return winner
