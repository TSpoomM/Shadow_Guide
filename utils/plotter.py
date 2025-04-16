import pandas as pd
import matplotlib.pyplot as plt


class DataPlotter:
    @staticmethod
    def generate_graph(csv_path='game_data.csv', output_path='statistics_summary.png'):
        try:
            df = pd.read_csv(csv_path)

            fig, axs = plt.subplots(3, 1, figsize=(8, 10))

            axs[0].bar(df['level'], df['jump_count'], color='skyblue')
            axs[0].set_title('Jump Count per Level')
            axs[0].set_xlabel('Level')
            axs[0].set_ylabel('Jumps')

            axs[1].plot(df['level'], df['death_count'], marker='o', color='salmon')
            axs[1].set_title('Death Count per Level')
            axs[1].set_xlabel('Level')
            axs[1].set_ylabel('Deaths')

            axs[2].plot(df['level'], df['avg_jump_interval'], marker='x', color='green')
            axs[2].set_title('Average Time Between Jumps')
            axs[2].set_xlabel('Level')
            axs[2].set_ylabel('Seconds')

            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()
            return True
        except Exception as e:
            print(f'Error generating graph: {e}')
            return False
