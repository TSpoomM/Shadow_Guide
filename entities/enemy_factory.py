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
        level = max(1, min(level, 5))  # Clamp level 1-5

        pool = EnemyFactory.WEIGHTED_ENEMY_POOL[level]
        classes = [cls for cls, _ in pool]
        weights = [w for _, w in pool]

        chosen_cls = random.choices(classes, weights=weights, k=1)[0]
        return chosen_cls(x, y)
