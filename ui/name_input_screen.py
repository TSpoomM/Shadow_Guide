# ui/name_input_screen.py

import pygame


class NameInputScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.input_text = ""
        self.prompt_text = "Enter your name:"
        self.next_screen = None

    def run(self):
        input_active = True

        while input_active:
            self.screen.fill((20, 20, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.input_text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 16:
                            self.input_text += event.unicode

            # Render texts
            prompt_surf = self.font.render(self.prompt_text, True, (255, 255, 255))
            input_surf = self.font.render(self.input_text, True, (0, 255, 255))
            prompt_rect = prompt_surf.get_rect(center=(self.screen.get_width() // 2, 200))
            input_rect = input_surf.get_rect(center=(self.screen.get_width() // 2, 260))

            self.screen.blit(prompt_surf, prompt_rect)
            self.screen.blit(input_surf, input_rect)

            pygame.display.flip()
            self.clock.tick(30)
