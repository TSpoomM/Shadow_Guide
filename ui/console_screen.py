import pygame
import textwrap


class ConsoleScreen:
    """
    ConsoleScreen displays the control instructions for the game.
    Supports scrolling and returns to the main menu when 'B' is pressed.
    """

    def __init__(self, screen):
        """
        Initializes fonts, layout, and control instruction content.

        Args:
            screen (pygame.Surface): The main display surface.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont(None, 52)
        self.key_font = pygame.font.SysFont(None, 34, bold=True)
        self.desc_font = pygame.font.SysFont(None, 30)
        self.hint_font = pygame.font.SysFont(None, 28)

        self.controls = [
            ("← / →", "Move Left / Right"),
            ("SPACE", "Jump (Double Jump if enough energy)"),
            ("SHIFT", "Dash (Consumes energy, has cooldown)"),
            ("B", "Return to Main Menu (if Game Over or Passed)"),
            ("ENTER / Y", "Proceed to Next Level"),
            ("N", "Return to Main Menu after pass"),
            ("1 / 2 / 3 / 4", "View Graphs on Statistics Page"),
            ("ESC / Close", "Exit the game"),
        ]

        self.scroll_offset = 0
        self.line_height = 70
        self.max_scroll = max(0, len(self.controls) * self.line_height - 360)

    def draw_controls(self):
        """
        Draws all key-description pairs with styled boxes and handles scrolling display.
        """
        screen_w = self.screen.get_width()
        key_box_w, desc_box_w = 180, 420
        spacing = 20
        total_w = key_box_w + desc_box_w + spacing
        base_x = (screen_w - total_w) // 2
        current_y = 130 - self.scroll_offset

        for key_text, desc_text in self.controls:
            # Word wrap for long descriptions
            wrapped_lines = textwrap.wrap(desc_text, width=38)
            desc_box_h = 50 + (len(wrapped_lines) - 1) * 22
            box_h = max(50, desc_box_h)

            # Draw only if visible on screen
            if -60 < current_y < self.screen.get_height() - 80:
                # Key box
                key_rect = pygame.Rect(base_x, current_y, key_box_w, box_h)
                pygame.draw.rect(self.screen, (50, 50, 100), key_rect, border_radius=8)
                pygame.draw.rect(self.screen, (180, 180, 255), key_rect, 2, border_radius=8)
                key_render = self.key_font.render(key_text, True, (255, 255, 100))
                self.screen.blit(key_render, key_render.get_rect(center=key_rect.center))

                # Description box
                desc_rect = pygame.Rect(base_x + key_box_w + spacing, current_y, desc_box_w, box_h)
                pygame.draw.rect(self.screen, (30, 30, 60), desc_rect, border_radius=8)
                pygame.draw.rect(self.screen, (100, 100, 200), desc_rect, 2, border_radius=8)

                for j, line in enumerate(wrapped_lines[:2]):
                    desc_render = self.desc_font.render(line, True, (255, 255, 255))
                    self.screen.blit(desc_render, (desc_rect.left + 12, desc_rect.top + 10 + j * 22))

            # Increase Y for next line
            current_y += box_h + 10

    def run(self):
        """
        Runs the control screen loop, waits for user to press 'B' or scroll.
        Returns:
            str: "home" if user presses B, "exit" if user quits.
        """
        while True:
            self.screen.fill((15, 15, 35))

            # Draw title
            title_y = 50 - self.scroll_offset
            title = self.title_font.render("🎮 Controls / How to Play", True, (255, 215, 0))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, title_y))
            self.screen.blit(title, title_rect)

            # Draw control list
            self.draw_controls()

            # Draw footer hint
            hint = self.hint_font.render("↑ / ↓ or W / S to scroll   |   Press B to go back", True, (180, 180, 180))
            hint_rect = hint.get_rect(center=(self.screen.get_width() // 2, 560))
            self.screen.blit(hint, hint_rect)

            pygame.display.flip()

            # Handle events
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
