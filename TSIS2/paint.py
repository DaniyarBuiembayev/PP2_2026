import pygame
from datetime import datetime
import os

from tools import (
    draw_line,
    draw_rect,
    draw_circle,
    draw_square,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    flood_fill
)

# ---------- INIT ----------
pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Extended")

clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# ---------- SETTINGS ----------
drawing = False
start_pos = None
last_pos = None

color = (0, 0, 0)

brush_sizes = {
    1: 2,
    2: 5,
    3: 10
}
brush_size = brush_sizes[2]

mode = "pencil"

colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "black": (0, 0, 0)
}

# ---------- TEXT TOOL ----------
font = pygame.font.SysFont("Arial", 24)
text_input = ""
text_position = None
typing = False


# ---------- SAVE ----------
def save_canvas():
    desktop = os.path.expanduser("~/Desktop")
    filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    full_path = os.path.join(desktop, filename)

    pygame.image.save(canvas, full_path)

    print("SAVE TRIGGERED")
    print(f"Saved: {full_path}")


# ---------- MAIN LOOP ----------
running = True

while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():

        # ---------- QUIT ----------
        if event.type == pygame.QUIT:
            running = False

        # ---------- KEYBOARD ----------
        if event.type == pygame.KEYDOWN:

            # SAVE (Z = guaranteed save on Mac/Windows)
            if event.key == pygame.K_z:
                save_canvas()

            # Ctrl+S or Cmd+S
            elif event.key == pygame.K_s:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL or mods & pygame.KMOD_META:
                    save_canvas()

            # ---------- TEXT MODE ----------
            elif typing:
                if event.key == pygame.K_RETURN:
                    rendered_text = font.render(text_input, True, color)
                    canvas.blit(rendered_text, text_position)
                    typing = False
                    text_input = ""

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

            # ---------- NORMAL MODE ----------
            else:
                # TOOLS
                if event.key == pygame.K_p:
                    mode = "pencil"

                elif event.key == pygame.K_l:
                    mode = "line"

                elif event.key == pygame.K_r:
                    mode = "rect"

                elif event.key == pygame.K_c:
                    mode = "circle"

                elif event.key == pygame.K_e:
                    mode = "eraser"

                elif event.key == pygame.K_s:
                    mode = "square"

                elif event.key == pygame.K_t:
                    mode = "rtriangle"

                elif event.key == pygame.K_y:
                    mode = "etriangle"

                elif event.key == pygame.K_h:
                    mode = "rhombus"

                elif event.key == pygame.K_f:
                    mode = "fill"

                elif event.key == pygame.K_x:
                    mode = "text"

                # ---------- BRUSH SIZE ----------
                elif event.key == pygame.K_1:
                    brush_size = brush_sizes[1]

                elif event.key == pygame.K_2:
                    brush_size = brush_sizes[2]

                elif event.key == pygame.K_3:
                    brush_size = brush_sizes[3]

                # ---------- COLORS ----------
                elif event.key == pygame.K_q:
                    color = colors["red"]

                elif event.key == pygame.K_w:
                    color = colors["green"]

                elif event.key == pygame.K_a:
                    color = colors["blue"]

                elif event.key == pygame.K_d:
                    color = colors["black"]

        # ---------- MOUSE DOWN ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            last_pos = event.pos
            drawing = True

            # FILL
            if mode == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)

            # TEXT
            elif mode == "text":
                typing = True
                text_position = event.pos
                text_input = ""

        # ---------- MOUSE UP ----------
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos

                if mode == "line":
                    draw_line(canvas, color, start_pos, end_pos, brush_size)

                elif mode == "rect":
                    draw_rect(canvas, color, start_pos, end_pos, brush_size)

                elif mode == "circle":
                    draw_circle(canvas, color, start_pos, end_pos, brush_size)

                elif mode == "square":
                    draw_square(canvas, color, start_pos, end_pos, brush_size)

                elif mode == "rtriangle":
                    draw_right_triangle(canvas, color, start_pos, end_pos, brush_size)

                elif mode == "etriangle":
                    draw_equilateral_triangle(canvas, color, start_pos, end_pos, brush_size)

                elif mode == "rhombus":
                    draw_rhombus(canvas, color, start_pos, end_pos, brush_size)

            drawing = False

        # ---------- MOUSE MOTION ----------
        if event.type == pygame.MOUSEMOTION and drawing:

            # PENCIL
            if mode == "pencil":
                draw_line(canvas, color, last_pos, event.pos, brush_size)

            # ERASER
            elif mode == "eraser":
                draw_line(canvas, (255, 255, 255), last_pos, event.pos, brush_size)

            last_pos = event.pos

    # ---------- LIVE PREVIEW ----------
    if drawing and mode in [
        "line",
        "rect",
        "circle",
        "square",
        "rtriangle",
        "etriangle",
        "rhombus"
    ]:

        temp_surface = canvas.copy()
        mouse_pos = pygame.mouse.get_pos()

        if mode == "line":
            draw_line(temp_surface, color, start_pos, mouse_pos, brush_size)

        elif mode == "rect":
            draw_rect(temp_surface, color, start_pos, mouse_pos, brush_size)

        elif mode == "circle":
            draw_circle(temp_surface, color, start_pos, mouse_pos, brush_size)

        elif mode == "square":
            draw_square(temp_surface, color, start_pos, mouse_pos, brush_size)

        elif mode == "rtriangle":
            draw_right_triangle(temp_surface, color, start_pos, mouse_pos, brush_size)

        elif mode == "etriangle":
            draw_equilateral_triangle(temp_surface, color, start_pos, mouse_pos, brush_size)

        elif mode == "rhombus":
            draw_rhombus(temp_surface, color, start_pos, mouse_pos, brush_size)

        screen.blit(temp_surface, (0, 0))

    # ---------- TEXT PREVIEW ----------
    if typing:
        preview = font.render(text_input, True, color)
        screen.blit(preview, text_position)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()

# P  = Pencil (free draw)
# L  = Line
# E  = Eraser
# R  = Rectangle
# C  = Circle
# S  = Square
# T  = Right Triangle
# Y  = Equilateral Triangle
# H  = Rhombus
# F  = Flood Fill
# X  = Text Tool

# 1  = Small Brush
# 2  = Medium Brush
# 3  = Large Brush

# Q  = Red
# W  = Green
# A  = Blue
# D  = Black

# Z        = Save
# CMD + S  = Save (Mac)
# CTRL + S = Save (Windows)

# ENTER  = Confirm Text
# ESC    = Cancel Text