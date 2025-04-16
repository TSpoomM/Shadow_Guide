import csv
import os


class DataLogger:
    FILE_PATH = 'game_data.csv'

    @staticmethod
    def initialize():
        if not os.path.exists(DataLogger.FILE_PATH):
            with open(DataLogger.FILE_PATH, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['level', 'jump_count', 'death_count', 'avg_jump_interval', 'hint_count'])

    @staticmethod
    def log(level, jump_count, death_count, avg_jump_interval, hint_count):
        DataLogger.initialize()
        with open(DataLogger.FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([level, jump_count, death_count, round(avg_jump_interval, 2), hint_count])
