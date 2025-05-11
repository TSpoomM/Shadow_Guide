import pygame
import random
import os
from ui.main_menu import MainMenu
from ui.play_screen import PlayScreen
from ui.console_screen import ConsoleScreen
from ui.records_screen import RecordsScreen
from ui.stats_screen import StatsScreen
from ui.name_input_screen import NameInputScreen


class ShadowGuideGame:
    """
    The main class that manages the game loop and screen transitions.
    Handles game start, level progression, and navigation between UI screens.
    """

    def __init__(self):
        """
        Initializes Pygame, window configuration, and default game state.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Shadow Guide")
        self.font = pygame.font.SysFont(None, 32)
        self.clock = pygame.time.Clock()

        # Load all level map paths
        self.level_maps = self.load_maps("assets/levels")
        self.used_maps = []
        self.current_screen = MainMenu(self.screen)
        self.level = 0
        self.player_name = None

    def load_maps(self, path):
        """
        Loads all .txt map files from the specified directory.

        Args:
            path (str): Directory path where level maps are stored.

        Returns:
            list[str]: Sorted list of map file paths.
        """
        maps = []
        if not os.path.exists(path):
            print(f"❌ Folder not found: {path}")
            return maps
        for file in os.listdir(path):
            if file.endswith(".txt"):
                maps.append(os.path.join(path, file))
        return sorted(maps)

    def run(self):
        """
        Main game loop. Handles screen changes based on user navigation or game events.
        """
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
                self.player_name = None  # Ask for player name only once

            elif isinstance(next_screen, str) and next_screen.startswith("play"):
                # Prompt for name on first play
                if not self.player_name:
                    name_input = NameInputScreen(self.screen)
                    self.player_name = name_input.run()
                    if not self.player_name:
                        continue  # Player cancelled

                map_choice = self.get_next_map(previous_map)
                if map_choice == "all_maps_completed":
                    result = self.show_finish_screen()
                    if result == "home":
                        self.current_screen = MainMenu(self.screen)
                        self.level = 0
                        self.used_maps = []
                        self.player_name = None
                    continue

                previous_map = map_choice
                self.current_screen = PlayScreen(self.screen, map_choice, self.level, self.player_name)

            elif next_screen == "level_complete":
                self.level += 1
                map_choice = self.get_next_map(previous_map)
                if map_choice == "all_maps_completed":
                    result = self.show_finish_screen()
                    if result == "home":
                        self.current_screen = MainMenu(self.screen)
                        self.level = 0
                        self.used_maps = []
                        self.player_name = None
                    continue

                previous_map = map_choice
                self.current_screen = PlayScreen(self.screen, map_choice, self.level, self.player_name)

            elif next_screen == "console":
                self.current_screen = ConsoleScreen(self.screen)

            elif next_screen == "records":
                self.current_screen = RecordsScreen(self.screen)

            elif next_screen == "stats":
                self.current_screen = StatsScreen(self.screen)

            self.clock.tick(60)

        pygame.quit()

    def get_next_map(self):
        """
        Selects the next map to load. Skips already used maps and starts with level0.

        Returns:
            str: Path to the next map, or "all_maps_completed"
        """
        if not self.level_maps:
            raise FileNotFoundError("❌ No Map In - assets/levels")

        # Level 0 map is fixed
        if self.level == 0:
            for map_path in self.level_maps:
                if "level0.txt" in map_path:
                    return map_path

        # Select random unused map
        available_maps = [m for m in self.level_maps if "level0.txt" not in m and m not in self.used_maps]
        if not available_maps:
            return "all_maps_completed"

        choice = random.choice(available_maps)
        self.used_maps.append(choice)
        return choice

    def show_finish_screen(self):
        """
        Displays the final screen after completing all maps.
        Shows average score and allows return to main menu.

        Returns:
            str: "home" or "exit"
        """
        clock = pygame.time.Clock()
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        title_font = pygame.font.SysFont(None, 64, bold=True)
        text_font = pygame.font.SysFont(None, 40)
        button_font = pygame.font.SysFont(None, 32, bold=True)

        try:
            average_score = sum(self.current_screen.total_score_list) / len(self.current_screen.total_score_list)
        except:
            average_score = 0

        while True:
            self.screen.fill((0, 0, 0))

            # 🎉 Title
            msg1 = title_font.render("✅ You Finished All Maps!", True, (0, 255, 0))
            self.screen.blit(msg1, msg1.get_rect(center=(center_x, center_y - 100)))

            # 📊 Score
            msg2 = text_font.render(f"Average Score: {average_score:.2f}/10", True, (255, 255, 255))
            self.screen.blit(msg2, msg2.get_rect(center=(center_x, center_y - 30)))

            # 🔘 Button: B to home
            back_rect = pygame.Rect(center_x - 100, center_y + 30, 200, 45)
            pygame.draw.rect(self.screen, (50, 50, 200), back_rect, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 2, border_radius=8)

            back_text = button_font.render("Back to Home (B)", True, (255, 255, 255))
            self.screen.blit(back_text, back_text.get_rect(center=back_rect.center))

            # Footer
            footer = self.font.render("Press B to return Home", True, (180, 180, 180))
            self.screen.blit(footer, footer.get_rect(center=(center_x, center_y + 110)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        return "home"

            clock.tick(30)


if __name__ == "__main__":
    game = ShadowGuideGame()
    game.run()
