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
        self.used_maps = []
        self.current_screen = MainMenu(self.screen)
        self.level = 0  # ⭐ เริ่มที่ level 0

    def load_maps(self, path):
        maps = []
        if not os.path.exists(path):
            print(f"❌ Folder not found: {path}")
            return maps
        for file in os.listdir(path):
            if file.endswith(".txt"):
                maps.append(os.path.join(path, file))
        return sorted(maps)

    def run(self):
        running = True
        previous_map = None

        while running:
            next_screen = self.current_screen.run()
            if next_screen == "exit":
                running = False
            elif next_screen == "home":
                self.current_screen = MainMenu(self.screen)
                self.level = 0
                self.used_maps = []
            elif isinstance(next_screen, str) and next_screen.startswith("play"):
                if not self.level_maps:
                    print("❌ No Map In - assets/levels")
                    continue
                map_choice = self.get_next_map(previous_map)
                if map_choice == "all_maps_completed":
                    result = self.show_finish_screen()
                    if result == "home":
                        self.current_screen = MainMenu(self.screen)
                        self.level = 0
                        self.used_maps = []
                    continue
                previous_map = map_choice
                self.current_screen = PlayScreen(self.screen, map_choice, self.level)
            elif next_screen == "level_complete":
                self.level += 1
                map_choice = self.get_next_map(previous_map)
                if map_choice == "all_maps_completed":
                    result = self.show_finish_screen()
                    if result == "home":
                        self.current_screen = MainMenu(self.screen)
                        self.level = 0
                        self.used_maps = []
                    continue
                previous_map = map_choice
                self.current_screen = PlayScreen(self.screen, map_choice, self.level)
            elif next_screen == "settings":
                self.current_screen = SettingsScreen(self.screen)
            elif next_screen == "records":
                self.current_screen = RecordsScreen(self.screen)
            elif next_screen == "stats":
                self.current_screen = StatsScreen(self.screen)

            self.clock.tick(60)

        pygame.quit()

    def get_next_map(self, previous_map):
        if not self.level_maps:
            raise FileNotFoundError("❌ No Map In - assets/levels")

        if self.level == 0:
            for map_path in self.level_maps:
                if "level0.txt" in map_path:
                    return map_path

        available_maps = [m for m in self.level_maps if "level0.txt" not in m and m not in self.used_maps]
        if not available_maps:
            return "all_maps_completed"

        choice = random.choice(available_maps)
        self.used_maps.append(choice)
        return choice

    def show_finish_screen(self):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 50)

        # ⭐ โชว์คะแนนเฉลี่ย
        try:
            average_score = sum(self.current_screen.total_score_list) / len(self.current_screen.total_score_list)
        except:
            average_score = 0

        while True:
            self.screen.fill((0, 0, 0))
            msg1 = font.render("🎉 You Finished All Maps!", True, (0, 255, 0))
            msg2 = font.render(f"Average Score: {average_score:.2f}/10", True, (255, 255, 255))
            msg3 = font.render("Press B to return Home", True, (200, 200, 200))
            self.screen.blit(msg1, (100, 200))
            self.screen.blit(msg2, (150, 260))
            self.screen.blit(msg3, (140, 320))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    return "home"

            clock.tick(30)


if __name__ == "__main__":
    game = ShadowGuideGame()
    game.run()
