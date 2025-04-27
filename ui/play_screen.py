import pygame
import os
import time
import random
from pygame.sprite import Group
from entities.enemy import EnemyFactory
from entities.player import Player
from ai.ai_helper import AIHelper
from data_logger import DataLogger


class PlayScreen:
    TILE_SIZE = 30

    def __init__(self, screen, map_path, level):
        self.screen = screen
        self.map_path = map_path
        self.level = level
        self.font = pygame.font.SysFont(None, 40)
        self.gravity = 1
        self.platforms = []
        self.enemies = Group()
        self.goal = None
        self.health = 3
        self.game_over = False
        self.level_complete = False
        self.level_data = self.load_map()
        self.spawn_points = []
        self.jump_count = 0
        self.death_count = 0
        self.jump_times = []
        self.last_jump_time = None
        self.hint_count = 0
        self.level_score = 10
        self.total_score_list = []
        self.start_time = time.time()

        self.tile_images = {
            "#": pygame.transform.scale(pygame.image.load("assets/images/dirt_block_with_grass.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            "S": pygame.transform.scale(pygame.image.load("assets/images/stone_block.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            "W": pygame.transform.scale(pygame.image.load("assets/images/wood_block.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE))
        }

        self.goal_image = pygame.transform.scale(
            pygame.image.load("assets/images/portal.png"),
            (self.TILE_SIZE, self.TILE_SIZE)
        )

        self.parse_map()
        self.player = Player(self.spawn_points, tile_size=self.TILE_SIZE)
        self.ai_helper = AIHelper(self.player, self.platforms, self.enemies, self.goal)
        self.hint_font = pygame.font.SysFont(None, 30)

        self.last_hint_time = 0
        self.current_hints = []
        self.hint_interval = 3000  # 3 วินาที

    def load_map(self):
        with open(self.map_path, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def parse_map(self):
        for y, row in enumerate(self.level_data):
            for x, tile in enumerate(row):
                pos = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                if tile in ["#", "S", "W"]:
                    self.platforms.append((pos, tile))
                elif tile == 'E':
                    enemy = EnemyFactory.create_random(pos.x, pos.y, self.level)
                    self.enemies.add(enemy)
                elif tile == 'G':
                    self.goal = pos
                elif tile == 'P':
                    self.spawn_points.append((pos.x, pos.y))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.screen.fill((10, 10, 40))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        if self.game_over:
                            return "home"
                    elif event.key == pygame.K_SPACE:
                        jumped = self.player.jump()
                        if jumped:
                            self.jump_count += 1
                            current_time = time.time()
                            if self.last_jump_time:
                                interval = current_time - self.last_jump_time
                                self.jump_times.append(interval)
                            self.last_jump_time = current_time

            keys = pygame.key.get_pressed()
            move_x = self.player.move(keys)

            self.player.apply_gravity()
            self.player.check_collision_y(self.platforms)
            self.player.check_collision_x(self.platforms, move_x)

            # ⭐ ตกนอกแมพ
            if self.player.rect.top > self.screen.get_height():
                self.health -= 1
                self.level_score = max(0, self.level_score - 2)
                self.death_count += 1
                self.player.reset_position()
                if self.health <= 0:
                    self.game_over = True
                    self.save_stats()
                    return self.show_game_over()

            self.enemies.update(self.player.rect)
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    self.health -= 1
                    self.level_score = max(0, self.level_score - 2)
                    self.death_count += 1
                    self.player.reset_position()
                    if self.health <= 0:
                        self.game_over = True
                        self.save_stats()
                        return self.show_game_over()

            if self.goal and self.player.rect.colliderect(self.goal):
                self.level_complete = True
                self.calculate_level_score()
                self.save_stats()
                return self.show_level_complete()

            # Draw
            for plat, tile_type in self.platforms:
                if tile_type in self.tile_images:
                    self.screen.blit(self.tile_images[tile_type], plat.topleft)

            self.enemies.draw(self.screen)

            if self.goal:
                self.screen.blit(self.goal_image, self.goal.topleft)

            self.player.draw(self.screen)

            self.draw_helper_hint()
            self.draw_ui()

            pygame.display.flip()
            clock.tick(60)

    def draw_helper_hint(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_hint_time > self.hint_interval:
            self.current_hints = self.ai_helper.get_hints()
            self.last_hint_time = current_time

        for i, hint in enumerate(self.current_hints):
            hint_text = self.hint_font.render(hint, True, (255, 255, 0))
            self.screen.blit(hint_text, (self.player.rect.x - 20, self.player.rect.y - 40 - i * 20))

    def draw_ui(self):
        text = self.font.render(f"HP: {self.health}  Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 50
        energy_ratio = self.player.energy / self.player.max_energy
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 200, 255), (bar_x, bar_y, bar_width * energy_ratio, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def calculate_level_score(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        if self.jump_count > 10:
            self.level_score = max(0, self.level_score - 1)
        if elapsed_time > 60:
            self.level_score = max(0, self.level_score - 1)

        self.total_score_list.append(self.level_score)

    def save_stats(self):
        avg_interval = sum(self.jump_times) / len(self.jump_times) if self.jump_times else 0.0
        DataLogger.log(self.level, self.jump_count, self.death_count, avg_interval, self.hint_count)

    def show_level_complete(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((0, 0, 0))
            msg1 = self.font.render("You Passed This Level!", True, (0, 255, 0))
            msg2 = self.font.render("Wanna Go Next? (Enter/N)", True, (255, 255, 255))
            self.screen.blit(msg1, (180, 200))
            self.screen.blit(msg2, (160, 260))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y or event.key == pygame.K_RETURN:
                        return "level_complete"
                    elif event.key == pygame.K_n or event.key == pygame.K_b:
                        return "home"
            clock.tick(30)

    def show_game_over(self):
        clock = pygame.time.Clock()
        average_score = sum(self.total_score_list) / len(self.total_score_list) if self.total_score_list else 0
        while True:
            self.screen.fill((0, 0, 0))
            msg1 = self.font.render("Game Over!", True, (255, 0, 0))
            msg2 = self.font.render(f"Average Score: {average_score:.2f}/10", True, (255, 255, 255))
            msg3 = self.font.render("Press B to return Home", True, (200, 200, 200))
            self.screen.blit(msg1, (250, 180))
            self.screen.blit(msg2, (200, 240))
            self.screen.blit(msg3, (180, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    return "home"
            clock.tick(30)
