import pygame
import math
import random


class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 0, 0)):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, player_rect):
        pass


class PatrollingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 100, 100))
        self.original_x = x
        self.direction = 1
        self.speed = 2
        self.range = 100

    def update(self, player_rect):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.original_x) > self.range:
            self.direction *= -1


class ChasingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 200, 100))
        self.speed = 2
        self.chase_range = 200

    def update(self, player_rect):
        dist = math.hypot(player_rect.centerx - self.rect.centerx, player_rect.centery - self.rect.centery)
        if dist < self.chase_range:
            if player_rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed


class JumpingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (100, 255, 100))
        self.base_y = y
        self.jump_height = 40
        self.timer = 0

    def update(self, player_rect):
        self.timer += 1
        self.rect.y = self.base_y + int(math.sin(self.timer * 0.1) * self.jump_height)


class FlyingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (100, 200, 255))
        self.base_y = y
        self.timer = 0
        self.fly_range = 30

    def update(self, player_rect):
        self.timer += 1
        self.rect.y = self.base_y + int(math.sin(self.timer * 0.05) * self.fly_range)


class TrapEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 255))  # stationary trap
        self.damage = True


class EnemyFactory:
    LEVEL_ENEMY_POOL = {
        1: [PatrollingEnemy],
        2: [PatrollingEnemy, ChasingEnemy],
        3: [PatrollingEnemy, ChasingEnemy, JumpingEnemy],
        4: [PatrollingEnemy, ChasingEnemy, JumpingEnemy, FlyingEnemy],
        5: [PatrollingEnemy, ChasingEnemy, JumpingEnemy, FlyingEnemy, TrapEnemy],
    }

    @staticmethod
    def create_random(x, y, level):
        pool = []
        for i in range(1, level + 1):
            pool.extend(EnemyFactory.LEVEL_ENEMY_POOL.get(i, []))
        if not pool:
            pool = [PatrollingEnemy]
        cls = random.choice(pool)
        return cls(x, y)
