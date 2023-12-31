# Import the pygame module
import pygame
from pygame.locals import *
import time
import config

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
# Constants for button width and height
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# game variable
wall_thickness = 20
wall_thickness1 = 60
gravity = .5
bounce_stop = 0.3
# track positions of mouse to get movement vector
mouse_trajectory = []

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 15))
        self.surf.fill('yellow')
        self.rect = self.surf.get_rect()

        # initial position of the moving rectangle to bottom-left position
        self.rect.topleft = (0, SCREEN_HEIGHT - self.rect.height- wall_thickness1/2)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0) 
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)   
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
                             

class Ball(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, radius, color, mass, retention,y_speed, x_speed, id, friction):
        super(Ball, self).__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction
        self.create_circle_surface('maroon')
        self.rect = self.surf.get_rect()

    def create_circle_surface(self, color):
        self.color = color
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

ball = Ball(50, 50, 20, 'slate gray', 100, .8, 0, 0, 1, 0.02)
# Add the ball sprite to the gball group
gball.add(ball)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
speed = [1, 1]

def draw_walls():
    left = pygame.draw.line(screen, 'brown', (0, 0), (0, SCREEN_HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, 'sea green', (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, 'Teal', (0, 0), (SCREEN_WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'pink', (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), wall_thickness1)
    wall_list = [left, right, top, bottom]
    return wall_list

# Function to draw buttons
def draw_button(x, y, width, height, text, color):
    # Create a font object
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
white = (255, 255, 255)

def print_text( x_pos, y_pos, text, color, size):
    x = x_pos
    y = y_pos
    t = text
    c = color
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(t, True, c)
    textRect = text.get_rect()
    textRect.center = (x , y)
    screen.blit(text, textRect)

# Variable to keep the main loop running
config.running = False
paused = False
restart = False
score = 0
config.highest_score = 0
running1 = True
running_main = True
score_dict = {}
# Variable to store the player's name
player_name = ""
# Variable to store the player's score
player_score = 0
# score_dict = sorted(score_dict.items(), key=lambda x:x[1])

def game_over_screen(score):
    # Create a font object to display the input message
    font = pygame.font.SysFont(None, 30)

    # Variable to store the player's name
    player_name = ""
    is_input_complete = False
    player_score = score 
    while not is_input_complete:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

                elif event.key == K_RETURN and len(player_name) > 0:
                    # Add the player name and score to the dictionary
                    score_dict[player_name] = player_score
                    is_input_complete = True
                
                elif event.key == K_BACKSPACE:
                    player_name = player_name[:-1]

                else:
                    player_name += event.unicode
        sorted_scores = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

        # Fill the screen with a color
        screen.fill((0, 0, 0))

        # Display the game over message and the player's score
        game_over_text = font.render("Game Over!!", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH //3, SCREEN_HEIGHT //2))

        score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 30))

        # Display the input message
        input_text = font.render("Input Name: {}".format(player_name), True, (255, 255, 255))
        screen.blit(input_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 60))

        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)
    running1 = True
    while running1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_KP_ENTER or event.key == K_RETURN:
                    running1 = False
                    # config.running = True
                    is_input_complete = True
                    break

        screen.fill(black)
        # Render and display the keys (player names) and values (scores) on the screen
        y_offset = 50
        font = pygame.font.SysFont(None, 30)
        top_5_scores = sorted_scores[:5]
        config.highest_score = sorted_scores[0][1]
        print_text( 50 , y_offset , 'Name : ', white, 20)
        print_text( 200 , y_offset , 'Score : ', white, 20)
        y_offset += 30

        for name, score in top_5_scores:
            name_text = font.render(name, True, white)
            score_text = font.render(str(score), True, white)
            screen.blit(name_text, (50, y_offset))
            screen.blit(score_text, (200, y_offset))
            y_offset += 30
        
        pygame.display.flip()

        clock.tick(30)
    running1 = False

def play_ground():
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
    # ball = Ball(radius, color)
    ball = Ball(50, 50, 20, 'slate gray', 100, .8, 0, 0, 1, 0.02)
    # Add the ball sprite to the gball group
    gball.add(ball)
    draw_walls()

    global paused
    global score
    score = 0 
    while config.running: 
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    game_over_screen(score)

                    config.running = False

                elif event.key == K_p:
                    paused = True
                elif event.key == K_r:
                    paused = False 
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                # game_over_screen(score)
                config.running = False
                game_over_screen(score)

        screen.fill((0, 0, 0))  # Fill the screen with black
        if not paused:
            ball.rect.x += speed[0]
            ball.rect.y += speed[1]
        if paused:
            print_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "Paused", white, 30)        
        if ball.rect.left < 0 :
            speed[0] = -speed[0]
            ball.create_circle_surface('brown')        
        if ball.rect.right > SCREEN_WIDTH:
            speed[0] = -speed[0]
            ball.create_circle_surface('sea green')
        if ball.rect.top < 0 :
            speed[1] = -speed[1]
            ball.create_circle_surface('Teal')
        if pygame.sprite.spritecollideany(player, gball) and ball.rect.y == 516:        
            speed[1] = -speed[1]
            score = score + 5 
            ball.create_circle_surface('yellow')
            # speed[1] = speed[1] + .1
            # speed[0] = speed[0] + .1
        if  ball.rect.bottom > SCREEN_HEIGHT:
            config.running = False
            game_over_screen(score)

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        walls = draw_walls()
        # screen.blit(text, textRect)
        print_text( 50 , SCREEN_HEIGHT - wall_thickness1/4, 'Score : ', black, 20)
        print_text( 100 , SCREEN_HEIGHT - wall_thickness1/4, str(score) , black, 20)

        print_text(650, SCREEN_HEIGHT - wall_thickness1/4, 'Highest Score : ', black, 20)
        print_text( 750 , SCREEN_HEIGHT - wall_thickness1/4, str(config.highest_score) , black, 20)
        screen.blit(ball.surf, ball.rect)  # Draw the circular sprite

        # Draw the player on the screen
        screen.blit(player.surf, player.rect)

        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(250)     

running_main = True
# Variables for speed increase
time_elapsed = 0
speed_increase_interval = 1
# Main loop
while running_main:
    # Create a font object
    font = pygame.font.Font(None, 36)
    for event in pygame.event.get():
        if event.type == QUIT:
            running_main = False
        elif event.type == MOUSEBUTTONDOWN: 
            x, y = event.pos 
            if 350 <= x <= 400 and 150 <= y <= 200:
                config.running = True
                play_ground()

            elif 350 <= x <= 400 and 250 <= y <= 300:
                # running = False 
                pygame.quit()  
        if time_elapsed >= speed_increase_interval:
            # Increase the speed of the ball by a fixed amount or a percentage
            speed[0] *= 1.9  # Increase the x-speed by 90% (adjust the multiplier as needed)
            speed[1] *= 1.9  # Increase the y-speed by 90% (adjust the multiplier as needed)
            time_elapsed = 0  # Reset the time_elapsed for the next speed increase    
        
    # Clear the screen
    screen.fill((255, 255, 255))
    # Draw the buttons
    draw_button(350, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Start", (46,139,87))
    draw_button(350, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Close", (250,128,114))

    pygame.display.flip()

pygame.quit()