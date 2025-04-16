import pygame
import time
from pygame.sprite import Group
from entities.enemy import EnemyFactory
from data_logger import DataLogger


class PlayScreen:
    TILE_SIZE = 50

    def __init__(self, screen, map_path, level):
        self.screen = screen
        self.map_path = map_path
        self.level = level
        self.font = pygame.font.SysFont(None, 40)
        self.player_rect = pygame.Rect(100, 300, 50, 50)
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = False
        self.platforms = []
        self.enemies = Group()
        self.goal = None
        self.health = 3
        self.game_over = False
        self.level_complete = False
        self.level_data = self.load_map()
        self.parse_map()

        # stats
        self.jump_count = 0
        self.death_count = 0
        self.jump_times = []
        self.last_jump_time = None
        self.hint_count = 0

        if not self.platforms:
            self.platforms.append(pygame.Rect(0, 550, 800, 50))

    def load_map(self):
        with open(self.map_path, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def parse_map(self):
        for y, row in enumerate(self.level_data):
            for x, tile in enumerate(row):
                pos = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                if tile == '#':
                    self.platforms.append(pos)
                elif tile == 'E':
                    enemy = EnemyFactory.create_random(pos.x, pos.y, self.level)
                    self.enemies.add(enemy)
                elif tile == 'G':
                    self.goal = pos

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.screen.fill((10, 10, 40))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    if self.game_over or self.level_complete:
                        return "home"

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.player_rect.x += 5
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -15
                self.on_ground = False
                self.jump_count += 1
                current_time = time.time()
                if self.last_jump_time:
                    interval = current_time - self.last_jump_time
                    self.jump_times.append(interval)
                self.last_jump_time = current_time

            self.velocity_y += self.gravity
            self.player_rect.y += self.velocity_y

            self.on_ground = False
            for plat in self.platforms:
                if self.player_rect.colliderect(plat) and self.velocity_y >= 0:
                    self.player_rect.bottom = plat.top
                    self.velocity_y = 0
                    self.on_ground = True

            self.enemies.update(self.player_rect)

            for enemy in self.enemies:
                if self.player_rect.colliderect(enemy.rect):
                    self.health -= 1
                    self.death_count += 1
                    self.player_rect.topleft = (100, 300)
                    if self.health <= 0:
                        self.game_over = True
                        self.save_stats()

            if self.goal and self.player_rect.colliderect(self.goal):
                self.level_complete = True
                self.save_stats()
                return "level_complete"

            for plat in self.platforms:
                pygame.draw.rect(self.screen, (100, 255, 100), plat)

            self.enemies.draw(self.screen)
            pygame.draw.rect(self.screen, (255, 255, 0), self.player_rect)

            if self.goal:
                pygame.draw.rect(self.screen, (0, 255, 255), self.goal)

            text = self.font.render(f"HP: {self.health}  Level: {self.level}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

    def save_stats(self):
        if self.jump_times:
            avg_interval = sum(self.jump_times) / len(self.jump_times)
        else:
            avg_interval = 0.0
        DataLogger.log(
            self.level,
            self.jump_count,
            self.death_count,
            avg_interval,
            self.hint_count
        )
