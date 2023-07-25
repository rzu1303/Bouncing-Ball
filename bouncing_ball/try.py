import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        super().__init__()
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

size = width, height = 800, 600

# Set up the display
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Circular Sprite Example")

# Create a circular sprite
radius = 20
color = (255, 255, 255)  # White
ball = Ball(radius, color)

speed = [1, 1]


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the position of the ball based on the speed vector
    ball.rect.x += speed[0]
    ball.rect.y += speed[1]
    # ballrect = circular_sprite.rect.move(speed)


    if ball.rect.left < 0 or ball.rect.right > width:

        speed[0] = -speed[0]

    if ball.rect.top < 0 or ball.rect.bottom > height:

        speed[1] = -speed[1]

    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(ball.surf, ball.rect)  # Draw the circular sprite
    pygame.display.flip()

# Quit pygame
pygame.quit()
