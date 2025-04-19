import pandas as pd
import time
import matplotlib.pyplot as plt
import os
import csv

file_paths = [
    "1.csv", "2.csv", "3.csv", "4.csv", "5.csv", "6.csv", "7.csv",
    *[f"synthetic_full_dataset_{i}.csv" for i in range(8, 32)]
]

TORQUE_COL = '#028_Torque3'
ANGLE_COL = '#032_Angle3'

# Output CSV setup
output_csv_path = "/home/ubuntu/Desktop/nokia/ai_adaptive_limits_log.csv"
with open(output_csv_path, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "Step",
        "Torque_Min", "Torque_Max", "Torque_Value",
        "Angle_Min", "Angle_Max", "Angle_Value"
    ])

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle('Live Monitoring with Value-Based Dynamic Limits')

torque_data = []
angle_data = []
x_data = []

count = 0
max_entries = 19

for file_path in file_paths:
    if not os.path.exists(file_path):
        continue

    df = pd.read_csv(file_path)

    if TORQUE_COL not in df.columns or ANGLE_COL not in df.columns:
        continue

    for _, row in df.iterrows():
        if count >= max_entries:
            break

        try:
            torque = float(row[TORQUE_COL])
            angle = float(row[ANGLE_COL])
        except:
            continue

        count += 1
        x_data.append(count)
        torque_data.append(torque)
        angle_data.append(angle)

        # Set limits dynamically based on current value
        torque_buffer = 0.5
        angle_buffer = 100.0

        torque_min = torque - torque_buffer
        torque_max = torque + torque_buffer
        angle_min = angle - angle_buffer
        angle_max = angle + angle_buffer

        # Check alerts
        torque_alert = not (torque_min <= torque <= torque_max)
        angle_alert = not (angle_min <= angle <= angle_max)

        print(f"[{count}] Torque3: {torque:.2f} | Angle3: {angle:.2f}")
        print(f"  Torque Limits: {torque_min:.2f} to {torque_max:.2f}")
        print(f"  Angle Limits: {angle_min:.2f} to {angle_max:.2f}")
        if torque_alert:
            print("  WARNING: Torque3 out of threshold")
        if angle_alert:
            print("  WARNING: Angle3 out of threshold")
        print("-" * 50)

        # Save to CSV
        with open(output_csv_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                count,
                round(torque_min, 2), round(torque_max, 2), round(torque, 2),
                round(angle_min, 2), round(angle_max, 2), round(angle, 2)
            ])

        # Plot
        ax1.clear()
        ax2.clear()

        ax1.plot(x_data, torque_data, label='Torque3', color='blue')
        ax1.axhline(torque_min, color='orange', linestyle='--', label='Dynamic Min')
        ax1.axhline(torque_max, color='orange', linestyle='--', label='Dynamic Max')
        ax1.set_title('Torque3 Live Plot')
        ax1.set_ylabel('Torque3')
        ax1.grid(True)
        ax1.legend()

        ax2.plot(x_data, angle_data, label='Angle3', color='green')
        ax2.axhline(angle_min, color='orange', linestyle='--', label='Dynamic Min')
        ax2.axhline(angle_max, color='orange', linestyle='--', label='Dynamic Max')
        ax2.set_title('Angle3 Live Plot')
        ax2.set_xlabel('Sample Count')
        ax2.set_ylabel('Angle3')
        ax2.grid(True)
        ax2.legend()

        plt.pause(0.1)
        time.sleep(0.1)

    if count >= max_entries:
        break

plt.ioff()
plt.show()
print(f"\nAll dynamic limits and results logged to: {output_csv_path}")
