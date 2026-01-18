import math
import pygame
import numpy as np
import time
import random

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

    def getRect(self):
        imageRect = self.image.get_rect()
        imageRect.center = (round(self.pos.x), round(self.pos.y))
        return imageRect

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.getRect())


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
        for i in range(len(self.bullets)-1, -1, -1):
            b: Bullet = self.bullets[i]
            if (b.offscreen(screen)):
                self.bullets.pop(i)
            else:
                b.move()
                b.draw(screen)

    def move(self):
        self.vel = [FRICTION * a for a in self.vel]
        self.pos += self.vel


class Enemy():
    size = 50
    speed = 4

    def __init__(self, spawnPos: pygame.Vector2):
        self.pos = spawnPos
        self.rect = pygame.Rect(spawnPos, (self.size, self.size))
        self.vel = pygame.Vector2(0, 0)

    def move(self, targetVec: pygame.Vector2):
        direction = targetVec - self.pos
        targetVel = direction.normalize()
        targetVel.scale_to_length(self.speed)
        self.vel += ((targetVel - self.vel) * 0.1)
        self.pos += self.vel

    def offscreen(self, screen: pygame.Surface):
        return not self.rect.colliderect(screen.get_rect())

    def draw(self, screen: pygame.Surface):
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        pygame.draw.rect(screen, "pink", self.rect, self.size)


class EnemySpawner():
    maxEnemies = 5
    enemies = []
    lastSpawn = 0
    spawnGap = 2

    def __init__(self, screenWid: int, screenHgt: int):
        self.maxX = screenWid
        self.maxY = screenHgt

    def canSpawn(self):
        return (len(self.enemies) < self.maxEnemies and
                time.time() - self.lastSpawn > self.spawnGap)

    def spawn(self):
        if self.canSpawn():
            self.lastSpawn = time.time()
            randX = (self.maxX + Enemy.size) * random.choice([-1, 1])
            randY = random.randint(0, self.maxY)
            randVec = pygame.Vector2(randX, randY)
            self.enemies.append(Enemy(randVec))

    def isCollision(self, player: Player):
        for i in range(len(self.enemies)-1, -1, -1):
            e: Enemy = self.enemies[i]
            if e.rect.colliderect(player.getRect()):
                return True
        return False
    
    def shotCollisions(self, bullets: list):
        for i in range(len(bullets)-1, -1, -1):
            b: Bullet = bullets[i]
            for j in range(len(self.enemies)-1, -1, -1):
                e: Enemy = self.enemies[j]
                if e.rect.colliderect(b.rect):
                    bullets.pop(i)
                    self.enemies.pop(j)
                    break

    def update(self, player: Player):
        for e in self.enemies:
            e.move(player.pos)

    def draw(self, screen: pygame.Surface):
        for e in self.enemies:
            e.draw(screen)

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