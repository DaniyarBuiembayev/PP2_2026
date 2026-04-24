import pygame
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
running = True
clock = pygame.time.Clock()

car = pygame.image.load("images/car.png").convert_alpha()
car = pygame.transform.scale(car, (120, 150))
car_mask = pygame.mask.from_surface(car)

bg = pygame.image.load("images/background.png").convert_alpha()
bg = pygame.transform.scale(bg, (800, 600))


try:
    bg_sound = pygame.mixer.Sound("backgmus/bg_sound.mp3")
    bg_sound.play(-1)
except:
    print("Звуковой файл не найден, играем без звука")
    bg_sound = None

enemy_img = pygame.image.load("images/enemy1.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (170, 170))
enemy_mask = pygame.mask.from_surface(enemy_img)


car_x, car_y = 335, 400
car_speed = 5 
bg_y = 0
score = 0
gameplay = True

enemy_list_in_game = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 800) 


font = pygame.font.SysFont("Arial", 40)
lose_label = font.render("YOU LOSE!", True, (255, 0, 0))
restart_label = font.render("RESTART", True, (255, 255, 255))
restart_rect = restart_label.get_rect(center=(400, 350))

while running:
    if gameplay:
    
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - 600))
        bg_y += 3
        if bg_y >= 600:
            bg_y = 0

   
        screen.blit(car, (car_x, car_y))
        
      
        for el in enemy_list_in_game[:]: 
            screen.blit(enemy_img, el)
            el.y += 5 
       
            offset = (el.x - car_x, el.y - car_y)
            if car_mask.overlap(enemy_mask, offset):
                gameplay = False
                if bg_sound: bg_sound.stop()

           
            if el.y > 600:
                enemy_list_in_game.remove(el)
                score += 1

       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 150: car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < 525: car_x += car_speed
        if keys[pygame.K_UP] and car_y > 0: car_y -= car_speed
        if keys[pygame.K_DOWN] and car_y < 450: car_y += car_speed

        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
 
        screen.fill((0, 0, 0))
        screen.blit(lose_label, (315, 250))
        screen.blit(restart_label, restart_rect)
        
        mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
           
            gameplay = True
            score = 0
            car_x, car_y = 335, 400
            enemy_list_in_game.clear()
            if bg_sound: bg_sound.play(-1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if gameplay and event.type == enemy_timer:
            new_x = random.randint(150, 480) #
            enemy_list_in_game.append(enemy_img.get_rect(topleft=(new_x, -200)))

    pygame.display.update()
    clock.tick(60) #

pygame.quit()