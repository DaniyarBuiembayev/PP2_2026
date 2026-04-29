import pygame
import json
import sys

from game import run_game
from db import init_db, get_top_scores

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake TSIS 4")

font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
GRAY = (80,80,80)

# ---------------- SETTINGS ----------------
def load_settings():
    default_settings = {
        "snake_color": [0, 255, 0],
        "grid": True,
        "sound": True
    }

    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)

        # Добавляем отсутствующие ключи
        for key, value in default_settings.items():
            if key not in settings:
                settings[key] = value

        return settings

    except:
        return default_settings

def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)

# ---------------- DRAW BUTTON ----------------
def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + 20, y + 10))

# ---------------- USERNAME INPUT ----------------
def username_screen():
    username = ""

    while True:
        screen.fill(BLACK)

        title = font.render("Enter Username:", True, WHITE)
        name_text = font.render(username, True, GREEN)

        screen.blit(title, (200, 120))
        screen.blit(name_text, (200, 180))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 15:
                        username += event.unicode

# ---------------- LEADERBOARD SCREEN ----------------
def leaderboard_screen():
    scores = get_top_scores()

    while True:
        screen.fill(BLACK)

        title = font.render("TOP 10 LEADERBOARD", True, GREEN)
        screen.blit(title, (150, 20))

        y = 80

        for i, row in enumerate(scores):
            username, score, level, date = row
            text = small_font.render(
                f"{i+1}. {username} | Score: {score} | Lvl: {level}",
                True,
                WHITE
            )
            screen.blit(text, (50, y))
            y += 28

        draw_button("Back", 250, 340, 100, 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if 250 <= mx <= 350 and 340 <= my <= 380:
                    return

# ---------------- SETTINGS SCREEN ----------------
def settings_screen(settings):
    while True:
        screen.fill(BLACK)

        title = font.render("SETTINGS", True, GREEN)
        screen.blit(title, (230, 30))

        # Текущие настройки
        grid_text = small_font.render(f"Grid: {settings['grid']}", True, WHITE)
        sound_text = small_font.render(f"Sound: {settings['sound']}", True, WHITE)

        screen.blit(grid_text, (220, 90))
        screen.blit(sound_text, (220, 130))

        # Кнопки grid / sound
        draw_button("Toggle Grid", 200, 170, 200, 40)
        draw_button("Toggle Sound", 200, 220, 200, 40)

        # ---------- COLOR PICKER ----------
        color_title = small_font.render("Snake Color:", True, WHITE)
        screen.blit(color_title, (230, 280))

        # Зеленый
        pygame.draw.rect(screen, (0,255,0), (150, 320, 50, 50))

        # Синий
        pygame.draw.rect(screen, (0,150,255), (275, 320, 50, 50))

        # Красный
        pygame.draw.rect(screen, (255,0,0), (400, 320, 50, 50))

        # Save
        draw_button("Save & Back", 200, 385, 200, 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Toggle Grid
                if 200 <= mx <= 400 and 170 <= my <= 210:
                    settings["grid"] = not settings["grid"]

                # Toggle Sound
                elif 200 <= mx <= 400 and 220 <= my <= 260:
                    settings["sound"] = not settings["sound"]

                # GREEN
                elif 150 <= mx <= 200 and 320 <= my <= 370:
                    settings["snake_color"] = [0,255,0]

                # BLUE
                elif 275 <= mx <= 325 and 320 <= my <= 370:
                    settings["snake_color"] = [0,150,255]

                # RED
                elif 400 <= mx <= 450 and 320 <= my <= 370:
                    settings["snake_color"] = [255,0,0]

                # Save & Back
                elif 200 <= mx <= 400 and 385 <= my <= 425:
                    save_settings(settings)
                    return settings

# ---------------- MAIN MENU ----------------
def main_menu():
    init_db()
    settings = load_settings()

    while True:
        screen.fill(BLACK)

        title = font.render("SNAKE ADVANCED", True, GREEN)
        screen.blit(title, (190, 50))

        draw_button("Play", 220, 130, 160, 40)
        draw_button("Leaderboard", 220, 190, 160, 40)
        draw_button("Settings", 220, 250, 160, 40)
        draw_button("Quit", 220, 310, 160, 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if 220 <= mx <= 380:
                    if 130 <= my <= 170:
                        username = username_screen()
                        run_game(username, settings)

                    elif 190 <= my <= 230:
                        leaderboard_screen()

                    elif 250 <= my <= 290:
                        settings = settings_screen(settings)

                    elif 310 <= my <= 350:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main_menu()