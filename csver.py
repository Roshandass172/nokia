import pandas as pd
import os

def generate_ok_screws(csv_path, output_dir, start_range=3, end_range=19, step_gap=19):
    # Load the CSV
    df = pd.read_csv(csv_path)

    # Ensure required columns exist
    required_columns = ['id', 'status', 'torque_low_limit', 'torque_high_limit', 'torque_result',
                        'angle_low_limit', 'angle_high_limit', 'angle_result']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Convert max id to integer
    max_id = int(df['id'].max())

    for start in range(start_range, end_range + 1):
        selected_ids = list(range(start, max_id + 1, step_gap))
        filtered_df = df[(df['id'].isin(selected_ids)) & (df['status'].str.lower() == 'ok')]

        # Select only the required columns
        result_df = filtered_df[[
            'torque_low_limit', 'torque_high_limit', 'torque_result',
            'angle_low_limit', 'angle_high_limit', 'angle_result'
        ]].copy()

        # Save to CSV
        output_file = os.path.join(output_dir, f'screw{start}.csv')
        result_df.to_csv(output_file, index=False)

    print(f"CSV files generated in: {output_dir}")

# === Run the function ===
generate_ok_screws(
    csv_path=r"C:\Users\Rosh05\Desktop\data\combined.csv",  # Update if needed
    output_dir=r"C:\Users\Rosh05\Desktop\data\screw_csvs"   # Update if needed
)
