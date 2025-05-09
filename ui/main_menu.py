import pygame


class Button:
    def __init__(self, text, pos, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.callback = callback
        self.color_idle = (50, 50, 50)
        self.color_hover = (100, 100, 100)
        self.border_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

    def draw(self, screen):
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()


class MainMenu:
    def __init__(self, screen):
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

        for i, (text, callback) in enumerate(button_info):
            button = Button(
                text,
                (center_x, start_y + i * (button_height + button_spacing)),
                button_width,
                button_height,
                callback
            )
            self.buttons.append(button)

        self.next_screen = None  # ⭐ ไว้ return หน้าใหม่ตอนกดปุ่ม

    def draw_gradient_background(self):
        """วาดพื้นหลังแบบไล่สี"""
        top_color = (50, 150, 255)  # ฟ้า
        bottom_color = (80, 0, 160)  # ม่วง
        height = self.screen.get_height()
        for y in range(height):
            color_ratio = y / height
            r = top_color[0] * (1 - color_ratio) + bottom_color[0] * color_ratio
            g = top_color[1] * (1 - color_ratio) + bottom_color[1] * color_ratio
            b = top_color[2] * (1 - color_ratio) + bottom_color[2] * color_ratio
            pygame.draw.line(self.screen, (int(r), int(g), int(b)), (0, y), (self.screen.get_width(), y))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw_gradient_background()

            title_surf = self.font.render("Shadow Guide", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 80))
            self.screen.blit(title_surf, title_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                for button in self.buttons:
                    button.handle_event(event)

            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

            # ⭐ ถ้า next_screen ถูก set หลังจากกดปุ่ม
            if self.next_screen:
                return self.next_screen

    # ⭐ Callback ฟังก์ชันสำหรับปุ่ม
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
