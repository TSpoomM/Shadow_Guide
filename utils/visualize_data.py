import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
import statistics


class Visualizer:
    FILE_PATH = "game_data.csv"

    @staticmethod
    def load_recent_stats():
        if not os.path.exists(Visualizer.FILE_PATH):
            return None

        with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            reader = list(reader)

            if not reader:
                return None

            last = reader[-1]

            return {
                "Player": last.get("player_name", "?").strip(),
                "Level": last.get("level_score") or last.get("level", "?"),
                "Jump Count": last.get("jump_count", "?"),
                "Death Count": last.get("death_count", "?"),
                "Avg Time Between Jumps": round(float(last.get("avg_jump_interval", "0.0")), 3),
                "Hints Given": last.get("hint_count", "?"),
                "Enemy Encounters": last.get("enemy_triggered", "?")
            }

    @staticmethod
    def get_statistical_summary():
        if not os.path.exists(Visualizer.FILE_PATH):
            return {}

        try:
            with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                reader.fieldnames = [name.strip() for name in reader.fieldnames]
                reader = list(reader)

            if not reader:
                return {}

            df = {
                "jump_count": [int(r.get("jump_count", 0)) for r in reader],
                "death_count": [int(r.get("death_count", 0)) for r in reader],
                "avg_jump_interval": [float(r.get("avg_jump_interval", 0.0)) for r in reader],
                "hint_count": [int(r.get("hint_count", 0)) for r in reader],
                "enemy_triggered": [int(r.get("enemy_triggered", 0)) for r in reader],
                "level": [int(r.get("level", 0)) for r in reader],
            }

            # Hints per level
            level_hints = defaultdict(list)
            for r in reader:
                lvl = int(r.get("level", 0))
                hints = int(r.get("hint_count", 0))
                level_hints[lvl].append(hints)

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

    @staticmethod
    def show_bar_chart():
        level_jumps = defaultdict(list)
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    level = int(row.get("level", 0))
                    jump = int(row.get("jump_count", 0))
                    level_jumps[level].append(jump)
                except:
                    continue

        levels = sorted(level_jumps)
        avg_jumps = [sum(v) / len(v) for v in [level_jumps[l] for l in levels]]

        plt.figure()
        plt.bar(levels, avg_jumps)
        plt.xlabel("Level")
        plt.ylabel("Average Jump Count")
        plt.title("Jump Count per Level")
        plt.xticks(levels)
        plt.show()

    @staticmethod
    def show_line_chart():
        level_deaths = defaultdict(list)
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    level = int(row.get("level", 0))
                    deaths = int(row.get("death_count", 0))
                    level_deaths[level].append(deaths)
                except:
                    continue

        levels = sorted(level_deaths)
        total_deaths = [sum(level_deaths[l]) for l in levels]

        plt.figure()
        plt.plot(levels, total_deaths, marker="o")
        plt.xlabel("Level")
        plt.ylabel("Total Deaths")
        plt.title("Deaths per Level")
        plt.grid(True)
        plt.xticks(levels)
        plt.show()

    @staticmethod
    def show_pie_chart():
        hint_counter = Counter()
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    hint_counter["Hints"] += int(row.get("hint_count", 0))
                except:
                    continue

        plt.figure()
        plt.pie(hint_counter.values(), labels=hint_counter.keys(), autopct="%1.1f%%", startangle=140)
        plt.title("AI Hints Distribution")
        plt.axis("equal")
        plt.show()

    @staticmethod
    def show_heatmap():
        xy_counter = defaultdict(int)
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                try:
                    x = (i * 5) % 10
                    y = (i * 3) % 10
                    xy_counter[(x, y)] += int(row.get("enemy_triggered", 0))
                except:
                    continue

        heat = [[0] * 10 for _ in range(10)]
        for (x, y), count in xy_counter.items():
            heat[y][x] = count

        plt.figure()
        sns.heatmap(heat, cmap="YlOrRd", annot=True, fmt="d")
        plt.title("Enemy Encounters Heatmap (simulated)")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()
