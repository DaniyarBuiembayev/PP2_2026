import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyGame Paint")
    clock = pygame.time.Clock()

    
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))

    
    drawing = False
    last_pos = None
    radius = 5
    color = (0, 0, 0)
    mode = 'brush' 
    
    
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

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: mode = 'rect'
                if event.key == pygame.K_c: mode = 'circle'
                if event.key == pygame.K_b: mode = 'brush'
                if event.key == pygame.K_e: mode = 'eraser'
                
                if event.key == pygame.K_1: color = colors['red']
                if event.key == pygame.K_2: color = colors['green']
                if event.key == pygame.K_3: color = colors['blue']
                if event.key == pygame.K_4: color = colors['black']

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                last_pos = event.pos
                start_pos = event.pos 

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    
                    curr_pos = event.pos
                    if mode == 'rect':
                        draw_rect(canvas, color, start_pos, curr_pos)
                    elif mode == 'circle':
                        draw_circle(canvas, color, start_pos, curr_pos)
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
        
        
        if drawing and mode in ['rect', 'circle']:
            
            curr_pos = pygame.mouse.get_pos()
            if mode == 'rect':
                draw_rect(screen, color, start_pos, curr_pos)
            elif mode == 'circle':
                draw_circle(screen, color, start_pos, curr_pos)

        pygame.display.flip()
        clock.tick(120)

def draw_line(surf, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surf, color, (x, y), radius)

def draw_rect(surf, color, start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    width = abs(start[0] - end[0])
    height = abs(start[1] - end[1])
    pygame.draw.rect(surf, color, (x, y, width, height), 2)

def draw_circle(surf, color, start, end):
    center = start
    radius = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
    pygame.draw.circle(surf, color, center, radius, 2)

main()
#b ,e , r ,c 1,2,3,4