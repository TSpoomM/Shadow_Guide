import pygame
import random
import os
from ui.main_menu import MainMenu
from ui.play_screen import PlayScreen
from ui.settings_screen import SettingsScreen
from ui.records_screen import RecordsScreen
from ui.stats_screen import StatsScreen


class ShadowGuideGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Shadow Guide")
        self.clock = pygame.time.Clock()
        self.level_maps = self.load_maps("assets/levels")
        self.current_screen = MainMenu(self.screen)
        self.level = 1

    def load_maps(self, path):
        maps = []
        if not os.path.exists(path):
            print(f"❌ Folder not found: {path}")
            return maps
        for file in os.listdir(path):
            if file.endswith(".txt"):
                maps.append(os.path.join(path, file))
        return maps

    def run(self):
        running = True
        previous_map = None

        while running:
            next_screen = self.current_screen.run()
            if next_screen == "exit":
                running = False
            elif next_screen == "home":
                self.current_screen = MainMenu(self.screen)
            elif isinstance(next_screen, str) and next_screen.startswith("play"):
                if not self.level_maps:
                    print("❌ No Map In - assets/levels")
                    continue
                map_choice = self.get_random_map(previous_map)
                previous_map = map_choice
                self.current_screen = PlayScreen(self.screen, map_choice, self.level)
            elif next_screen == "level_complete":
                self.level += 1
                self.current_screen = MainMenu(self.screen)
            elif next_screen == "settings":
                self.current_screen = SettingsScreen(self.screen)
            elif next_screen == "records":
                self.current_screen = RecordsScreen(self.screen)
            elif next_screen == "stats":
                self.current_screen = StatsScreen(self.screen)
            self.clock.tick(60)

        pygame.quit()

    def get_random_map(self, previous_map):
        if not self.level_maps:
            raise FileNotFoundError("❌ No Map In - assets/levels")
        if len(self.level_maps) == 1:
            return self.level_maps[0]
        choice = random.choice(self.level_maps)
        while choice == previous_map:
            choice = random.choice(self.level_maps)
        return choice


if __name__ == "__main__":
    game = ShadowGuideGame()
    game.run()
