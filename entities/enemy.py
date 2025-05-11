import pygame
import math
import random
from entities.explosion import Explosion  # Ensure this exists and has draw()


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


class ShootingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (100, 100, 255))
        self.shoot_cooldown = 120
        self.shoot_timer = 0
        self.bullets = pygame.sprite.Group()

    def update(self, player_rect):
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            bullet = Bullet(self.rect.centerx, self.rect.centery, player_rect.centerx, player_rect.centery)
            self.bullets.add(bullet)
        self.bullets.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        angle = math.atan2(target_y - y, target_x - x)
        speed = 5
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def update(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)


class ExplodingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 150, 0))
        self.trigger_range = 80  # เริ่มระเบิดถ้าเข้าใกล้
        self.damage_radius = 80  # ระยะที่โดนดาเมจ AoE
        self.exploded = False

    def update(self, player_rect):
        if self.exploded:
            return
        dist = math.hypot(player_rect.centerx - self.rect.centerx, player_rect.centery - self.rect.centery)
        if dist < self.trigger_range:
            self.exploded = True
            self.kill()  # ระเบิดตัวเอง
            return Explosion(self.rect.centerx, self.rect.centery), dist < self.damage_radius
        return None, False


class TeleportingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (150, 0, 200))
        self.timer = 0
        self.teleport_interval = 120  # ทุก 2 วินาที (60 FPS)
        self.safe_distance = 100

    def update(self, player_rect):
        self.timer += 1
        if self.timer >= self.teleport_interval:
            self.timer = 0
            px, py = player_rect.center
            # ย้ายตำแหน่งใกล้ player โดยไม่อยู่ตรงบน
            offset_x = random.choice([-1, 1]) * random.randint(50, 100)
            offset_y = random.choice([-1, 1]) * random.randint(30, 80)
            new_x = max(0, px + offset_x)
            new_y = max(0, py + offset_y)
            self.rect.center = (new_x, new_y)


class DroppingEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, (100, 100, 100))
        self.original_y = y
        self.speed = 8
        self.dropped = False

    def update(self, player_rect):
        if not self.dropped:
            # Check ถ้า player อยู่แนวตั้งใกล้ด้านล่าง
            if abs(player_rect.centerx - self.rect.centerx) < 20 and player_rect.centery > self.rect.centery:
                self.dropped = True
        else:
            self.rect.y += self.speed  # หล่นลงมา
