import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_RETURN

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 600
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 40)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_BG = (228, 240, 247)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.transform.scale(pygame.image.load('./images/background.png'), (WIDTH, HEIGHT))
IMAGE_PATH = "animation"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20,20)
def load_player():
    return pygame.image.load('./images/player.png').convert_alpha()

def create_enemy(): 
    enemy_size = (50, 20)
    enemy = pygame.image.load('./images/enemy.png').convert_alpha()
    enemy = pygame.transform.scale(enemy, enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus(): 
    bonus_size = (80, 100)
    bonus = pygame.image.load('./images/bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus, bonus_size)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus_size[0]), 0,  *bonus_size)
    bonus_move = [0, random.randint(1, 5)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 150)

def main_menu():
    menu_running = True
    while menu_running:
        main_display.fill(COLOR_BG)
        text = FONT.render("Press ENTER to Play", True, COLOR_BLACK)
        main_display.blit(text, (WIDTH//2 - 200, HEIGHT//2 - 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                menu_running = False
                game_loop()

def game_loop():
    global background, background_X1, background_X2, player
    player = load_player()
    player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    player_move_down = [0, 4]
    player_move_right = [4, 0]
    player_move_up = [0, -4]
    player_move_left = [-4, 0]
    background_X1 = 0
    background_X2 = background.get_width()
    background_move = 2

    bonuses = []
    enemies = []
    score = 0
    image_index = 0
    playing = True

    while playing:
        FPS.tick(120)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGE:
                player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index = (image_index + 1) % len(PLAYER_IMAGES)
        
        background_X1 -= background_move
        background_X2 -= background_move
        if background_X1 < -background.get_width():
            background_X1 = background.get_width()
        if background_X2 < -background.get_width():
            background_X2 = background.get_width()
        
        main_display.blit(background, (background_X1, 0))
        main_display.blit(background, (background_X2, 0))
        
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)
        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)
        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])
            if player_rect.colliderect(enemy[1]):
                playing = False
        
        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])
            if player_rect.colliderect(bonus[1]):
                score += 1
                bonuses.remove(bonus)
        
        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
        main_display.blit(player, player_rect)
        pygame.display.flip()

        enemies = [e for e in enemies if e[1].left > 0]
        bonuses = [b for b in bonuses if b[1].top < HEIGHT]
    
    game_over()

def game_over():
    game_over_running = True
    while game_over_running:
        main_display.fill(COLOR_BG)
        text = FONT.render("Game Over. Press 'Enter' to Start", True, COLOR_BLACK)
        main_display.blit(text, (WIDTH//2 - 320, HEIGHT//2 - 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                game_over_running = False
                main_menu()



main_menu()
