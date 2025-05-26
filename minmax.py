import os
import pandas as pd

folder_path = r'C:\Users\Rosh05\Desktop\data\screw_csvs'  # Your folder path

summary_data = []

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        min_torque = df['torque_result'].min()
        max_torque = df['torque_result'].max()
        min_angle = df['angle_result'].min()
        max_angle = df['angle_result'].max()
        
        summary_data.append({
            'filename': filename,
            'min_torque': min_torque,
            'max_torque': max_torque,
            'min_angle': min_angle,
            'max_angle': max_angle
        })

summary_df = pd.DataFrame(summary_data)

# Save summary CSV in the same folder
output_path = os.path.join(folder_path, 'summary_min_max.csv')
summary_df.to_csv(output_path, index=False)

print(f"Summary saved to {output_path}")
