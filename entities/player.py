import pygame
import random


class Player:
    def __init__(self, spawn_points, tile_size=30):
        self.tile_size = tile_size
        self.spawn_points = spawn_points
        self.rect = pygame.Rect(0, 0, tile_size, tile_size)
        self.velocity_y = 0
        self.gravity = 1
        self.speed = 5
        self.jump_power = -15
        self.on_ground = False

        # ⭐ Double Jump
        self.jump_count = 0
        self.max_jump = 2

        # ⭐ Dash
        self.is_dashing = False
        self.dash_speed = 10
        self.dash_duration = 10
        self.dash_timer = 0
        self.dash_cooldown = 60
        self.last_dash_time = -self.dash_cooldown
        self.direction_x = 0

        # ⭐ Energy
        self.energy = 40
        self.max_energy = 40
        self.energy_regen_rate = 0.3

        if spawn_points:
            self.rect.topleft = random.choice(spawn_points)
        else:
            self.rect.topleft = (100, 300)

    def move(self, keys):
        move_x = 0

        # ⭐ Dash trigger
        if (keys[pygame.K_LSHIFT]) or (keys[pygame.K_RSHIFT]):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_dash_time >= self.dash_cooldown * (1000 // 60):
                if self.energy >= 20:
                    self.is_dashing = True
                    self.dash_timer = self.dash_duration
                    self.last_dash_time = current_time
                    self.energy -= 20

        # ⭐ Walking
        if not self.is_dashing:
            if keys[pygame.K_LEFT]:
                move_x = -self.speed
                self.direction_x = -1
            elif keys[pygame.K_RIGHT]:
                move_x = self.speed
                self.direction_x = 1

        # ⭐ Dashing
        if self.is_dashing:
            move_x = self.direction_x * (self.speed + self.dash_speed)
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False

        return move_x

    def jump(self):
        if self.jump_count < self.max_jump:
            if self.energy >= 15:
                self.velocity_y = self.jump_power
                self.on_ground = False
                self.jump_count += 1
                self.energy -= 15
                return True
        return False

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # ⭐ Energy regen
        self.energy += self.energy_regen_rate
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def check_collision_y(self, platforms):
        self.on_ground = False
        for plat, _ in platforms:
            if self.rect.colliderect(plat):
                if self.velocity_y > 0:
                    self.rect.bottom = plat.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.velocity_y < 0:
                    self.rect.top = plat.bottom
                    self.velocity_y = 0

    def check_collision_x(self, platforms, move_x):
        self.rect.x += move_x
        for plat, _ in platforms:
            if self.rect.colliderect(plat):
                if move_x > 0:
                    self.rect.right = plat.left
                elif move_x < 0:
                    self.rect.left = plat.right

    def reset_position(self):
        if self.spawn_points:
            self.rect.topleft = random.choice(self.spawn_points)
        else:
            self.rect.topleft = (100, 300)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)
