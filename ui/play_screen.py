# ui/play_screen.py

import pygame
import time
from pygame.sprite import Group
from entities.enemy import EnemyFactory
from entities.player import Player
from ai.ai_helper import AIHelper
from utils.data_logger import DataLogger


class PlayScreen:
    TILE_SIZE = 30

    def __init__(self, screen, map_path, level, player_name):
        self.screen = screen
        self.map_path = map_path
        self.level = level
        self.player_name = player_name

        self.font = pygame.font.SysFont(None, 40)
        self.hint_font = pygame.font.SysFont(None, 30)

        self.platforms = []
        self.enemies = Group()
        self.goal = None
        self.spawn_points = []

        self.health = 3
        self.level_complete = False
        self.game_over = False
        self.level_score = 10
        self.total_score_list = []
        self.start_time = time.time()

        self.jump_count = 0
        self.jump_times = []
        self.last_jump_time = None
        self.death_count = 0
        self.hint_count = 0
        self.enemy_triggered = 0

        self.last_hint_time = 0
        self.current_hints = []
        self.hint_interval = 3000  # 3 seconds

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

        self.level_data = self.load_map()
        self.parse_map()
        self.player = Player(self.spawn_points, tile_size=self.TILE_SIZE)
        self.ai_helper = AIHelper(self.player, self.platforms, self.enemies, self.goal)

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
                    self.enemies.add(EnemyFactory.create_random(pos.x, pos.y, self.level))
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
                        if self.player.jump():
                            self.jump_count += 1
                            now = time.time()
                            if self.last_jump_time:
                                self.jump_times.append(now - self.last_jump_time)
                            self.last_jump_time = now

            keys = pygame.key.get_pressed()
            move_x = self.player.move(keys)

            self.player.apply_gravity()
            self.player.check_collision_y(self.platforms)
            self.player.check_collision_x(self.platforms, move_x)

            # ตกเหว
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
                    self.enemy_triggered += 1
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
            for plat, t in self.platforms:
                if t in self.tile_images:
                    self.screen.blit(self.tile_images[t], plat.topleft)

            self.enemies.draw(self.screen)

            if self.goal:
                self.screen.blit(self.goal_image, self.goal.topleft)

            self.player.draw(self.screen)
            self.draw_helper_hint()
            self.draw_ui()

            pygame.display.flip()
            clock.tick(60)

    def draw_helper_hint(self):
        now = pygame.time.get_ticks()
        if now - self.last_hint_time > self.hint_interval:
            self.current_hints = self.ai_helper.get_hints()
            self.last_hint_time = now
            self.hint_count += len(self.current_hints)

        for i, hint in enumerate(self.current_hints):
            hint_surface = self.hint_font.render(hint, True, (255, 255, 0))
            self.screen.blit(hint_surface, (self.player.rect.x - 20, self.player.rect.y - 40 - i * 20))

    def draw_ui(self):
        text = self.font.render(f"HP: {self.health}  Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        # Energy bar
        bar_x, bar_y = 10, 50
        bar_width, bar_height = 200, 20
        ratio = self.player.energy / self.player.max_energy
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 200, 255), (bar_x, bar_y, bar_width * ratio, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def calculate_level_score(self):
        elapsed = time.time() - self.start_time
        if self.jump_count > 10:
            self.level_score = max(0, self.level_score - 1)
        if elapsed > 60:
            self.level_score = max(0, self.level_score - 1)
        self.total_score_list.append(self.level_score)

    def save_stats(self):
        avg_jump = sum(self.jump_times) / len(self.jump_times) if self.jump_times else 0.0
        DataLogger.log(
            player_name=self.player_name,
            level=self.level,
            jump_count=self.jump_count,
            death_count=self.death_count,
            avg_jump_interval=avg_jump,
            hint_count=self.hint_count,
            enemy_triggered=self.enemy_triggered
        )

    def show_level_complete(self):
        clock = pygame.time.Clock()
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        title_font = pygame.font.SysFont(None, 64, bold=True)
        text_font = pygame.font.SysFont(None, 40)
        button_font = pygame.font.SysFont(None, 32, bold=True)

        while True:
            self.screen.fill((10, 10, 10))

            # Title
            msg1 = title_font.render("✅ You Passed This Level!", True, (0, 255, 0))
            self.screen.blit(msg1, msg1.get_rect(center=(center_x, center_y - 100)))

            # Subtitle
            msg2 = text_font.render("Wanna go to the next level?", True, (255, 255, 255))
            self.screen.blit(msg2, msg2.get_rect(center=(center_x, center_y - 30)))

            # Buttons visual
            enter_rect = pygame.Rect(center_x - 120, center_y + 30, 100, 45)
            n_rect = pygame.Rect(center_x + 20, center_y + 30, 100, 45)

            pygame.draw.rect(self.screen, (0, 200, 100), enter_rect, border_radius=8)
            pygame.draw.rect(self.screen, (200, 50, 50), n_rect, border_radius=8)

            pygame.draw.rect(self.screen, (255, 255, 255), enter_rect, 2, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), n_rect, 2, border_radius=8)

            enter_text = button_font.render("Enter / Y", True, (255, 255, 255))
            n_text = button_font.render("N", True, (255, 255, 255))
            self.screen.blit(enter_text, enter_text.get_rect(center=enter_rect.center))
            self.screen.blit(n_text, n_text.get_rect(center=n_rect.center))

            # Footer
            footer = self.font.render("Press Enter/Y to continue or N to return", True, (180, 180, 180))
            self.screen.blit(footer, footer.get_rect(center=(center_x, center_y + 110)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_y]:
                        return "level_complete"
                    elif event.key == pygame.K_n or event.key == pygame.K_b:
                        return "home"

            clock.tick(30)

    def show_game_over(self):
        clock = pygame.time.Clock()
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        title_font = pygame.font.SysFont(None, 64, bold=True)
        text_font = pygame.font.SysFont(None, 40)
        button_font = pygame.font.SysFont(None, 32, bold=True)

        average_score = sum(self.total_score_list) / len(self.total_score_list) if self.total_score_list else 0

        while True:
            self.screen.fill((0, 0, 0))

            # ❌ Title
            msg1 = title_font.render("💀 Game Over!", True, (255, 50, 50))
            self.screen.blit(msg1, msg1.get_rect(center=(center_x, center_y - 100)))

            # 📊 Score
            score_text = text_font.render(f"Your Average Score: {average_score:.2f}/10", True, (255, 255, 255))
            self.screen.blit(score_text, score_text.get_rect(center=(center_x, center_y - 30)))

            # 🔘 Button: Back
            back_rect = pygame.Rect(center_x - 90, center_y + 30, 180, 45)
            pygame.draw.rect(self.screen, (50, 50, 200), back_rect, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 2, border_radius=8)
            back_text = button_font.render("Back to Menu (B)", True, (255, 255, 255))
            self.screen.blit(back_text, back_text.get_rect(center=back_rect.center))

            # Footer
            footer = self.font.render("Press B to return", True, (180, 180, 180))
            self.screen.blit(footer, footer.get_rect(center=(center_x, center_y + 110)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        return "home"

            clock.tick(30)
