# ui/records_screen.py

import pygame
import csv
import os
from collections import defaultdict


class RecordsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 28)
        self.records = self.load_grouped_records()

        self.card_width = 580
        self.card_height = 70
        self.card_spacing = 15
        self.scroll_offset = 0
        self.max_scroll = max(0, len(self.records) * (self.card_height + self.card_spacing) + 60 - 400)

    def load_grouped_records(self):
        file_path = "game_data.csv"
        if not os.path.exists(file_path):
            return []

        scores_by_name = defaultdict(list)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    score = 10
                    if int(row["jump_count"]) > 10:
                        score -= 1
                    if float(row["avg_jump_interval"]) > 1.0:
                        score -= 1
                    if int(row["death_count"]) > 0:
                        score -= 2
                    score = max(0, score)
                    scores_by_name[row["player_name"]].append(score)
                except:
                    continue

        grouped = []
        for name, scores in scores_by_name.items():
            avg = sum(scores) / len(scores)
            grouped.append({
                "player": name,
                "avg_score": round(avg, 2),
                "sessions": len(scores)
            })

        grouped.sort(key=lambda r: r["avg_score"], reverse=True)
        return grouped

    def draw_record_card(self, surface, x, y, width, height, rank, player, avg_score, sessions):
        pygame.draw.rect(surface, (30, 30, 60), (x, y, width, height), border_radius=12)
        pygame.draw.rect(surface, (100, 100, 200), (x, y, width, height), 2, border_radius=12)

        text_rank = self.card_font.render(f"#{rank}", True, (255, 255, 100))
        text_name = self.card_font.render(f"{player}", True, (255, 255, 255))
        text_score = self.card_font.render(f"Avg Score: {avg_score}/10", True, (200, 255, 200))
        text_sessions = self.card_font.render(f"Sessions: {sessions}", True, (180, 180, 255))

        surface.blit(text_rank, (x + 12, y + 10))
        surface.blit(text_name, (x + 70, y + 10))
        surface.blit(text_score, (x + 70, y + 40))
        surface.blit(text_sessions, (x + 300, y + 40))

    def run(self):
        center_x = self.screen.get_width() // 2 - self.card_width // 2

        while True:
            self.screen.fill((15, 15, 35))

            # Draw title (scrolls with content)
            title_y = 50 - self.scroll_offset
            title = self.title_font.render("🏆 Top Players (by Avg Score)", True, (255, 215, 0))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, title_y))
            self.screen.blit(title, title_rect)

            # Draw cards (scrolls with content)
            current_y = 120 - self.scroll_offset
            for i, record in enumerate(self.records):
                if -self.card_height < current_y < self.screen.get_height() - 80:
                    self.draw_record_card(
                        self.screen, center_x, current_y, self.card_width, self.card_height,
                        i + 1, record["player"], record["avg_score"], record["sessions"]
                    )
                current_y += self.card_height + self.card_spacing

            # Footer Hint
            hint = self.font.render("↑ / ↓ or W / S to scroll   |   Press B to go back", True, (180, 180, 180))
            hint_rect = hint.get_rect(center=(self.screen.get_width() // 2, 560))
            self.screen.blit(hint, hint_rect)

            pygame.display.flip()

            # Input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        return "home"
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.scroll_offset = min(self.scroll_offset + 30, self.max_scroll)
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        self.scroll_offset = max(self.scroll_offset - 30, 0)

            self.clock.tick(30)
