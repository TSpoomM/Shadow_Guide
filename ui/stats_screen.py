import pygame
import os
from utils.plotter import DataPlotter


class StatsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 40)
        self.image_path = "statistics_summary.png"
        self.graph = None

        # Generate graph on load
        success = DataPlotter.generate_graph()
        if success and os.path.exists(self.image_path):
            image = pygame.image.load(self.image_path)
            screen_w, screen_h = self.screen.get_size()
            self.graph = pygame.transform.scale(image, (screen_w, screen_h - 100))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((30, 30, 30))
            title = self.font.render("Statistics - Press B to go back", True, (255, 255, 255))
            self.screen.blit(title, (120, 20))

            if self.graph:
                self.screen.blit(self.graph, (0, 60))
            else:
                no_data = self.font.render("No statistics available.", True, (180, 180, 180))
                self.screen.blit(no_data, (200, 300))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    return "home"

            clock.tick(60)
