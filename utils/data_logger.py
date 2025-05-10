import csv
import os


class DataLogger:
    FILE_PATH = "game_data.csv"
    HEADER = [
        "player_name", "level", "jump_count", "death_count",
        "avg_jump_interval", "hint_count", "enemy_triggered", "level_score",
        "hint_jump_now", "hint_enemy_close", "hint_almost_there",
        "hint_go_left", "hint_go_right", "hint_be_careful"
    ]

    @staticmethod
    def log(level, jump_count, death_count, avg_jump_interval, hint_count,
            enemy_triggered, level_score, player_name="Unknown", hint_counter=None):
        hcount = hint_counter or {}
        file_exists = os.path.isfile(DataLogger.FILE_PATH)

        with open(DataLogger.FILE_PATH, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(DataLogger.HEADER)
            writer.writerow([
                player_name, level, jump_count, death_count,
                round(avg_jump_interval, 3), hint_count, enemy_triggered, level_score,
                hcount.get("Jump Now!", 0),
                hcount.get("Enemy Close!", 0),
                hcount.get("Almost There!", 0),
                hcount.get("Go Left!", 0),
                hcount.get("Go Right!", 0),
                hcount.get("Be Careful!", 0)
            ])
