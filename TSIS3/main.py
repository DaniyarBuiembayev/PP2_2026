import pygame
from persistence import load_settings, add_score
from ui import main_menu, username_screen, settings_screen, leaderboard_screen, game_over_screen
from racer import RacerGame, WIDTH, HEIGHT

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/sound.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer — TSIS 3")


coin_img  = pygame.image.load("assets/coin.png")
coin_img  = pygame.transform.scale(coin_img, (30, 30))

racer_img = pygame.image.load("assets/space_racer.png")
racer_img = pygame.transform.scale(racer_img, (50, 70))

enemy_img = pygame.image.load("assets/Enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 70))

street_img = pygame.image.load("assets/AnimatedStreet.png")



settings = load_settings()
username = "Player"

if not settings.get("sound", True):
    pygame.mixer.music.pause()


while True:
    action = main_menu(screen, WIDTH, HEIGHT)

    if action == "quit":
        break

    elif action == "leaderboard":
        leaderboard_screen(screen, WIDTH, HEIGHT)

    elif action == "settings":
        settings = settings_screen(screen, WIDTH, HEIGHT, settings)

    elif action == "play":
        username = username_screen(screen, WIDTH, HEIGHT)

        while True:
            game = RacerGame(screen, username, settings, racer_img, coin_img, street_img, enemy_img)
            score, distance, coins = game.run()
            add_score(username, score, distance)

            result = game_over_screen(screen, WIDTH, HEIGHT, score, distance, coins)

            if result == "retry":
                continue
            else:
                break

pygame.quit()