import pygame
import random
import time

pygame.init()

# ------------------ CONSTANTS ------------------
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Advanced")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# ------------------ FOOD SYSTEM ------------------

def generate_food(snake):
    """Создаёт еду с разным весом и временем жизни"""
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

        if (x, y) not in snake:
            value = random.choice([1, 2, 3])  # вес еды
            lifetime = random.randint(5, 10)  # секунд до исчезновения

            return {
                'pos': (x, y),
                'value': value,
                'spawn_time': time.time(),
                'lifetime': lifetime
            }

def get_food_color(value):
    """Цвет зависит от ценности"""
    if value == 1:
        return RED
    elif value == 2:
        return YELLOW
    else:
        return BLUE

# ------------------ GAME STATE ------------------

snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
change_to = direction

food = generate_food(snake)

score = 0
level = 1
food_eaten_this_level = 0
speed = 10

# ------------------ GAME LOOP ------------------

running = True
while running:

    # ---- EVENTS ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # ---- MOVE ----
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # ---- COLLISION ----
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        running = False

    if not running:
        break

    snake.insert(0, new_head)

    # ---- FOOD TIMER (исчезновение) ----
    current_time = time.time()
    if current_time - food['spawn_time'] > food['lifetime']:
        food = generate_food(snake)

    # ---- EAT FOOD ----
    if new_head == food['pos']:
        score += food['value']  # учитываем вес еды
        food_eaten_this_level += 1

        food = generate_food(snake)

        # ---- LEVEL UP ----
        if food_eaten_this_level >= 3:
            level += 1
            food_eaten_this_level = 0
            speed += 2

    else:
        snake.pop()

    # ---- DRAW ----
    screen.fill(BLACK)

    # snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE - 1, CELL_SIZE - 1))

    # food (цвет зависит от value)
    food_color = get_food_color(food['value'])
    pygame.draw.rect(screen, food_color, (food['pos'][0], food['pos'][1], CELL_SIZE, CELL_SIZE))

    # ---- UI ----
    stats = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(stats, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()