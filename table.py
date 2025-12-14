import pandas as pd
import matplotlib.pyplot as plt

def draw_tables():
    try:
        df = pd.read_csv('scheduler_results.csv')
    except FileNotFoundError:
        print("run simulation.py first to get scheduler_results.csv")
        return

    test_cases = df['Test Case'].unique()

    for test_case in test_cases:
        case_df = df[df['Test Case'] == test_case].copy()
        
        display_df = case_df.drop(columns=['Test Case'])
        
        if 'Avg Turnaround' in display_df.columns:
            display_df['Avg Turnaround'] = display_df['Avg Turnaround'].apply(lambda x: f'{x:.0f}')
        if 'Avg Response' in display_df.columns:
            display_df['Avg Response'] = display_df['Avg Response'].apply(lambda x: f'{x:.2f}')
        if 'Avg Waiting' in display_df.columns:
            display_df['Avg Waiting'] = display_df['Avg Waiting'].apply(lambda x: f'{x:.1f}')
        if 'Throughput' in display_df.columns:
            display_df['Throughput'] = display_df['Throughput'].apply(lambda x: f'{x:.2f}')

        fig, ax = plt.subplots(figsize=(12, 4)) 
        
        ax.axis('off')
        ax.axis('tight')
        
        table = ax.table(cellText=display_df.values,
                         colLabels=display_df.columns,
                         cellLoc='center',
                         loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        
        plt.title(test_case, fontsize=14, pad=20)
        
        plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    draw_tables()
