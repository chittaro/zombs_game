import pygame
import time
from soldier import Player, ZombieSpawner
from utils import Textify
from audio import AudioManager

pygame.init()
wwid = 1280
whgt = 1020
center = (round(wwid/2), round(whgt/2))
screen = pygame.display.set_mode((wwid, whgt))
clock = pygame.time.Clock()
pygame.mixer.init()
audio = AudioManager()
audio.load("background", "action_background_music.mp3")
audio.load("game_over", "game_over.mp3")
audio.load("victory", "victory.mp3")
audio.play_ongoing("background")

hearts = 5
running = True

player = Player(5, pygame.Vector2(center), audio)

zombieSpawner = ZombieSpawner(wwid, whgt, audio)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    
    # update player direction
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.updateSpeed((1, 0))
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.updateSpeed((0, 1))
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.updateSpeed((-1, 0))
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.updateSpeed((0, -1))

    # update shooting
    if (pressed[0] and player.canShoot()):
        player.shoot(mouse_pos)

    # update enemies
    zombieSpawner.spawn()
    zombieSpawner.playerCollisions(player)
    zombieSpawner.shotCollisions(player)
    zombieSpawner.update(player)

    # update player
    player.updateRot(mouse_pos)
    player.move()


    # update screen
    screen.fill((67, 102, 63))

    zombieSpawner.draw(screen)
    player.updateAndDrawBullets(screen)
    player.draw(screen)

    Textify(f"Lives: {player.hearts}", 40, wwid/2, 40, screen)
    Textify(f"Hits: {player.kills}", 40, wwid/2, 80, screen)

    if player.hearts <= 0:
        running = False
        Textify("GAME OVER", 100, wwid/2, whgt/2, screen)
        pygame.display.flip()
        audio.play("game_over")
        time.sleep(3)

    elif player.victory == True:
        running = False
        Textify("YOU WIN", 100, wwid/2, whgt/2, screen)
        pygame.display.flip()
        audio.play("victory")
        time.sleep(3) 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()