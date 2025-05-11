# 🌑 Shadow Guide

**Shadow Guide** is a 2D platformer game built with Python and Pygame.  
Players must navigate each level, dodge intelligent enemies, and rely on an AI helper that offers real-time strategic
hints.

---

## 🎮 Gameplay Features

- 🧠 **AI Helper**: Provides context-sensitive hints (e.g., “Jump Now!”, “Go Left!”) based on proximity to traps,
  enemies, and goal.
- ⚔️ **Enemy Types**:
    - **Patrolling**, **Chasing**, **Jumping**
    - **Shooting** (with bullets), **Exploding**
    - **Teleporting** (reappears near player), **Dropping** (falls from ceiling)
- ⚡ **Player Abilities**:
    - Double Jump
    - Energy-based Dash
- 💾 **Data Logging**: All game stats (jump count, deaths, AI hints, score, etc.) are logged to CSV.
- 📊 **Statistics Dashboard**:
    - Recent stats, statistical summaries, and visualizations (bar chart, pie chart, line chart, heatmap).

---

## 🗂 Installation

1. Clone this repository:

```bash
cd to your directory
git clone https://github.com/TSpoomM/Shadow_Guide.git
cd shadow_guide
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

---

## 🚀 Controls

- ← / → or A / D: Move Left / Right
- SPACE / W: Jump / Double Jump (if energy)
- SHIFT: Dash (uses energy, cooldown applies)
- B: Return to main menu if passed or failed
- ENTER / Y: Proceed to next level
- N: Return to main menu
- 1/2/3/4: View Graphs (on statistics page)

---

## Requirements

See `requirements.txt`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more info.

---

## 👤 Credits

Developed as part of an academic game analytics project using:

- Python + Pygame
- Matplotlib, Seaborn
- Tkinter

---