import csv
import tkinter as tk
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict


class StatsDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Statistics Dashboard")
        self.geometry("900x700")

        self.current_charts = {}
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        self.toggle_frame = tk.Frame(self)
        self.toggle_frame.pack(pady=10)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        charts = [
            ("jump count", self.plot_bar_chart),
            ("death count", self.plot_line_chart),
            ("hint count", self.plot_pie_chart),
            ("enemy triggered", self.plot_heatmap),
        ]

        for label, func in charts:
            b = ttk.Button(self.toggle_frame, text=label,
                           command=lambda l=label, f=func: self.toggle_chart(l, f))
            b.pack(side=tk.LEFT, padx=10)

        ttk.Button(self, text="Close", command=self.on_close).pack(pady=5)

    def on_close(self):
        for widget in self.current_charts.values():
            widget.destroy()
        self.current_charts.clear()
        self.destroy()

    def read_game_data(self):
        with open("game_data.csv", "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def toggle_chart(self, name, plot_fn):
        for widget in self.current_charts.values():
            widget.destroy()
        self.current_charts.clear()

        chart = plot_fn()
        self.current_charts[name] = chart

    def embed_plot(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        plt.close(fig)
        return widget

    def plot_bar_chart(self):
        data = self.read_game_data()
        level_jumps = defaultdict(list)
        for row in data:
            level = int(row["level"])
            level_jumps[level].append(int(row["jump_count"]))
        levels = sorted(level_jumps)
        avg_jumps = [sum(v) / len(v) for v in [level_jumps[l] for l in levels]]

        fig, ax = plt.subplots()
        ax.bar(levels, avg_jumps, color="skyblue")
        ax.set_title("Average Jump Count per Level")
        ax.set_xlabel("Level")
        ax.set_ylabel("Jump Count")
        return self.embed_plot(fig)

    def plot_line_chart(self):
        data = self.read_game_data()
        level_deaths = defaultdict(list)
        for row in data:
            level = int(row["level"])
            level_deaths[level].append(int(row["death_count"]))
        levels = sorted(level_deaths)
        total_deaths = [sum(level_deaths[l]) for l in levels]

        fig, ax = plt.subplots()
        ax.plot(levels, total_deaths, marker="o", color="tomato")
        ax.set_title("Total Deaths per Level")
        ax.set_xlabel("Level")
        ax.set_ylabel("Deaths")
        ax.grid(True)
        return self.embed_plot(fig)

    def plot_pie_chart(self):
        data = self.read_game_data()
        hint_total = sum(int(row["hint_count"]) for row in data)
        labels = ["Hints Used", "Other"]
        sizes = [hint_total, max(1, 100 - hint_total)]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title("AI Hint Usage")
        ax.axis("equal")
        return self.embed_plot(fig)

    def plot_heatmap(self):
        data = self.read_game_data()
        xy_counter = defaultdict(int)
        for i, row in enumerate(data):
            x = (i * 5) % 10
            y = (i * 3) % 10
            xy_counter[(x, y)] += int(row["enemy_triggered"])

        heat = [[0] * 10 for _ in range(10)]
        for (x, y), count in xy_counter.items():
            heat[y][x] = count

        fig, ax = plt.subplots()
        sns.heatmap(heat, cmap="YlOrRd", annot=True, fmt="d", ax=ax)
        ax.set_title("Enemy Encounter Heatmap")
        return self.embed_plot(fig)


def launch_stats_window():
    app = StatsDashboard()
    app.mainloop()
