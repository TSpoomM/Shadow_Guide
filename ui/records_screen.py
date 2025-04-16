import pygame


class RecordsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 40)

    def run(self):
        while True:
            self.screen.fill((80, 50, 50))
            text = self.font.render("Records Screen - Press B to go back", True, (255, 255, 255))
            self.screen.blit(text, (100, 250))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        return "home"
