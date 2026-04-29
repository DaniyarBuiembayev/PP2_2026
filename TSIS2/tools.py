import pygame
import math
from collections import deque

# ---------- BASIC DRAW ----------
def draw_line(surf, color, start, end, size):
    pygame.draw.line(surf, color, start, end, size)


def draw_rect(surf, color, start, end, size):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(surf, color, (x, y, w, h), size)


def draw_circle(surf, color, start, end, size):
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    pygame.draw.circle(surf, color, start, radius, size)


def draw_square(surf, color, start, end, size):
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    x = start[0]
    y = start[1]

    if end[0] < start[0]:
        x -= side
    if end[1] < start[1]:
        y -= side

    pygame.draw.rect(surf, color, (x, y, side, side), size)


def draw_right_triangle(surf, color, start, end, size):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surf, color, points, size)


def draw_equilateral_triangle(surf, color, start, end, size):
    base_half = abs(end[0] - start[0]) // 2
    height = abs(end[1] - start[1])

    top = (start[0], start[1] - height)
    left = (start[0] - base_half, start[1])
    right = (start[0] + base_half, start[1])

    pygame.draw.polygon(surf, color, [top, left, right], size)


def draw_rhombus(surf, color, start, end, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    points = [
        (cx, start[1]),
        (end[0], cy),
        (cx, end[1]),
        (start[0], cy)
    ]

    pygame.draw.polygon(surf, color, points, size)


# ---------- FLOOD FILL ----------
def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))