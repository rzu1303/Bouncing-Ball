import pygame
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

pygame.init()

screen = pygame.display.set_caption('Simple Movement')

position_x = 0
while True:
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        break

    # moves the square one pixel per cycle
    position_x += 1

    screen.fill(BLACK)

    # DRAWS THE SQUARE WITH THE INCREMENTED POSITION
    pygame.draw.rect(screen, WHITE, [position_x, 230, 20, 20])

    pygame.display.flip()
 