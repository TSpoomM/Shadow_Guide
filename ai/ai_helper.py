from collections import defaultdict


class AIHelper:
    def __init__(self, player, platforms, enemies, goal):
        """
        Initialize the AIHelper with references to the game environment.

        Args:
            player: The player object.
            platforms: List of platform Rects in the level.
            enemies: Group of enemy objects in the level.
            goal: Rect representing the goal position.
        """
        self.player = player
        self.platforms = platforms
        self.enemies = enemies
        self.goal = goal
        self.hint_counter = defaultdict(int)

    def get_hints(self):
        """
        Analyze the current game state and generate context-aware hints for the player.
        Returns:
            List of string hints (e.g., "Jump Now!", "Go Right!")
        """
        hints = []

        # 1. Jump Now (close to trap)
        if self.is_near_gap():
            hints.append("Jump Now!")
            self.hint_counter["Jump Now!"] += 1

        # 2. Enemy Close
        if self.is_enemy_close():
            hints.append("Enemy Close!")
            self.hint_counter["Enemy Close!"] += 1

        # 3. Almost There
        if self.is_near_goal():
            hints.append("Almost There!")
            self.hint_counter["Almost There!"] += 1

        # 4. Go Left / Go Right / Be Careful
        direction_hint = self.analyze_direction()
        if direction_hint:
            hints.append(direction_hint)
            self.hint_counter[direction_hint] += 1

        return hints

    def is_near_gap(self):
        """
        Check if there is no platform ahead of the player, indicating a potential fall.

        Returns:
            True if there's a gap ahead, False otherwise.
        """
        check_distance = 40
        check_rect = self.player.rect.move(check_distance, 5)
        for plat, _ in self.platforms:
            if plat.colliderect(check_rect):
                return False
        return True

    def is_enemy_close(self):
        """
        Check if any enemy is within a dangerous proximity to the player.

        Returns:
            True if an enemy is close, False otherwise.
        """
        for enemy in self.enemies:
            if abs(enemy.rect.centerx - self.player.rect.centerx) < 100 and abs(
                    enemy.rect.centery - self.player.rect.centery) < 80:
                return True
        return False

    def is_near_goal(self):
        """
        Check if the player is within a reasonable distance of the level's goal.

        Returns:
            True if the player is near the goal, False otherwise.
        """
        if self.goal and abs(self.goal.centerx - self.player.rect.centerx) < 200:
            return True
        return False

    def analyze_direction(self):
        """
        Evaluate the left and right directions to suggest a safer path.

        Returns:
            A string hint: "Go Left!", "Go Right!", or "Be Careful!" depending on threats and terrain.
        """
        left_risk = 0
        right_risk = 0

        for enemy in self.enemies:
            if enemy.rect.centerx < self.player.rect.centerx and abs(
                    enemy.rect.centerx - self.player.rect.centerx) < 150:
                left_risk += 3
            if enemy.rect.centerx > self.player.rect.centerx and abs(
                    enemy.rect.centerx - self.player.rect.centerx) < 150:
                right_risk += 3

        left_gap = True
        right_gap = True
        for plat, _ in self.platforms:
            if plat.colliderect(self.player.rect.move(-40, 5)):
                left_gap = False
            if plat.colliderect(self.player.rect.move(40, 5)):
                right_gap = False
        if left_gap:
            left_risk += 5
        if right_gap:
            right_risk += 5

        if left_risk < right_risk:
            return "Go Left!"
        elif right_risk < left_risk:
            return "Go Right!"
        else:
            return "Be Careful!"
