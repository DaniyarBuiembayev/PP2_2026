import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Leveler")
clock = pygame.time.Clock()
# Load font ONCE outside the loop
font = pygame.font.SysFont("Arial", 24)

def generate_food(snake):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

# Game State
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
change_to = direction
food = generate_food(snake)
score = 0
level = 1
food_eaten_this_level = 0
speed = 10

running = True
while running:
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
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Collision: Walls or Self
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        running = False

    if not running: break

    snake.insert(0, new_head)

    # Eating Food
    if new_head == food:
        score += 1
        food_eaten_this_level += 1
        food = generate_food(snake)
        # Level Up Logic
        if food_eaten_this_level >= 3:
            level += 1
            food_eaten_this_level = 0
            speed += 2
    else:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE - 1, CELL_SIZE - 1))

    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Display Stats
    stats_surface = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(stats_surface, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()