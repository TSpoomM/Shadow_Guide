import random
from entities.enemy import (
    PatrollingEnemy,
    ChasingEnemy,
    JumpingEnemy,
    ShootingEnemy,
    ExplodingEnemy,
    TeleportingEnemy,
    DroppingEnemy
)


class EnemyFactory:
    """
    EnemyFactory dynamically creates enemies based on the current level difficulty.
    Uses weighted random selection from a predefined enemy pool per level.
    """
    # Define which enemy types can spawn at each level, with weight probabilities
    WEIGHTED_ENEMY_POOL = {
        1: [
            (PatrollingEnemy, 1.0)
        ],
        2: [
            (PatrollingEnemy, 0.6),
            (ChasingEnemy, 0.4)
        ],
        3: [
            (PatrollingEnemy, 0.4),
            (ChasingEnemy, 0.3),
            (JumpingEnemy, 0.3)
        ],
        4: [
            (ChasingEnemy, 0.3),
            (JumpingEnemy, 0.2),
            (ShootingEnemy, 0.3),
            (TeleportingEnemy, 0.2)
        ],
        5: [
            (JumpingEnemy, 0.2),
            (ShootingEnemy, 0.25),
            (ExplodingEnemy, 0.3),
            (TeleportingEnemy, 0.15),
            (DroppingEnemy, 0.1)
        ]
    }

    @staticmethod
    def create_random(x, y, level):
        """
        Randomly selects an enemy class based on level difficulty and spawns it at (x, y).

        Args:
            x (int): X position of the enemy spawn.
            y (int): Y position of the enemy spawn.
            level (int): The current level, used to scale difficulty.

        Returns:
            EnemyBase: An instance of a randomly selected enemy subclass.
        """
        # Ensure level stays within 1–5
        level = max(1, min(level, 5))

        pool = EnemyFactory.WEIGHTED_ENEMY_POOL[level]
        classes = [cls for cls, _ in pool]
        weights = [w for _, w in pool]

        # Use weighted random choice to select an enemy class
        chosen_cls = random.choices(classes, weights=weights, k=1)[0]
        return chosen_cls(x, y)
