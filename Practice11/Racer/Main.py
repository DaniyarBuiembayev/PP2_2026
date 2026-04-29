import pygame
import random

pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racer Extended")
clock = pygame.time.Clock()


car = pygame.image.load("images/car.png").convert_alpha()
car = pygame.transform.scale(car, (120, 150))
car_mask = pygame.mask.from_surface(car)

enemy_img = pygame.image.load("images/enemy1.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (170, 170))
enemy_mask = pygame.mask.from_surface(enemy_img)

coin_img = pygame.image.load("images/coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (50, 50))
coin_mask = pygame.mask.from_surface(coin_img)

bg = pygame.image.load("images/background.png").convert_alpha()
bg = pygame.transform.scale(bg, (800, 600))


try:
    bg_sound = pygame.mixer.Sound("backgmus/bg_sound.mp3")
    bg_sound.play(-1)
except:
    print("Нет звука")
    bg_sound = None


car_x, car_y = 335, 400
car_speed = 5


bg_y = 0
score = 0
gameplay = True


enemy_list = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 800)

enemy_speed = 5
speed_threshold = 5  


coins = []
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 1500)


font = pygame.font.SysFont("Arial", 40)
lose_label = font.render("YOU LOSE!", True, (255, 0, 0))
restart_label = font.render("RESTART", True, (255, 255, 255))
restart_rect = restart_label.get_rect(center=(400, 350))


running = True
while running:

    if gameplay:

      
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - 600))
        bg_y += 3
        if bg_y >= 600:
            bg_y = 0

        
        screen.blit(car, (car_x, car_y))


        for enemy in enemy_list[:]:
            screen.blit(enemy_img, enemy)
            enemy.y += enemy_speed

            offset = (enemy.x - car_x, enemy.y - car_y)

            
            if car_mask.overlap(enemy_mask, offset):
                gameplay = False
                if bg_sound:
                    bg_sound.stop()

           
            if enemy.y > 600:
                enemy_list.remove(enemy)
                score += 1

        
        for coin in coins[:]:
            screen.blit(coin_img, (coin['rect'].x, coin['rect'].y))
            coin['rect'].y += coin['speed']

            offset = (coin['rect'].x - car_x, coin['rect'].y - car_y)

            
            if car_mask.overlap(coin_mask, offset):
                score += coin['value']
                coins.remove(coin)

            
            elif coin['rect'].y > 600:
                coins.remove(coin)

        
        enemy_speed = 5 + (score // speed_threshold)

        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and car_x > 150:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < 525:
            car_x += car_speed
        if keys[pygame.K_UP] and car_y > 0:
            car_y -= car_speed
        if keys[pygame.K_DOWN] and car_y < 450:
            car_y += car_speed

        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
        
        screen.fill((0, 0, 0))
        screen.blit(lose_label, (300, 250))
        screen.blit(restart_label, restart_rect)

        mouse = pygame.mouse.get_pos()

        
        if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            score = 0
            car_x, car_y = 335, 400

            enemy_list.clear()
            coins.clear()

            enemy_speed = 5

            if bg_sound:
                bg_sound.play(-1)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if gameplay and event.type == enemy_timer:
            x = random.randint(150, 480)
            enemy_list.append(enemy_img.get_rect(topleft=(x, -200)))

        
        if gameplay and event.type == coin_timer:
            x = random.randint(150, 500)

            coin = {
                'rect': coin_img.get_rect(topleft=(x, -50)),
                'value': random.choice([1, 2, 3]),  
                'speed': random.randint(3, 6)
            }

            coins.append(coin)

    pygame.display.update()
    clock.tick(60)

pygame.quit()