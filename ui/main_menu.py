import pygame


class Button:
    """
    A simple button UI component with hover and click functionality.
    """

    def __init__(self, text, pos, width, height, callback):
        """
        Initializes a button.

        Args:
            text (str): Text to display on the button.
            pos (tuple): (x, y) position of the top-left corner.
            width (int): Width of the button.
            height (int): Height of the button.
            callback (function): Function to call when the button is clicked.
        """
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.callback = callback
        self.color_idle = (50, 50, 50)
        self.color_hover = (100, 100, 100)
        self.border_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

    def draw(self, screen):
        """
        Draw the button to the screen with hover effect.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.color_hover, self.rect)
        else:
            pygame.draw.rect(screen, self.color_idle, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        """
        Handle click events.

        Args:
            event (pygame.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()


class MainMenu:
    """
    Main menu screen of the game. Shows title and menu buttons with gradient background.
    """

    def __init__(self, screen):
        """
        Initializes the main menu and its buttons.

        Args:
            screen (pygame.Surface): The main display surface.
        """
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)

        button_width = 300
        button_height = 60
        button_spacing = 20

        center_x = self.screen.get_width() // 2 - button_width // 2
        start_y = 150

        self.buttons = []
        button_info = [
            ("Play", self.goto_play),
            ("Console", self.goto_console),
            ("Records", self.goto_records),
            ("Statistics", self.goto_stats),
            ("Exit", self.exit_game)
        ]

        # Create Button objects from label and callback pairs
        for i, (text, callback) in enumerate(button_info):
            button = Button(
                text,
                (center_x, start_y + i * (button_height + button_spacing)),
                button_width,
                button_height,
                callback
            )
            self.buttons.append(button)

        self.next_screen = None

    def draw_gradient_background(self):
        """
        Draw a vertical gradient background (top: blue, bottom: purple).
        """
        top_color = (50, 150, 255)  # lightblue
        bottom_color = (80, 0, 160)  # purple
        height = self.screen.get_height()
        for y in range(height):
            color_ratio = y / height
            r = top_color[0] * (1 - color_ratio) + bottom_color[0] * color_ratio
            g = top_color[1] * (1 - color_ratio) + bottom_color[1] * color_ratio
            b = top_color[2] * (1 - color_ratio) + bottom_color[2] * color_ratio
            pygame.draw.line(self.screen, (int(r), int(g), int(b)), (0, y), (self.screen.get_width(), y))

    def run(self):
        """
        Run the main menu loop. Waits for button input and returns the selected next screen.

        Returns:
            str: Identifier for the next screen ("play", "console", etc.)
        """
        clock = pygame.time.Clock()
        while True:
            self.draw_gradient_background()

            # Draw title
            title_surf = self.font.render("Shadow Guide", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 80))
            self.screen.blit(title_surf, title_rect)

            # Handle input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                for button in self.buttons:
                    button.handle_event(event)

            # Draw all buttons
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

            # Return to main loop when a button is pressed
            if self.next_screen:
                return self.next_screen

    # ===== Button callback methods =====
    def goto_play(self):
        self.next_screen = "play"

    def goto_console(self):
        self.next_screen = "console"

    def goto_records(self):
        self.next_screen = "records"

    def goto_stats(self):
        self.next_screen = "stats"

    def exit_game(self):
        self.next_screen = "exit"
