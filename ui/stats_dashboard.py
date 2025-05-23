import csv
import seaborn as sns
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatsDashboard(tk.Tk):
    """
        A dashboard UI (using Tkinter) for displaying game statistics.
        Contains bar chart, line chart, pie chart, and heatmap based on CSV data.
        """

    def __init__(self):
        """
        Initializes the dashboard window, layout, and chart buttons.
        """
        super().__init__()
        self.title("Statistics Dashboard")
        self.geometry("900x700")
        self.current_charts = {}
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        """
        Creates the toggle buttons and content frame for embedding charts.
        """
        self.toggle_frame = tk.Frame(self)
        self.toggle_frame.pack(pady=10)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        charts = [
            ("Avg Jump Count Per Level", self.plot_bar_chart),
            ("Total Death Per Level", self.plot_line_chart),
            ("Ai Hint Type Distribution", self.plot_pie_chart),
            ("Enemy Encounter", self.plot_heatmap)
        ]

        # Create toggle buttons
        for label, func in charts:
            b = ttk.Button(self.toggle_frame, text=label,
                           command=lambda l=label, f=func: self.toggle_chart(l, f))
            b.pack(side=tk.LEFT, padx=10)

        # Close button
        ttk.Button(self, text="Close", command=self.on_close).pack(pady=5)

    def on_close(self):
        """
        Destroys all charts and closes the window.
        """
        for widget in self.current_charts.values():
            widget.destroy()
        self.current_charts.clear()
        self.destroy()

    def read_game_data(self):
        """
        Reads and parses the game_data.csv file.

        Returns:
            list[dict]: List of records (each row) as dictionaries.
        """
        with open("game_data.csv", "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [h.strip() for h in reader.fieldnames]
            return list(reader)

    def toggle_chart(self, name, plot_fn):
        """
        Displays a chart and hides the previous one.

        Args:
            name (str): Chart label name.
            plot_fn (function): Function that returns a matplotlib figure.
        """
        for widget in self.current_charts.values():
            widget.destroy()
        self.current_charts.clear()

        chart = plot_fn()
        if chart:
            self.current_charts[name] = chart

    def embed_plot(self, fig):
        """
        Embeds a matplotlib figure into the Tkinter frame.

        Args:
            fig (matplotlib.Figure): The figure to embed.

        Returns:
            widget: The Tkinter canvas widget.
        """
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        plt.close(fig)
        return widget

    def plot_bar_chart(self):
        """
        Plots a bar chart of average jump count per level.
        """
        data = self.read_game_data()
        level_jumps = defaultdict(list)
        for row in data:
            try:
                level = int(row.get("level", 0))
                jump = int(row.get("jump_count", 0))
                level_jumps[level].append(jump)
            except:
                continue

        if not level_jumps:
            return None

        levels = sorted(level_jumps)
        avg_jumps = [sum(v) / len(v) for v in [level_jumps[l] for l in levels]]

        fig, ax = plt.subplots()
        ax.bar(levels, avg_jumps, color="skyblue")
        ax.set_title("Average Jump Count per Level")
        ax.set_xlabel("Level")
        ax.set_ylabel("Jump Count")
        ax.set_xticks(levels)
        return self.embed_plot(fig)

    def plot_line_chart(self):
        """
        Plots a line chart showing total deaths per level.
        """
        data = self.read_game_data()
        level_deaths = defaultdict(list)
        for row in data:
            try:
                level = int(row.get("level", 0))
                deaths = int(row.get("death_count", 0))
                level_deaths[level].append(deaths)
            except:
                continue

        if not level_deaths:
            return None

        levels = sorted(level_deaths)
        total_deaths = [sum(level_deaths[l]) for l in levels]

        fig, ax = plt.subplots()
        ax.plot(levels, total_deaths, marker="o", color="tomato")
        ax.set_title("Total Deaths per Level")
        ax.set_xlabel("Level")
        ax.set_ylabel("Deaths")
        ax.grid(True)
        ax.set_xticks(levels)
        return self.embed_plot(fig)

    def plot_pie_chart(self):
        """
        Plots a pie chart of hint usage distribution by type.
        """
        data = self.read_game_data()
        hint_totals = defaultdict(int)
        for row in data:
            for hint_key, label in [
                ("hint_jump_now", "Jump Now!"),
                ("hint_enemy_close", "Enemy Close!"),
                ("hint_almost_there", "Almost There!"),
                ("hint_go_left", "Go Left!"),
                ("hint_go_right", "Go Right!"),
                ("hint_be_careful", "Be Careful!")
            ]:
                try:
                    hint_totals[label] += int(row.get(hint_key, 0))
                except:
                    continue

        labels = list(hint_totals.keys())
        sizes = list(hint_totals.values())

        if sum(sizes) == 0:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, 'No Hint Data Available', ha='center', va='center')
            ax.axis('off')
            return self.embed_plot(fig)

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title("AI Hint Type Distribution")
        ax.axis("equal")
        return self.embed_plot(fig)

    def plot_heatmap(self):
        """
        Plots a simulated heatmap of enemy encounters based on CSV index.
        """
        data = self.read_game_data()
        xy_counter = defaultdict(int)
        for i, row in enumerate(data):
            try:
                x = (i * 5) % 10
                y = (i * 3) % 10
                xy_counter[(x, y)] += int(row.get("enemy_triggered", 0))
            except:
                continue

        if not xy_counter:
            return None

        heat = [[0] * 10 for _ in range(10)]
        for (x, y), count in xy_counter.items():
            heat[y][x] = count

        fig, ax = plt.subplots()
        sns.heatmap(heat, cmap="YlOrRd", annot=True, fmt="d", ax=ax)
        ax.set_title("Enemy Encounter Heatmap (simulated)")
        return self.embed_plot(fig)


def launch_stats_window():
    """
    Launches the statistics dashboard window (for embedding in game or debugging).
    """
    app = StatsDashboard()
    app.mainloop()
