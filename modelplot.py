import pandas as pd
import time
import matplotlib.pyplot as plt
import os

file_paths = [
    "1.csv", "2.csv", "3.csv", "4.csv", "5.csv", "6.csv", "7.csv",
    *[f"synthetic_full_dataset_{i}.csv" for i in range(8, 32)]
]

TORQUE_COL = '#028_Torque3'
ANGLE_COL = '#032_Angle3'

TORQUE_LIMITS = [1.0, 3.0]
ANGLE_LIMITS = [3200.0, 5500.0]

torque_values = []
angle_values = []

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle('Live Monitoring with AI-Adaptive Thresholds')

torque_data = []
angle_data = []
x_data = []

count = 0

for file_path in file_paths:
    if not os.path.exists(file_path):
        continue

    df = pd.read_csv(file_path)

    if TORQUE_COL not in df.columns or ANGLE_COL not in df.columns:
        continue

    for _, row in df.iterrows():
        try:
            torque = float(row[TORQUE_COL])
            angle = float(row[ANGLE_COL])
        except:
            continue

        count += 1
        x_data.append(count)
        torque_data.append(torque)
        angle_data.append(angle)
        torque_values.append(torque)
        angle_values.append(angle)

        if count > 20:
            torque_series = pd.Series(torque_values[-100:])
            angle_series = pd.Series(angle_values[-100:])

            torque_mean = torque_series.mean()
            torque_std = torque_series.std()
            angle_mean = angle_series.mean()
            angle_std = angle_series.std()

            new_torque_limits = (torque_mean - 2 * torque_std, torque_mean + 2 * torque_std)
            new_angle_limits = (angle_mean - 2 * angle_std, angle_mean + 2 * angle_std)

            torque_lr = 0.05
            angle_lr = 0.05
            TORQUE_LIMITS[0] = (1 - torque_lr) * TORQUE_LIMITS[0] + torque_lr * new_torque_limits[0]
            TORQUE_LIMITS[1] = (1 - torque_lr) * TORQUE_LIMITS[1] + torque_lr * new_torque_limits[1]
            ANGLE_LIMITS[0] = (1 - angle_lr) * ANGLE_LIMITS[0] + angle_lr * new_angle_limits[0]
            ANGLE_LIMITS[1] = (1 - angle_lr) * ANGLE_LIMITS[1] + angle_lr * new_angle_limits[1]

        torque_alert = not (TORQUE_LIMITS[0] <= torque <= TORQUE_LIMITS[1])
        angle_alert = not (ANGLE_LIMITS[0] <= angle <= ANGLE_LIMITS[1])

        print(f"[{count}] Torque3: {torque:.2f} | Angle3: {angle:.2f}")
        if torque_alert:
            print("  WARNING: Torque3 out of threshold")
        if angle_alert:
            print("  WARNING: Angle3 out of threshold")
        print(f"  Current Torque Limits: {TORQUE_LIMITS[0]:.2f} to {TORQUE_LIMITS[1]:.2f}")
        print(f"  Current Angle Limits: {ANGLE_LIMITS[0]:.2f} to {ANGLE_LIMITS[1]:.2f}")
        print("-" * 50)

        ax1.clear()
        ax2.clear()

        ax1.plot(x_data, torque_data, label='Torque3', color='blue')
        ax1.axhline(TORQUE_LIMITS[0], color='orange', linestyle='--', label='Dynamic Min')
        ax1.axhline(TORQUE_LIMITS[1], color='orange', linestyle='--', label='Dynamic Max')
        ax1.set_title('Torque3 Live Plot')
        ax1.set_ylabel('Torque3')
        ax1.grid(True)
        ax1.legend()

        ax2.plot(x_data, angle_data, label='Angle3', color='green')
        ax2.axhline(ANGLE_LIMITS[0], color='orange', linestyle='--', label='Dynamic Min')
        ax2.axhline(ANGLE_LIMITS[1], color='orange', linestyle='--', label='Dynamic Max')
        ax2.set_title('Angle3 Live Plot')
        ax2.set_xlabel('Sample Count')
        ax2.set_ylabel('Angle3')
        ax2.grid(True)
        ax2.legend()

        plt.pause(0.1)
        time.sleep(0.1)

plt.ioff()
plt.show()
