import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyGame Paint Extended")
    clock = pygame.time.Clock()

   
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))

    drawing = False
    last_pos = None
    start_pos = None

    radius = 5
    color = (0, 0, 0)


    mode = 'brush'  
    # brush, rect, circle, eraser, square, rtriangle, etriangle, rhombus

    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0)
    }

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            # -------- KEYBOARD --------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: mode = 'brush'
                if event.key == pygame.K_r: mode = 'rect'
                if event.key == pygame.K_c: mode = 'circle'
                if event.key == pygame.K_e: mode = 'eraser'

                
                if event.key == pygame.K_s: mode = 'square'
                if event.key == pygame.K_t: mode = 'rtriangle'
                if event.key == pygame.K_y: mode = 'etriangle'
                if event.key == pygame.K_h: mode = 'rhombus'

               
                if event.key == pygame.K_1: color = colors['red']
                if event.key == pygame.K_2: color = colors['green']
                if event.key == pygame.K_3: color = colors['blue']
                if event.key == pygame.K_4: color = colors['black']

            # -------- MOUSE --------
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                last_pos = event.pos
                start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = event.pos

                    
                    if mode == 'rect':
                        draw_rect(canvas, color, start_pos, end_pos)
                    elif mode == 'circle':
                        draw_circle(canvas, color, start_pos, end_pos)
                    elif mode == 'square':
                        draw_square(canvas, color, start_pos, end_pos)
                    elif mode == 'rtriangle':
                        draw_right_triangle(canvas, color, start_pos, end_pos)
                    elif mode == 'etriangle':
                        draw_equilateral_triangle(canvas, color, start_pos, end_pos)
                    elif mode == 'rhombus':
                        draw_rhombus(canvas, color, start_pos, end_pos)

                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'brush':
                        draw_line(canvas, color, last_pos, event.pos, radius)
                    elif mode == 'eraser':
                        draw_line(canvas, (255, 255, 255), last_pos, event.pos, radius * 2)

                    last_pos = event.pos

        
        screen.fill((200, 200, 200))
        screen.blit(canvas, (0, 0))

        
        if drawing and mode not in ['brush', 'eraser']:
            end_pos = pygame.mouse.get_pos()

            if mode == 'rect':
                draw_rect(screen, color, start_pos, end_pos)
            elif mode == 'circle':
                draw_circle(screen, color, start_pos, end_pos)
            elif mode == 'square':
                draw_square(screen, color, start_pos, end_pos)
            elif mode == 'rtriangle':
                draw_right_triangle(screen, color, start_pos, end_pos)
            elif mode == 'etriangle':
                draw_equilateral_triangle(screen, color, start_pos, end_pos)
            elif mode == 'rhombus':
                draw_rhombus(screen, color, start_pos, end_pos)

        pygame.display.flip()
        clock.tick(120)

# ---------- BASIC DRAW ----------

def draw_line(surf, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    for i in range(distance):
        x = int(start[0] + i / distance * dx)
        y = int(start[1] + i / distance * dy)
        pygame.draw.circle(surf, color, (x, y), radius)

def draw_rect(surf, color, start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(surf, color, (x, y, w, h), 2)

def draw_circle(surf, color, start, end):
    radius = int(math.hypot(start[0]-end[0], start[1]-end[1]))
    pygame.draw.circle(surf, color, start, radius, 2)



def draw_square(surf, color, start, end):
    size = min(abs(start[0]-end[0]), abs(start[1]-end[1]))
    x = start[0]
    y = start[1]
    pygame.draw.rect(surf, color, (x, y, size, size), 2)

def draw_right_triangle(surf, color, start, end):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surf, color, points, 2)

def draw_equilateral_triangle(surf, color, start, end):
    
    cx = (start[0] + end[0]) // 2
    top = (cx, start[1])
    left = start
    right = end
    pygame.draw.polygon(surf, color, [top, left, right], 2)

def draw_rhombus(surf, color, start, end):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    points = [
        (cx, start[1]),
        (end[0], cy),
        (cx, end[1]),
        (start[0], cy)
    ]
    pygame.draw.polygon(surf, color, points, 2)

# ---------- RUN ----------
#b ,  e , r , c , s ,t , y , n ,1 ,2 ,3 ,4 
main()