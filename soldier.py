import math
import pygame
import numpy as np
import time

FRICTION = 0.8
MAX_SPEED = 15
SPEED = 2

class Soldier():
    def __init__(self, health: int, spawnPos: pygame.Vector2):
        # sprite
        self.size = 50
        self.baseImage = pygame.image.load("assets/soldier_head.png").convert_alpha()
        self.baseImage = pygame.transform.scale(self.baseImage, (self.size, self.size))
        self.image = self.baseImage

        # traits
        self.health = health
        self.shotTime = 0

        # movement
        self.vel = pygame.Vector2(0, 0)
        self.pos = spawnPos

    def draw(self, screen: pygame.Surface):
        imageRect = self.image.get_rect()
        imageRect.center = (round(self.pos.x), round(self.pos.y))
        screen.blit(self.image, imageRect)



class Player(Soldier):
    def __init__(self, health: int, spawnPos: pygame.Vector2):
        super().__init__(health, spawnPos)
        self.bullets = []

    def updateSpeed(self, dir: tuple):
        for i in range(2):
            tempVel = round((dir[i] * SPEED) + self.vel[i])
            self.vel[i] = tempVel if abs(tempVel) < MAX_SPEED else MAX_SPEED

    def updateRot(self, mouse_pos):
        direction = mouse_pos - self.pos
        angle = -math.degrees(math.atan2(direction.y, direction.x)) - 90
        self.image = pygame.transform.rotate(self.baseImage, angle)

    def canShoot(self):
        if (time.time() - self.shotTime > 0.2):
            self.shotTime = time.time()
            return True
        return False

    def shoot(self, mouse_pos):
        self.bullets.append(Bullet(self.pos, mouse_pos - self.pos))

    def updateAndDrawBullets(self, screen: pygame.Surface):
        for i in range(len(self.bullets)-1, 0, -1):
            b: Bullet = self.bullets[i]
            if (b.offscreen(screen)):
                self.bullets.pop(i)
            else:
                b.move()
                b.draw(screen)

    def move(self):
        self.vel = [FRICTION * a for a in self.vel]
        self.pos += self.vel


class Bullet():
    def __init__(self, spawnPos: pygame.Vector2, dirVec: pygame.Vector2):
        # movement
        self.pos = pygame.Vector2(spawnPos.x, spawnPos.y)
        angle = -math.degrees(math.atan2(dirVec.y, dirVec.x))
        self.vel = dirVec.normalize()
        self.vel.scale_to_length(20)

        # sprite
        image = pygame.image.load("assets/bullet_px.png").convert_alpha()
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect()

    def move(self):
        self.pos += self.vel

    def offscreen(self, screen: pygame.Surface):
        return not self.rect.colliderect(screen.get_rect())

    def draw(self, screen: pygame.Surface):
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        screen.blit(self.image, self.rect)