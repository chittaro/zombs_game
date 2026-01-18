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
        self.size = 15
        self.baseImage = pygame.image.load("assets/soldier_head.png").convert_alpha()
        self.image = self.baseImage

        # traits
        self.health = health
        self.shotTime = 0

        # movement
        self.vel = pygame.Vector2(0, 0)
        self.pos = spawnPos

    def draw(self, screen):
        # pygame.draw.circle(screen, self.color, (self.rect.center), self.size)
        imageRect = self.image.get_rect()
        imageRect.center = (round(self.pos.x), round(self.pos.y))
        screen.blit(self.image, imageRect)



class Player(Soldier):
    def __init__(self, health: int, spawnPos: pygame.Vector2):
        super().__init__(health, spawnPos)

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

    def shoot(self, pos):
        print("shooting")
        
    def move(self, screen):
        self.vel = [FRICTION * a for a in self.vel]
        self.pos += self.vel


class Bullet():
    def __init__(self, spawnPos: pygame.Vector2, angle: float):
        # sprite
        # self.image = 

        # movement
        self.pos = spawnPos
        