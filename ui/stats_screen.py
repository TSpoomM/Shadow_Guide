import pygame
from ui.stats_dashboard import launch_stats_window
from utils.visualize_data import Visualizer


class StatsScreen:
    """
    A UI screen for viewing player statistics.
    Includes toggleable sections for recent data, overall graph, and statistical summary.
    """

    def __init__(self, screen):
        """
        Initializes the statistics screen layout and loads data.

        Args:
            screen (pygame.Surface): The main display surface.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 48)
        self.label_font = pygame.font.SysFont(None, 32, bold=True)
        self.value_font = pygame.font.SysFont(None, 32)

        self.recent_stats = Visualizer.load_recent_stats()
        self.stat_summary = Visualizer.get_statistical_summary()
        self.show_recent = False
        self.show_summary = False
        self.scroll_offset = 0
        self.max_scroll = 1000

    def run(self):
        """
        Main loop for the stats screen. Handles scrolling and mouse toggle interactions.

        Returns:
            str: "home" or "exit" based on user input.
        """
        SECTION_GAP = 40
        BOX_GAP = 30
        LINE_HEIGHT = 40
        TITLE_OFFSET = 60

        while True:
            self.screen.fill((15, 15, 35))
            center_x = self.screen.get_width() // 2
            y = 50 - self.scroll_offset

            # 📊 Title
            title = self.title_font.render("\U0001f4ca Statistics", True, (255, 215, 0))
            self.screen.blit(title, title.get_rect(center=(center_x, y)))
            y += TITLE_OFFSET

            # 🔘 Toggle Buttons
            button_labels = [("Recent", self.show_recent), ("Overall", False), ("Summary", self.show_summary)]
            btn_width = 180
            btn_height = 45
            btn_spacing = 30
            total_width = len(button_labels) * btn_width + (len(button_labels) - 1) * btn_spacing
            start_x = center_x - total_width // 2
            button_rects = []

            for i, (label, is_on) in enumerate(button_labels):
                btn_x = start_x + i * (btn_width + btn_spacing)
                rect = pygame.Rect(btn_x, y, btn_width, btn_height)
                btn_color = (0, 180, 100) if is_on else (80, 80, 80)
                pygame.draw.rect(self.screen, btn_color, rect, border_radius=8)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=8)
                text = self.font.render(label, True, (255, 255, 255))
                self.screen.blit(text, text.get_rect(center=rect.center))
                button_rects.append((rect, label))
            y += btn_height + SECTION_GAP

            # 📈 Recent Stats Section
            if self.show_recent:
                recent_lines = list(self.recent_stats.items()) if self.recent_stats else [("No Data", "-")]
                box_height = len(recent_lines) * LINE_HEIGHT + 20
                box_rect = pygame.Rect(center_x - 210, y, 440, box_height)
                pygame.draw.rect(self.screen, (30, 30, 60), box_rect, border_radius=10)
                pygame.draw.rect(self.screen, (0, 200, 255), box_rect, 2, border_radius=10)

                for i, (label, value) in enumerate(recent_lines):
                    line_y = y + 10 + i * LINE_HEIGHT
                    label_text = self.label_font.render(f"{label}:", True, (255, 255, 255))
                    value_text = self.value_font.render(str(value), True, (200, 255, 200))
                    self.screen.blit(label_text, (box_rect.left + 20, line_y))
                    self.screen.blit(value_text, (box_rect.right - 20 - value_text.get_width(), line_y))

                y += box_height + SECTION_GAP

            # 📊 Statistical Summary Section
            if self.show_summary:
                y += SECTION_GAP
                for group, metrics in self.stat_summary.items():

                    # Section header
                    group_title = self.label_font.render(group, True, (255, 255, 255))
                    self.screen.blit(group_title, (center_x - 200, y))
                    y += LINE_HEIGHT

                    lines = list(metrics.items())
                    box_height = len(lines) * LINE_HEIGHT + 20
                    box_rect = pygame.Rect(center_x - 210, y, 440, box_height)
                    pygame.draw.rect(self.screen, (30, 30, 60), box_rect, border_radius=10)
                    pygame.draw.rect(self.screen, (255, 255, 100), box_rect, 2, border_radius=10)

                    for i, (key, value) in enumerate(lines):
                        line_y = y + 10 + i * LINE_HEIGHT
                        key_text = self.value_font.render(f"{key}:", True, (255, 255, 255))
                        val_text = self.value_font.render(str(value), True, (200, 255, 200))
                        self.screen.blit(key_text, (box_rect.left + 20, line_y))
                        self.screen.blit(val_text, (box_rect.right - 20 - val_text.get_width(), line_y))

                    y += box_height + BOX_GAP

            # ⌨️ Footer hint
            hint = self.font.render("\u2191 / \u2193 scroll | B: back | Click toggle above", True, (180, 180, 180))
            self.screen.blit(hint, hint.get_rect(center=(center_x, 560)))

            pygame.display.flip()

            # 🎮 Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        return "home"
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.scroll_offset += 30
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        self.scroll_offset = max(0, self.scroll_offset - 30)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for rect, label in button_rects:
                        if rect.collidepoint(mx, my):

                            # Toggle sections
                            if label == "Recent":
                                self.show_recent = not self.show_recent
                            elif label == "Summary":
                                self.show_summary = not self.show_summary
                            elif label == "Overall":
                                launch_stats_window()
                                return "stats"

            self.clock.tick(30)
