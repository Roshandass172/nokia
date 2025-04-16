import pandas as pd
import time

# Use Unix-style file path for Linux/Jetson Nano
file_path = "/home/username/synthetic_full_dataset_15.csv"

# Load CSV file
df = pd.read_csv(file_path)

# Column names
TORQUE_COL = '#028_Torque3'
ANGLE_COL = '#032_Angle3'

# Alert limits
TORQUE_LIMITS = (1.0, 100.0)
ANGLE_LIMITS = (0.0, 3800.0)

# Initialize counters
torque_sum = 0.0
angle_sum = 0.0
count = 0

print("Starting AI-based live monitoring...\n")

for index, row in df.iterrows():
    torque = row[TORQUE_COL]
    angle = row[ANGLE_COL]
    count += 1

    # Update averages
    torque_sum += torque
    angle_sum += angle
    torque_avg = torque_sum / count
    angle_avg = angle_sum / count

    # Check limits
    torque_alert = not (TORQUE_LIMITS[0] <= torque <= TORQUE_LIMITS[1])
    angle_alert = not (ANGLE_LIMITS[0] <= angle <= ANGLE_LIMITS[1])

    print("[{}] Torque3: {:.2f} | Angle3: {:.2f}".format(count, torque, angle))
    print("     → Avg Torque3: {:.2f} | Avg Angle3: {:.2f}".format(torque_avg, angle_avg))

    if torque_alert:
        print("  WARNING: Torque3 value out of range!")

    if angle_alert:
        print("  WARNING: Angle3 value out of range!")

    print("-" * 50)

    # Simulate live data
    time.sleep(0.5)
