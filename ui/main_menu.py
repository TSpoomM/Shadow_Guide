import pygame


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
        self.buttons = [
            ("Play", "play"),
            ("Settings", "settings"),
            ("Records", "records"),
            ("Statistics", "stats"),
            ("Exit", "exit")
        ]

    def run(self):
        while True:
            self.screen.fill((30, 30, 30))
            title = self.font.render("Shadow Guide", True, (255, 255, 255))
            self.screen.blit(title, (300, 50))

            for idx, (text, _) in enumerate(self.buttons):
                btn = self.font.render(text, True, (200, 200, 200))
                self.screen.blit(btn, (340, 150 + idx * 70))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for idx, (_, action) in enumerate(self.buttons):
                        if 340 <= x <= 540 and 150 + idx * 70 <= y <= 190 + idx * 70:
                            return action
