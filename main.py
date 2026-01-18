import pygame
from soldier import Soldier, Player


pygame.init()
wwid = 1280
whgt = 1020
center = (round(wwid/2), round(whgt/2))
screen = pygame.display.set_mode((wwid, whgt))
clock = pygame.time.Clock()
running = True

player = Player(10, pygame.Vector2(center))

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

    # update player rotation
    player.updateRot(mouse_pos)

    # update shooting
    if (pressed[0] and player.canShoot()):
        player.shoot(mouse_pos)

    # update screen
    screen.fill((67, 102, 63))
    
    player.move()
    player.updateAndDrawBullets(screen)
    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()