import pygame
import random
import time

from db import save_game, get_personal_best

# ---------------- CONSTANTS ----------------
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,150,255)
BLACK = (0,0,0)
DARK_RED = (139,0,0)
PURPLE = (180,0,255)

# ---------------- FOOD ----------------
def generate_food(snake, obstacles):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE) * CELL_SIZE

        if (x,y) not in snake and (x,y) not in obstacles:
            return {
                "pos": (x,y),
                "value": random.choice([1,2,3]),
                "spawn_time": time.time(),
                "lifetime": random.randint(5,10)
            }

# ---------------- POISON ----------------
def generate_poison(snake, obstacles, food_pos):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE) * CELL_SIZE

        if (x,y) not in snake and (x,y) not in obstacles and (x,y) != food_pos:
            return (x,y)

# ---------------- POWERUPS ----------------
def generate_powerup(snake, obstacles, food_pos, poison_pos):
    types = ["speed", "slow", "shield"]

    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE) * CELL_SIZE

        if (x,y) not in snake and (x,y) not in obstacles and (x,y) != food_pos and (x,y) != poison_pos:
            return {
                "pos": (x,y),
                "type": random.choice(types),
                "spawn_time": pygame.time.get_ticks()
            }

# ---------------- OBSTACLES ----------------
def generate_obstacles(level, snake):
    obstacles = []

    if level < 3:
        return obstacles

    count = level + 2

    while len(obstacles) < count:
        x = random.randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE) * CELL_SIZE

        # Не рядом с головой
        if abs(x - snake[0][0]) > CELL_SIZE*3 and abs(y - snake[0][1]) > CELL_SIZE*3:
            if (x,y) not in snake and (x,y) not in obstacles:
                obstacles.append((x,y))

    return obstacles

# ---------------- COLORS ----------------
def get_food_color(value):
    if value == 1:
        return RED
    elif value == 2:
        return YELLOW
    return BLUE

def get_powerup_color(power_type):
    if power_type == "speed":
        return PURPLE
    elif power_type == "slow":
        return BLUE
    return WHITE

# ---------------- GAME OVER ----------------
def game_over_screen(screen, font, score, level, best_score):
    while True:
        screen.fill(BLACK)

        over = font.render("GAME OVER", True, RED)
        stats = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        best = font.render(f"Personal Best: {best_score}", True, YELLOW)
        retry = font.render("Press R to Retry or Q to Quit", True, GREEN)

        screen.blit(over, (220, 100))
        screen.blit(stats, (170, 160))
        screen.blit(best, (180, 210))
        screen.blit(retry, (120, 280))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False

# ---------------- MAIN GAME ----------------
def run_game(username, settings):

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Advanced")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    while True:

        # ---------- RESET ----------
        snake = [(100,100), (80,100), (60,100)]
        direction = (CELL_SIZE,0)
        change_to = direction

        score = 0
        level = 1
        speed = 10
        food_eaten = 0

        shield_active = False
        speed_boost_end = 0
        slow_end = 0

        obstacles = generate_obstacles(level, snake)

        food = generate_food(snake, obstacles)
        poison = generate_poison(snake, obstacles, food["pos"])

        powerup = None
        powerup_timer = pygame.time.get_ticks()

        personal_best = get_personal_best(username)

        running = True

        # ---------- LOOP ----------
        while running:

            current_ticks = pygame.time.get_ticks()

            # Spawn power-up каждые 10 сек
            if not powerup and current_ticks - powerup_timer > 10000:
                powerup = generate_powerup(snake, obstacles, food["pos"], poison)
                powerup_timer = current_ticks

            # Удаление power-up через 8 сек
            if powerup and current_ticks - powerup["spawn_time"] > 8000:
                powerup = None

            # Эффекты
            current_speed = speed

            if current_ticks < speed_boost_end:
                current_speed += 5

            if current_ticks < slow_end:
                current_speed = max(5, current_speed - 4)

            # ---------- EVENTS ----------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                        change_to = (0, -CELL_SIZE)

                    elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                        change_to = (0, CELL_SIZE)

                    elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                        change_to = (-CELL_SIZE, 0)

                    elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                        change_to = (CELL_SIZE, 0)

            direction = change_to

            # ---------- MOVE ----------
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # ---------- COLLISION ----------
            collision = (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake or
                new_head in obstacles
            )

            if collision:
                if shield_active:
                    shield_active = False
                    continue
                else:
                    running = False
                    break

            snake.insert(0, new_head)

            # ---------- FOOD EXPIRE ----------
            if time.time() - food["spawn_time"] > food["lifetime"]:
                food = generate_food(snake, obstacles)

            # ---------- EAT NORMAL FOOD ----------
            if new_head == food["pos"]:
                score += food["value"]
                food_eaten += 1

                food = generate_food(snake, obstacles)
                poison = generate_poison(snake, obstacles, food["pos"])

                if food_eaten >= 3:
                    level += 1
                    speed += 2
                    food_eaten = 0
                    obstacles = generate_obstacles(level, snake)

            # ---------- EAT POISON ----------
            elif new_head == poison:
                if len(snake) <= 2:
                    running = False
                    break

                snake.pop()
                snake.pop()

                poison = generate_poison(snake, obstacles, food["pos"])

            # ---------- EAT POWERUP ----------
            elif powerup and new_head == powerup["pos"]:

                if powerup["type"] == "speed":
                    speed_boost_end = current_ticks + 5000

                elif powerup["type"] == "slow":
                    slow_end = current_ticks + 5000

                elif powerup["type"] == "shield":
                    shield_active = True

                powerup = None

            else:
                snake.pop()

            # ---------- DRAW ----------
            screen.fill(BLACK)

            # Grid
            if settings["grid"]:
                for x in range(0, WIDTH, CELL_SIZE):
                    pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
                for y in range(0, HEIGHT, CELL_SIZE):
                    pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))

            # Snake
            for segment in snake:
                pygame.draw.rect(
                    screen,
                    tuple(settings["snake_color"]),
                    (segment[0], segment[1], CELL_SIZE-1, CELL_SIZE-1)
                )

            # Food
            pygame.draw.rect(screen, get_food_color(food["value"]),
                             (food["pos"][0], food["pos"][1], CELL_SIZE, CELL_SIZE))

            # Poison
            pygame.draw.rect(screen, DARK_RED,
                             (poison[0], poison[1], CELL_SIZE, CELL_SIZE))

            # Obstacles
            for block in obstacles:
                pygame.draw.rect(screen, WHITE,
                                 (block[0], block[1], CELL_SIZE, CELL_SIZE))

            # Power-up
            if powerup:
                pygame.draw.rect(screen, get_powerup_color(powerup["type"]),
                                 (powerup["pos"][0], powerup["pos"][1], CELL_SIZE, CELL_SIZE))

            # UI
            stats = font.render(
                f"{username} | Score: {score} | Level: {level} | Best: {personal_best}",
                True,
                WHITE
            )

            screen.blit(stats, (10,10))

            if shield_active:
                shield_text = font.render("SHIELD ACTIVE", True, YELLOW)
                screen.blit(shield_text, (10,40))

            pygame.display.flip()
            clock.tick(current_speed)

        # ---------- SAVE ----------
        save_game(username, score, level)

        if not game_over_screen(screen, font, score, level, max(score, personal_best)):
            break