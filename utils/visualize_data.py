import csv
import os
import statistics
from collections import defaultdict


class Visualizer:
    """
    A utility class for reading and analyzing gameplay statistics from a CSV log file.
    Provides functions for retrieving recent gameplay data and statistical summaries.
    """
    FILE_PATH = "game_data.csv"

    @staticmethod
    def load_recent_stats():
        """
        Loads and returns the most recent gameplay stats for the last recorded player.

        Returns:
            dict or None: Dictionary of recent stats (latest record) including:
                - Player name
                - Level
                - Jump count
                - Death count
                - Avg score per level (computed from same player records)
                - Avg jump interval
                - Hints used
                - Enemies encountered
        """
        if not os.path.exists(Visualizer.FILE_PATH):
            return None

        with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            reader = list(reader)

            if not reader:
                return None

            last = reader[-1]
            player = last.get("player_name", "?").strip()

            # Filter rows for the same player and valid level_score
            player_rows = [r for r in reader if r.get("player_name", "").strip() == player and r.get("level_score")]

            # Compute average score across all levels for this player
            try:
                scores = [float(r["level_score"]) for r in player_rows]
                avg_score = round(sum(scores) / len(scores), 2)
            except:
                avg_score = "?"

            return {
                "Player": player,
                "Level": last.get("level") or "?",
                "Jump Count": last.get("jump_count", "?"),
                "Death Count": last.get("death_count", "?"),
                "Avg Score Per Level": avg_score,
                "Avg Time Between Jumps": round(float(last.get("avg_jump_interval", "0.0")), 3),
                "Hints Given": last.get("hint_count", "?"),
                "Enemy Encounters": last.get("enemy_triggered", "?")
            }

    @staticmethod
    def get_statistical_summary():
        """
        Computes overall summary statistics from the full dataset.

        Returns:
            dict: A nested dictionary containing grouped stats:
                - Mean, Min, Max, and StdDev (SD) for jump count
                - Summary for death count
                - Summary for jump interval
                - Total and average AI hints
                - Median/max for enemy encounters
        """
        if not os.path.exists(Visualizer.FILE_PATH):
            return {}

        try:
            with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                reader.fieldnames = [name.strip() for name in reader.fieldnames]
                reader = list(reader)

            if not reader:
                return {}

            # Extract and convert values to numeric form
            df = {
                "jump_count": [int(r.get("jump_count", 0)) for r in reader],
                "death_count": [int(r.get("death_count", 0)) for r in reader],
                "avg_jump_interval": [float(r.get("avg_jump_interval", 0.0)) for r in reader],
                "hint_count": [int(r.get("hint_count", 0)) for r in reader],
                "enemy_triggered": [int(r.get("enemy_triggered", 0)) for r in reader],
                "level": [int(r.get("level", 0)) for r in reader],
            }

            # Group hints per level for averaging
            level_hints = defaultdict(list)
            for r in reader:
                lvl = int(r.get("level", 0))
                hints = int(r.get("hint_count", 0))
                level_hints[lvl].append(hints)

            # Compute average hints per level group
            avg_hint_per_level = round(sum(sum(v) / len(v) for v in level_hints.values()) / len(level_hints), 2)

            return {
                "Jump Count": {
                    "Mean": round(statistics.mean(df["jump_count"]), 2),
                    "Min": min(df["jump_count"]),
                    "Max": max(df["jump_count"]),
                    "SD": round(statistics.stdev(df["jump_count"]), 2) if len(df["jump_count"]) > 1 else 0.0
                },
                "Deaths": {
                    "Mean": round(statistics.mean(df["death_count"]), 2),
                    "Min": min(df["death_count"]),
                    "Max": max(df["death_count"])
                },
                "Avg Time Between Jumps": {
                    "Mean": round(statistics.mean(df["avg_jump_interval"]), 3),
                    "Min": round(min(df["avg_jump_interval"]), 3),
                    "Max": round(max(df["avg_jump_interval"]), 3)
                },
                "AI Hints Given": {
                    "Total": sum(df["hint_count"]),
                    "Avg per Level": avg_hint_per_level
                },
                "Enemy Encounters": {
                    "Median": statistics.median(df["enemy_triggered"]),
                    "Max": max(df["enemy_triggered"])
                }
            }

        except Exception as e:
            print("❌ Error in get_statistical_summary:", e)
            return {}
