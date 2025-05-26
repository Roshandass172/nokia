import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_every_19th_step(csv_path, start_range=1, end_range=19, step_gap=19, output_dir='plots'):
    # Load the CSV
    df = pd.read_csv(csv_path)

    # Ensure required columns exist
    if 'Step' not in df.columns or 'Angle_Value' not in df.columns:
        raise ValueError("CSV must contain 'Step' and 'Angle_Value' columns.")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for start in range(start_range, end_range + 1):
        selected_steps = list(range(start, df['Step'].max() + 1, step_gap))
        filtered_df = df[df['Step'].isin(selected_steps)].copy()

        # Limit to 679 points and assign palette numbers 1 to 679
        filtered_df = filtered_df.head(679)
        filtered_df['Palette'] = range(1, len(filtered_df) + 1)

        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(
            filtered_df['Palette'],
            filtered_df['Angle_Value'],
            color='red',
            linewidth=1
        )
        plt.title(f'Line Plot: Start Step = {start}')
        plt.xlabel('Palette Number (1 to 679)')
        plt.ylabel('Angle Value')

        # Add horizontal lines
        plt.axhline(y=5500, color='green', linestyle='--', linewidth=1.5, label='Max Threshold (5500)')
        plt.axhline(y=3200, color='blue', linestyle='--', linewidth=1.5, label='Min Threshold (2100)')

        # Optional: Add legend
        plt.legend()

        # Save plot
        plot_filename = os.path.join(output_dir, f'angle_line_start_{start}.png')
        plt.savefig(plot_filename, dpi=300)
        plt.close()

    print(f"Line plots saved to: {output_dir}")

# Run the function
plot_every_19th_step(
    csv_path=r"C:\Users\Rosh05\Desktop\data\merged_output.csv",
    output_dir=r"C:\Users\Rosh05\Desktop\data\graphs"
)
