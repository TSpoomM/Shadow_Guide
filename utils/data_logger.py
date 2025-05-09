# utils/data_logger.py

import csv
import os


class DataLogger:
    FILE_PATH = "game_data.csv"
    HEADERS = [
        "player_name",
        "level",
        "jump_count",
        "death_count",
        "avg_jump_interval",
        "hint_count",
        "enemy_triggered"
    ]

    @staticmethod
    def log(player_name, level, jump_count, death_count, avg_jump_interval, hint_count, enemy_triggered):
        file_exists = os.path.isfile(DataLogger.FILE_PATH)

        with open(DataLogger.FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=DataLogger.HEADERS)

            # เขียนหัวตารางถ้ายังไม่มี
            if not file_exists:
                writer.writeheader()

            # เขียนข้อมูล 1 แถว
            writer.writerow({
                "player_name": player_name,
                "level": level,
                "jump_count": jump_count,
                "death_count": death_count,
                "avg_jump_interval": round(avg_jump_interval, 3),
                "hint_count": hint_count,
                "enemy_triggered": enemy_triggered
            })
