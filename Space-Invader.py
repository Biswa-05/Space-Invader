import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game states
GAME_START = 0
GAME_PLAYING = 1
GAME_OVER = 2

# Player spaceship
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5

# Alien
ALIEN_WIDTH = 30
ALIEN_HEIGHT = 20
ALIEN_SPEED = 2

# Bullet
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 7


# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Load images (replace with your actual image paths)
player_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))  # Placeholder
player_image.fill(GREEN)
alien_image = pygame.Surface((ALIEN_WIDTH, ALIEN_HEIGHT))  # Placeholder
alien_image.fill(WHITE)
bullet_image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))  # Placeholder
bullet_image.fill(RED)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ALIEN_SPEED

    def update(self):
       self.rect.x += self.speed
       if self.rect.right >= WIDTH or self.rect.left <= 0:
           self.speed *= -1
           self.rect.y += ALIEN_HEIGHT # Move down slightly
       if self.rect.top > HEIGHT: # Respawn if they go off screen
           self.kill()
           # Add logic to bring in more aliens or end game

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create aliens (example - adjust as needed)
for row in range(3):
    for col in range(10):
        alien = Alien(col * (ALIEN_WIDTH + 10) + 50, row * (ALIEN_HEIGHT + 10) + 50)
        all_sprites.add(alien)
        aliens.add(alien)

# Game variables
game_state = GAME_START
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == GAME_START and event.key == pygame.K_SPACE:  # Start game
                game_state = GAME_PLAYING
            elif game_state == GAME_PLAYING and event.key == pygame.K_SPACE: # Shoot
                player.shoot()
            elif game_state == GAME_OVER and event.key == pygame.K_RETURN:  # Restart
                game_state = GAME_PLAYING
                score = 0
                aliens.empty()
                bullets.empty()
                player = Player()  # Reset the player
                all_sprites.add(player)
                for row in range(3):
                    for col in range(10):
                        alien = Alien(col * (ALIEN_WIDTH + 10) + 50, row * (ALIEN_HEIGHT + 10) + 50)
                        all_sprites.add(alien)
                        aliens.add(alien)


    if game_state == GAME_PLAYING:
        # Update sprites
        all_sprites.update()

        # Collision detection
        alien_bullet_collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for alien, bullet in alien_bullet_collisions.items():
            score += 1  # Increase score
            if len(aliens) == 0:
                game_state = GAME_OVER

        if pygame.sprite.spritecollide(player, aliens, False):
            game_state = GAME_OVER

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_state == GAME_START:
        start_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    elif game_state == GAME_OVER:
        game_over_text = font.render("Game Over! Press ENTER to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
