import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Load and Play Background Music
pygame.mixer.init()
pygame.mixer.music.load("assets/music/rosie_remix.mp3")
pygame.mixer.music.play(-1)  # Loop music indefinitely
pygame.mixer.music.set_volume(.5)

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DrunkSnake")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game settings
FPS = 60
TIMER = 100  # Game length in seconds

# Snake properties
snake_pos = [WIDTH // 2, HEIGHT // 2]
snake_body = [[WIDTH // 2, HEIGHT // 2]]
snake_speed = 1.5
snake_angle = 0  # Movement direction
snake_length = 10
snake_width = 10

drunkness = 0  # Determines wobbly movement

# Food and Beer properties
food_pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
beer_pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
food_spawned = True
beer_spawned = True

# Timer
start_time = pygame.time.get_ticks()

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Calculate time remaining
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, TIMER - elapsed_time)
    if time_left <= 0:
        running = False
    
    # Event handling
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_angle -= 3  # Smooth turn left
    if keys[pygame.K_RIGHT]:
        snake_angle += 3  # Smooth turn right

    
    # Calculate movement with angle
    direction_x = math.cos(math.radians(snake_angle)) * snake_speed
    direction_y = math.sin(math.radians(snake_angle)) * snake_speed
    
    # Drunk movement effect
    if drunkness > 0:
        direction_x += random.uniform(-drunkness / 10, drunkness / 10)
        direction_y += random.uniform(-drunkness / 10, drunkness / 10)
    
    # Update snake position
    snake_pos[0] += direction_x
    snake_pos[1] += direction_y
    snake_body.append(list(snake_pos))
    if len(snake_body) > snake_length:
        del snake_body[0]
    
    # Check for food collision
    if math.dist(snake_pos, food_pos) < 15:
        food_pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
        snake_length += random.choice([2, 4])  # Randomly grow in length
        snake_width += random.choice([0, 2])  # Randomly grow in width
        drunkness = max(0, drunkness - 1)  # Reduce drunkness
    
    # Check for beer collision
    if math.dist(snake_pos, beer_pos) < 15:
        beer_pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
        drunkness += 1  # Increase drunk effect
    
    # Draw food and beer
    pygame.draw.circle(screen, GREEN, food_pos, 8)
    pygame.draw.circle(screen, BROWN, beer_pos, 10)
    
    # Draw snake (grows in width randomly)
    for i, pos in enumerate(snake_body):
        pygame.draw.circle(screen, YELLOW, pos, snake_width // 2)
    
    # Display timer
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f'Time Left: {int(time_left)}s', True, RED)
    screen.blit(timer_text, (10, 10))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
