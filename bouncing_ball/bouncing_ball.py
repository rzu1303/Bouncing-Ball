# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# game variable
wall_thickness = 10


# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 15))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        # initial position of the moving rectangle to bottom-left position
        self.rect.topleft = (0, SCREEN_HEIGHT - self.rect.height)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0) 
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)   

        # screen.blit(self.surf, self.rect)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
                             

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        super(Ball, self).__init__()
        self.radius = radius
        self.color = color
        self.create_circle_surface()
        self.rect = self.surf.get_rect()


    def create_circle_surface(self):
        diameter = self.radius * 2
        self.surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.radius, self.radius), self.radius)

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold ball sprites and all sprites
# - all_sprites is used for rendering
gball = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Create a circular sprite
radius = 10
color = (255, 255, 255)  # White
ball = Ball(radius, color)
# Add the ball sprite to the gball group
gball.add(ball)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
speed = [1, 1]

def draw_walls():
    left = pygame.draw.line(screen, (255, 255, 255), (0, 0), (0, SCREEN_HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, 'white', (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0, 0), (SCREEN_WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), wall_thickness)
    wall_list = [left, right, top, bottom]
    return wall_list

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue

    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
    # Update the position of the ball based on the speed vector
    ball.rect.x += speed[0]
    ball.rect.y += speed[1]

    if ball.rect.left < 0 or ball.rect.right > SCREEN_WIDTH:
        speed[0] = -speed[0]

    # if ball.rect.top < 0 or ball.rect.bottom > SCREEN_HEIGHT:
    if ball.rect.top < 0 :
        speed[1] = -speed[1]
    if pygame.sprite.spritecollideany(player, gball):
        speed[1] = -speed[1]

    if  ball.rect.bottom > SCREEN_HEIGHT:
        running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # # Fill the screen with black
    # screen.fill((0, 0, 0))

    screen.fill((0, 0, 0))  # Fill the screen with black
    walls = draw_walls()
    screen.blit(ball.surf, ball.rect)  # Draw the circular sprite

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)


    # Update the display
    pygame.display.flip()
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(250) 