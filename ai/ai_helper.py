class AIHelper:
    def __init__(self, player, platforms, enemies, goal):
        self.player = player
        self.platforms = platforms
        self.enemies = enemies
        self.goal = goal

    def get_hints(self):
        hints = []

        # 1. Jump Now (close to trap)
        if self.is_near_gap():
            hints.append("Jump Now!")

        # 2. Enemy Close
        if self.is_enemy_close():
            hints.append("Enemy Close!")

        # 3. Almost There
        if self.is_near_goal():
            hints.append("Almost There!")

        # 4. Go Left / Go Right
        direction_hint = self.analyze_direction()
        if direction_hint:
            hints.append(direction_hint)

        return hints

    def is_near_gap(self):
        check_distance = 40  # pixel ข้างหน้า
        check_rect = self.player.rect.move(check_distance, 5)
        for plat, _ in self.platforms:
            if plat.colliderect(check_rect):
                return False
        return True

    def is_enemy_close(self):
        for enemy in self.enemies:
            if abs(enemy.rect.centerx - self.player.rect.centerx) < 100 and abs(
                    enemy.rect.centery - self.player.rect.centery) < 80:
                return True
        return False

    def is_near_goal(self):
        if self.goal and abs(self.goal.centerx - self.player.rect.centerx) < 200:
            return True
        return False

    def analyze_direction(self):
        left_risk = 0
        right_risk = 0

        # Enemy risk
        for enemy in self.enemies:
            if enemy.rect.centerx < self.player.rect.centerx and abs(
                    enemy.rect.centerx - self.player.rect.centerx) < 150:
                left_risk += 3
            if enemy.rect.centerx > self.player.rect.centerx and abs(
                    enemy.rect.centerx - self.player.rect.centerx) < 150:
                right_risk += 3

        # Gap risk
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

        # Decision
        if left_risk < right_risk:
            return "Go Left!"
        elif right_risk < left_risk:
            return "Go Right!"
        else:
            return "Be Careful!"
