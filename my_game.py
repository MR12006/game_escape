import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 Pixel Escape HD From Marwane 🔥")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 50, 50)

# ✅ Utiliser une police compatible emojis
def draw_text(text, size, color, y):
    font_obj = pygame.font.SysFont("Segoe UI Emoji", size)
    render = font_obj.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)
    return rect

# Charger images
background = pygame.image.load(r"C:\Users\Mr1_e\Documents\Nabil_folder\Castle-Views-Best-Gaming-Wallpapers-for-Epic-Fantasy-Adventures-2.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Player sprites
player_stand = pygame.image.load(r"C:\Users\Mr1_e\Documents\Nabil_folder\p1_front.png")
player_stand = pygame.transform.scale(player_stand, (120, 120))

player_jump = pygame.image.load(r"C:\Users\Mr1_e\Documents\Nabil_folder\p1_jump.png")
player_jump = pygame.transform.scale(player_jump, (120, 120))

# Obstacle
obstacle_img = pygame.image.load(r"C:\Users\Mr1_e\Documents\Nabil_folder\slimeWalk2.png")
obstacle_img = pygame.transform.scale(obstacle_img, (120, 120))

# Sons
jump_sound = pygame.mixer.Sound(r"C:\Users\Mr1_e\Documents\Nabil_folder\686523__xupr_e3__mixkit-arcade-game-jump-coin-216.wav")
game_over_sound = pygame.mixer.Sound(r"C:\Users\Mr1_e\Documents\Nabil_folder\318371__jalastram__retro_game_sounds_sfx_195.wav")

# Joueur
player_x = 150
player_y = HEIGHT - 180
player_vel_y = 0
gravity = 1
is_jumping = False

# Obstacles
obstacle_x = WIDTH
obstacle_y = HEIGHT - 180
obstacle_speed = 15

# Score
score = 5
high_score = 0

# États
menu = True
game_over = False

# Boucle principale
clock = pygame.time.Clock()

while True:
    # MENU PRINCIPAL
    while menu:
        screen.blit(background, (0, 0))
        draw_text("🔥 Pixel Escape HD 🔥", 150, WHITE, HEIGHT // 3)
        start_button = draw_text("▶ Start", 100, RED, HEIGHT // 2)
        quit_button = draw_text("❌ Quit", 100, RED, HEIGHT // 2 + 150)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    menu = False
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # JEU
    screen.blit(background, (0, 0))

    # Déplacement joueur
    player_y += player_vel_y
    if player_y >= HEIGHT - 180:
        player_y = HEIGHT - 180
        is_jumping = False
        player_vel_y = 0
    else:
        player_vel_y += gravity

    # Obstacles
    obstacle_x -= obstacle_speed
    if obstacle_x < -120:
        obstacle_x = WIDTH
        score += 1  # Passe obstacle = +1

    # Afficher joueur (debout ou saut)
    if is_jumping:
        screen.blit(player_jump, (player_x, player_y))
    else:
        screen.blit(player_stand, (player_x, player_y))

    screen.blit(obstacle_img, (obstacle_x, obstacle_y))

    # Score & High Score
    font_score = pygame.font.SysFont("Segoe UI Emoji", 70)
    screen.blit(font_score.render(f"⭐ Score: {score}", True, WHITE), (30, 30))
    screen.blit(font_score.render(f"🏆 High Score: {high_score}", True, WHITE), (30, 120))

    # Collision
    player_rect = pygame.Rect(player_x, player_y, 120, 120)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, 120, 120)

    if player_rect.colliderect(obstacle_rect):
        score -= 1
        obstacle_x = WIDTH  # Obstacle repart
        game_over_sound.play()

    # Vérifier si score = 0
    if score <= 0:
        game_over = True
        if high_score < score:
            high_score = score

    # GAME OVER
    while game_over:
        if score > high_score:
            high_score = score
        screen.blit(background, (0, 0))
        draw_text("💀 Game Over 💀", 150, RED, HEIGHT // 3)
        draw_text(f"⭐ Score: {score}", 100, WHITE, HEIGHT // 2)
        draw_text(f"🏆 High Score: {high_score}", 80, WHITE, HEIGHT // 2 + 100)
        restart_button = draw_text("🔄 Restart", 80, WHITE, HEIGHT // 2 + 250)
        quit_button = draw_text("❌ Quit", 80, RED, HEIGHT // 2 + 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    score = 5
                    obstacle_x = WIDTH
                    game_over = False
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = -28
                is_jumping = True
                jump_sound.play()

    pygame.display.flip()
    clock.tick(60)