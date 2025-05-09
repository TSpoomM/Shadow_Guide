# utils/visualize_data.py

import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict


class Visualizer:
    FILE_PATH = "game_data.csv"

    @staticmethod
    def load_recent_stats():
        if not os.path.exists(Visualizer.FILE_PATH):
            return None

        with open(Visualizer.FILE_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            if not reader:
                return None
            last = reader[-1]
            return {
                "Player": last["player_name"],
                "Level": last["level"],
                "Jump Count": last["jump_count"],
                "Death Count": last["death_count"],
                "Avg Time Between Jumps": round(float(last["avg_jump_interval"]), 3),
                "Hints Given": last["hint_count"],
                "Enemy Encounters": last["enemy_triggered"]
            }

    @staticmethod
    def get_statistical_summary():
        if not os.path.exists(Visualizer.FILE_PATH):
            return {}

        with open(Visualizer.FILE_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            if not reader:
                return {}

        import statistics

        try:
            # แปลง field ที่ต้องคำนวณ
            df = {
                "jump_count": [int(r["jump_count"]) for r in reader],
                "death_count": [int(r["death_count"]) for r in reader],
                "avg_jump_interval": [float(r["avg_jump_interval"]) for r in reader],
                "hint_count": [int(r["hint_count"]) for r in reader],
                "enemy_triggered": [int(r["enemy_triggered"]) for r in reader],
                "level": [int(r["level"]) for r in reader]
            }

            # รวม hint per level
            level_hints = {}
            for r in reader:
                lvl = int(r["level"])
                count = int(r["hint_count"])
                level_hints.setdefault(lvl, []).append(count)
            avg_hint_per_level = round(sum([sum(v) / len(v) for v in level_hints.values()]) / len(level_hints), 2)

            return {
                "Jump Count": {
                    "Mean": round(statistics.mean(df["jump_count"]), 2),
                    "Min": min(df["jump_count"]),
                    "Max": max(df["jump_count"]),
                    "SD": round(statistics.stdev(df["jump_count"]), 2)
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
        except:
            return {}

    @staticmethod
    def show_bar_chart():
        level_jumps = defaultdict(list)
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                level = int(row["level"])
                jump = int(row["jump_count"])
                level_jumps[level].append(jump)

        levels = sorted(level_jumps.keys())
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
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                level = int(row["level"])
                deaths = int(row["death_count"])
                level_deaths[level].append(deaths)

        levels = sorted(level_deaths.keys())
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
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                hint_counter["Hints"] += int(row["hint_count"])

        plt.figure()
        plt.pie(hint_counter.values(), labels=hint_counter.keys(), autopct="%1.1f%%", startangle=140)
        plt.title("AI Hints Distribution")
        plt.axis("equal")
        plt.show()

    @staticmethod
    def show_heatmap():
        xy_counter = defaultdict(int)
        # ปลอมตำแหน่งไว้ก่อน (เพราะ CSV ไม่มีจริง)
        # คุณสามารถเปลี่ยนให้จริงได้ถ้าเก็บตำแหน่งจริงในอนาคต
        with open(Visualizer.FILE_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # กระจายตำแหน่งจำลอง (ใช้ i เพื่อให้แตกต่าง)
                x = (i * 5) % 10
                y = (i * 3) % 10
                xy_counter[(x, y)] += int(row["enemy_triggered"])

        heat = [[0] * 10 for _ in range(10)]
        for (x, y), count in xy_counter.items():
            heat[y][x] = count

        plt.figure()
        sns.heatmap(heat, cmap="YlOrRd", annot=True, fmt="d")
        plt.title("Enemy Encounters Heatmap (simulated)")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()
