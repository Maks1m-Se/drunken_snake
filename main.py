# /// script
# dependencies = [
#  "pygame",
#  "random",
#  "math",
#  "numpy",
#  "os",
#  "asyncio",
# ]
# ///

import pygame
import random
import math
import numpy as np
import os
import asyncio

# Initialize Pygame
pygame.init()

# Load and Play Background Music
pygame.mixer.init()
# pygame.mixer.music.load("assets/music/rosie_remix.ogg")
# pygame.mixer.music.play()
# pygame.mixer.music.set_volume(.7)
rosie_music = pygame.mixer.Sound("assets/music/rosie_remix.ogg")
rosie_music.set_volume(.7)



# Load sound effects

heaven_music = pygame.mixer.Sound("assets/music/heaven.ogg")
heaven_music.set_volume(.7)

stretch_sound = pygame.mixer.Sound("assets/sounds/stretch.ogg")
stretch_sound.set_volume(.9)
grow_sound = pygame.mixer.Sound("assets/sounds/grow.ogg")
grow_sound.set_volume(1.5)
nom_sound = pygame.mixer.Sound("assets/sounds/nom.ogg")
nom_sound.set_volume(.9)
drink_sound = pygame.mixer.Sound("assets/sounds/drink.ogg")
drink_sound.set_volume(.9)
drink_long_sound = pygame.mixer.Sound("assets/sounds/drink_long.ogg")
drink_long_sound.set_volume(.9)
squeeky_sound = pygame.mixer.Sound("assets/sounds/squeeky.ogg")
squeeky_sound.set_volume(.9)


beep_sound = pygame.mixer.Sound("assets/sounds/short_beep.ogg")
go_sound = pygame.mixer.Sound("assets/sounds/go.ogg")
crash_sound = pygame.mixer.Sound("assets/sounds/crash.ogg")
honk_sound = pygame.mixer.Sound("assets/sounds/honk.ogg")
honk2_sound = pygame.mixer.Sound("assets/sounds/honk2.ogg")
burp_sound = pygame.mixer.Sound("assets/sounds/burp.ogg")
burp_long_sound = pygame.mixer.Sound("assets/sounds/burp.ogg")
beep_sound.set_volume(.5)
go_sound.set_volume(.5)
crash_sound.set_volume(.5)
honk_sound.set_volume(.7)
honk2_sound.set_volume(.7)
burp_sound.set_volume(3)
burp_long_sound.set_volume(3)
random_sounds = [honk_sound, honk2_sound, burp_sound, burp_long_sound]
last_sound_time = 5
play_beep = False

# Screen settings
HEIGHT = 720 #800
WIDTH = 1280 #int(HEIGHT+HEIGHT*1/3)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drunken Snake")
button_font = pygame.font.Font(None, 25)

# Colors
WHITE = (240, 245, 235)
LIGHTBLUE = (220, 220, 240)
LIGHTRED = (250, 211, 215)
YELLOWBLACK = (184, 178, 169)
GREEN = (36, 95, 29)
LIGHTGREEN = (66, 173, 54)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (151, 150, 148)
BG_COLOR = WHITE

# Game settings
FPS = 60
TIMER = 85  # Game length in seconds
points = 0

# Load images
item_size = 40

beer_image = pygame.image.load("assets/images/beer/beer.png")
beer_image = pygame.transform.scale(beer_image, (item_size, item_size))

big_beer_image = pygame.image.load("assets/images/beer/big_beer.png")
big_beer_image = pygame.transform.scale(big_beer_image, (item_size*2.5, item_size*2.5))

start_image = pygame.image.load("assets/images/start_screen/snake_start_3.jpg")
start_image = pygame.transform.scale(start_image, (HEIGHT, HEIGHT))

food_images = [pygame.image.load(os.path.join("assets/images/food", img)) for img in os.listdir("assets/images/food") if img.endswith(".png")]
food_images = [pygame.transform.scale(img, (item_size, item_size)) for img in food_images]
food_image1 = random.choice(food_images)
food_image2 = random.choice(food_images)
#food_image = pygame.image.load("assets/images/food/chicken-leg.png")
#food_image = pygame.transform.scale(food_image, (item_size, item_size))


# Snake properties
snake_pos = [WIDTH // 2, math.floor(HEIGHT*0.65)]
snake_body = [[WIDTH // 2, math.floor(HEIGHT*0.65)]]
snake_speed = 1.8
snake_angle = random.randint(0,359)  # Movement direction
snake_length = 50
snake_width = 10
fat_factor = 1

drunkness = 0  # Determines wobbly movement

# Food and Beer properties
food_pos1 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
food_pos2 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
beer_pos1 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
beer_pos2 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
food_spawned = True
beer_spawned = True




def display_text(text, size, color, position):
    font = pygame.font.SysFont(None, size)
    render_text = font.render(text, True, color)
    screen.blit(render_text, position)

# Pre-game sequence
pre_game_time = 18500  # 18 seconds before game starts
fade_time = 3000  # 3 seconds fade duration
countdown_time = 10000  # 10 seconds countdown

pregame_running = True
game_running = True
results_running = True



async def pregame_loop():
    global pregame_running, game_running, results_running, old_countdown_value, clock, points, display_big_beer
    print('PREGAME LOOP')

    clock = pygame.time.Clock()

    pygame.mixer.stop()
    rosie_music.play()

    TIMER = 85  # Game length in seconds
    points = 0
    BG_COLOR = WHITE
    display_big_beer = False
    
    old_countdown_value = 100

    game_start_time = pygame.time.get_ticks() + pre_game_time
    fade_start_time = pygame.time.get_ticks() + 5000  # 5 seconds after start
    countdown_start_time = fade_start_time + fade_time

    while pygame.time.get_ticks() < game_start_time and pregame_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pregame_running = False
                game_running = False
                results_running = False

        screen.fill(BG_COLOR)
        
        # Draw initial play field with snake
        # for i in range(0, snake_length):
        #     pygame.draw.circle(screen, GREEN, [WIDTH // 2  - i, math.floor(HEIGHT*0.65)], snake_width // 2)
        screen.blit(food_image1, food_pos1)
        screen.blit(food_image2, food_pos2)
        screen.blit(beer_image, beer_pos1)
        screen.blit(beer_image, beer_pos2)

        # Display HUD
        display_text(f'Points: {points}', 36, BLACK, (10, 10))
        display_text(f'{int(TIMER)}s', 36, BLACK, (10, 50))
        display_text(f'{drunkness/10}‰', 60, BLACK, (WIDTH//2-10, 10))
        #display_text(f'Speed: {snake_speed}', 20, GREY, (10, 90))
        
        elapsed = pygame.time.get_ticks()
        if elapsed < fade_start_time:
            screen.fill(GREY)
            screen.blit(start_image, (WIDTH//2-HEIGHT//2, 0))
        elif elapsed < countdown_start_time:
            fade_alpha = int(255 * (1 - (elapsed - fade_start_time) / fade_time))
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill(WHITE)
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

            # Display INFO
            display_text(f'Beer: 3 Points', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 100))
            display_text(f'Food: 1 Points', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 140))
            display_text(f'Big Beer: 7 Points', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 180))
            display_text(f'Collect as many points as possible!', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 240))
        else:
            countdown_value = max(0, 10 - (elapsed - countdown_start_time) // 1000)
            #print('countdown_value', countdown_value) #### DEBUGGING
            #print('old_countdown_value', old_countdown_value) #### DEBUGGING
            #print('play_beep', play_beep) #### DEBUGGING
            if countdown_value != old_countdown_value:
                play_beep = True
                old_countdown_value = countdown_value
            if countdown_value > 0:
                if play_beep and countdown_value < 6:
                    play_beep = False
                    beep_sound.play()
                display_text(f"{countdown_value}", 300, RED, (WIDTH//2 - 30, HEIGHT//3-100))
                
                # Display INFO
                display_text(f'Beer: 3 Points', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 100))
                display_text(f'Food: 1 Points', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 140))
                display_text(f'Big Beer: 7 Points', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 180))
                display_text(f'Collect as many points as possible!', 50, BLACK, (WIDTH//2 - 200, HEIGHT//2 + 240))
            else:
                if play_beep:
                    play_beep = False
                    go_sound.play()
                display_text("GO!", 330, RED, (WIDTH//2 - 180, HEIGHT//3-100))

        pygame.display.update()
        clock.tick(FPS)
    await asyncio.sleep(0)

async def restart_main_loop():
    global pregame_running, game_running, results_running, old_countdown_value, clock
    global snake_pos, snake_body, snake_speed, snake_angle, snake_length, snake_width, fat_factor
    global drunkness, food_pos1, food_pos2, beer_pos1, beer_pos2
    print('RESTART LOOP')

    pregame_running = True
    game_running = True
    results_running = True

    # Snake properties
    snake_pos = [WIDTH // 2, math.floor(HEIGHT*0.65)]
    snake_body = [[WIDTH // 2, math.floor(HEIGHT*0.65)]]
    snake_speed = 1.8
    snake_angle = random.randint(0,359)  # Movement direction
    snake_length = 50
    snake_width = 10
    fat_factor = 1

    drunkness = 0  # Determines wobbly movement

    # Food and Beer properties
    food_pos1 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
    food_pos2 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
    beer_pos1 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
    beer_pos2 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])

    await pregame_loop()
    await main_loop()
    await asyncio.sleep(0)

async def results_loop():
    global results_running, clock, button_font
    print('RESULTS LOOP')

    pygame.mixer.stop()
    heaven_music.play()


    while results_running:
        BG_COLOR = WHITE
        screen.fill(BG_COLOR)
        
        # Buttons
        button_restart_color = (50, 50, 150)  
        button_restart_hover_color = (70, 70, 200)  
        button_restart_text_color = (255, 255, 255)  
        buttons = [
            {"rect": pygame.Rect(WIDTH//2, HEIGHT - 100, 100, 30), "label": "RESTART", "action": restart_main_loop},
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                results_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        await button["action"]()

        # Draw buttons
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in buttons:
            rect = button["rect"]
            color = button_restart_hover_color if rect.collidepoint(mouse_x, mouse_y) else button_restart_color  
            pygame.draw.rect(screen, color, rect, border_radius=10)  
            label_surface = button_font.render(button["label"], True, button_restart_text_color)
            screen.blit(label_surface, (rect.x + 10, rect.y + 5))  

        display_text(f'GAME OVER', 150, RED, (WIDTH//5, 200))
        display_text(f'Points: {points}', 100, BLACK, (WIDTH//4, 350))
        display_text(f'{drunkness/10}‰', 45, BLACK, (WIDTH//3, 450))
        pygame.display.update()
        clock.tick(FPS)
    
    await asyncio.sleep(0)

async def main_loop():
    global game_running, results_running, BG_COLOR, drunkness, points
    global last_sound_time
    global break_snake_loop, snake_angle, snake_speed, snake_length, snake_width
    global food_pos1, food_pos2, beer_pos1, beer_pos2, big_beer_pos, display_big_beer
    global food_image1, food_image2, beer_image, big_beer_image
    print('MAIN LOOP')
    
    
    
    start_time = pygame.time.get_ticks()

    # Flags for holding mouse button
    holding_left = False
    holding_right = False

    while game_running:
        screen.fill(BG_COLOR)
        
        # Calculate time remaining
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_left = max(0, TIMER - elapsed_time)
        if time_left <= 0:
            game_running = False
        
        # display big beer on
        if int(time_left) == 70 and not display_big_beer:
            display_big_beer = True
            big_beer_pos = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
        if int(time_left) == 55 and not display_big_beer:
            display_big_beer = True
            big_beer_pos = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
        if int(time_left) == 30 and not display_big_beer:
            display_big_beer = True
            big_beer_pos = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
        if int(time_left) == 15 and not display_big_beer:
            display_big_beer = True
            big_beer_pos = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])


        # speed adjustment
        if time_left <= 72:
            snake_speed = 2
            BG_COLOR = LIGHTBLUE
        if time_left <= 44:
            snake_speed = 3
            BG_COLOR = LIGHTRED
        if time_left <= 26:
            snake_speed = 4
            BG_COLOR = YELLOWBLACK
        

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                results_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print('mouse_pos:', mouse_pos)
                if event.button == 1:  # Left mouse button
                    if mouse_pos[0] < WIDTH // 2:
                        holding_left = True  # Start turning left
                    elif mouse_pos[0] > WIDTH // 2:
                        holding_right = True  # Start turning right
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released
                    holding_left = False
                    holding_right = False

        # Continuous turning while holding mouse button
        if holding_left:
            snake_angle -= 3
        if holding_right:
            snake_angle += 3

        #key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            snake_angle -= 3  # Smooth turn left
        if keys[pygame.K_RIGHT]:
            snake_angle += 3  # Smooth turn right


    
        
        # Drunk movement effect
        if drunkness > 0:
            # direction_x += np.random.laplace(0, drunkness / 30, 1)[0]
            # direction_y += np.random.laplace(0, drunkness / 30, 1)[0]
            snake_angle += np.random.laplace(0, drunkness / 3, 1)[0]
            #direction_x += (np.random.standard_cauchy(1) * (drunkness / 50))[0] # zu stark
            #direction_y += (np.random.standard_cauchy(1) * (drunkness / 50))[0]
        
        # Calculate movement with angle
        direction_x = math.cos(math.radians(snake_angle)) * snake_speed
        direction_y = math.sin(math.radians(snake_angle)) * snake_speed
        
        
        
        # Update snake position
        snake_pos[0] += direction_x
        snake_pos[1] += direction_y
        snake_body.append(list(snake_pos))
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check for food1 collision
        if math.dist(snake_pos, food_pos1 + item_size//2) < (snake_width+item_size//2):
            food_pos1 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
            food_image1 = random.choice(food_images)  # Change food image on new spawn
            nom_sound.play()
            if random.choice([True, False]):
                grow_length = random.randint(20, 30)  # Randomly grow in length
                snake_length += grow_length
                print('grow length:', grow_length)
                stretch_sound.play()
            else:
                grow_width = random.randint(3, 5)  # Randomly grow in width
                snake_width += grow_width  # Randomly grow in width
                print('grow width:', grow_width)
                grow_sound.play()
            drunkness = max(0, drunkness - 1)  # Reduce drunkness
            points += 1
        # Check for food2 collision
        if math.dist(snake_pos, food_pos2 + item_size//2) < (snake_width+item_size//2):
            food_pos2 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
            food_image2 = random.choice(food_images)  # Change food image on new spawn
            nom_sound.play()
            if random.choice([True, False]):
                grow_length = random.randint(20, 30)  # Randomly grow in length
                snake_length += grow_length
                print('grow length:', grow_length)
                stretch_sound.play()
            else:
                grow_width = random.randint(3, 5)  # Randomly grow in width
                snake_width += grow_width  # Randomly grow in width
                print('grow width:', grow_width)
                grow_sound.play()
            drunkness = max(0, drunkness - 1)  # Reduce drunkness
            points += 1
        
        #print(food_pos)
        # Check for beer1 collision
        if math.dist(snake_pos, beer_pos1 + item_size//2) < (snake_width+item_size//2):
            beer_pos1 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
            drink_sound.play()
            drunkness += 2  # Increase drunk effect
            points += 3
        # Check for beer2 collision
        if math.dist(snake_pos, beer_pos2 + item_size//2) < (snake_width+item_size//2):
            beer_pos2 = np.array([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
            drink_sound.play()
            drunkness += 2  # Increase drunk effect
            points += 3

        # Check for big_beer collision
        if display_big_beer:
            if math.dist(snake_pos, big_beer_pos + item_size) < (snake_width+item_size):
                drink_long_sound.play()
                drunkness += 6  # Increase drunk effect
                points += 7
                display_big_beer = False

        
        # Draw food and beer using images
        screen.blit(food_image1, food_pos1)
        screen.blit(food_image2, food_pos2)
        screen.blit(beer_image, beer_pos1)
        screen.blit(beer_image, beer_pos2)
        if display_big_beer:
            screen.blit(big_beer_image, big_beer_pos)
        
        # Draw snake
        snake_head_counter = len(snake_body)
        fat_factor = 1
        for i, pos in enumerate(snake_body):
            if i % 7 == 0:
                SNAKE_COL = LIGHTGREEN
            else:
                SNAKE_COL = GREEN
            if snake_head_counter <= 2+snake_width//4:
                pygame.draw.circle(screen, GREEN, pos, 5 + snake_width//5)
            else:
                pygame.draw.circle(screen, SNAKE_COL, pos, snake_width//2 * fat_factor)
            if i < len(snake_body)//2:
                fat_factor += 0.03
            else:
                fat_factor -= 0.03
            snake_head_counter -= 1

        # check for snake body collision
        break_snake_loop = False
        for snake_segment_pos in snake_body[:-(30+snake_width//2)]:
            #pygame.draw.circle(screen, RED, snake_segment_pos, 2)
            if math.dist(snake_pos, snake_segment_pos) < snake_width:
                pygame.mixer.stop()
                crash_sound.play()
                game_running = False
                pygame.time.wait(2000)
                break_snake_loop = True
                break

        #print('snake_angle ', snake_angle)

        # check for WALL COLLISION
        if time_left != 0:
            time_wait_wall = int(30000/time_left)
        if snake_pos[0] <= 0:
            squeeky_sound.play()
            print(time_wait_wall)
            pygame.time.wait(time_wait_wall)
            snake_pos[0] = 5
            points -= 1
            if direction_y >= 0:
                snake_angle = 70
            else:
                snake_angle = -70
        if snake_pos[0] >= WIDTH:
            squeeky_sound.play()
            print(time_wait_wall)
            pygame.time.wait(time_wait_wall)
            snake_pos[0] = WIDTH-5
            points -= 1
            if direction_y >= 0:
                snake_angle = 110
            else:
                snake_angle = -110
        if snake_pos[1] <= 0:
            squeeky_sound.play()
            print(time_wait_wall)
            pygame.time.wait(time_wait_wall)
            snake_pos[1] = 5
            points -= 1
            if direction_x >= 0:
                snake_angle = 20
            else:
                snake_angle = 160
        if snake_pos[1] >= HEIGHT:
            squeeky_sound.play()
            print(time_wait_wall)
            pygame.time.wait(time_wait_wall)
            snake_pos[1] = HEIGHT-5
            points -= 1
            if direction_x >= 0:
                snake_angle = -20
            else:
                snake_angle = 200



        
        ## debugg collision
        # pygame.draw.circle(screen, RED, food_pos1 + item_size//2, 4)
        # pygame.draw.circle(screen, RED, beer_pos2 + item_size//2, 4)
        # pygame.draw.circle(screen, RED, snake_pos, 4)

        # Display HUD
        display_text(f'Points: {points}', 36, BLACK, (10, 10))
        display_text(f'{int(time_left)}s', 36, BLACK, (10, 50))
        display_text(f'{drunkness/10}‰', 60, BLACK, (WIDTH//2-10, 10))
        #display_text(f'Speed: {snake_speed}', 20, GREY, (10, 90))
        

        # Play a random sound every 10 seconds
        if pygame.time.get_ticks() - last_sound_time >= random.randint(5000, 10000):
            print('PLAY random sound')
            random.choice(random_sounds).play()
            last_sound_time = pygame.time.get_ticks()


        pygame.display.update()
        clock.tick(FPS)
    
    ## RESULTS LOOP
    await results_loop()

    await asyncio.sleep(0)


asyncio.run(pregame_loop())

asyncio.run(main_loop())



pygame.quit()