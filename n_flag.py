# Simple pygame program
import time
# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 600])

# time.sleep(3)

# Run until the user asks to quit

running = True

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 255, 0))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (255, 0, 0), (450, 300), 200)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()   