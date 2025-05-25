import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Continuous Movement")

# Set up colors and clock
WHITE = (255, 255, 255)
RED = (255, 0, 0)
clock = pygame.time.Clock()

# Set up the square
x, y = 50, 50
width, height = 50, 50
vel = 5  # velocity

# Main loop
running = True
while running:
    clock.tick(60)  # 60 frames per second

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key state checking
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    # Fill the screen
    win.fill(WHITE)

    # Draw the square
    pygame.draw.rect(win, RED, (x, y, width, height))

    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
