import pandas as pd
import time
import matplotlib.pyplot as plt

# File path (make sure it's valid for your system)
file_path = r"C:\Users\S Jananii\OneDrive\Desktop\nokia\1.csv"

# Load CSV
df = pd.read_csv(file_path)

# Column names
TORQUE_COL = '#028_Torque3'
ANGLE_COL = '#032_Angle3'

# Alert thresholds
TORQUE_LIMITS = (1.0, 100.0)
ANGLE_LIMITS = (0.0, 3800.0)

# Live data buffers
torque_data = []
angle_data = []
x_data = []

# Averages
torque_sum = 0.0
angle_sum = 0.0
count = 0

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle('Live Monitoring: Torque3 & Angle3')

print("Starting AI-based live monitoring...\n")

for index, row in df.iterrows():
    torque = row[TORQUE_COL]
    angle = row[ANGLE_COL]
    count += 1

    # Update sums and averages
    torque_sum += torque
    angle_sum += angle
    torque_avg = torque_sum / count
    angle_avg = angle_sum / count

    # Add to data buffer
    x_data.append(count)
    torque_data.append(torque)
    angle_data.append(angle)

    # Check for alerts
    torque_alert = not (TORQUE_LIMITS[0] <= torque <= TORQUE_LIMITS[1])
    angle_alert = not (ANGLE_LIMITS[0] <= angle <= ANGLE_LIMITS[1])

    # Console output
    print(f"[{count}] Torque3: {torque:.2f} | Angle3: {angle:.2f}")
    print(f"     → Avg Torque3: {torque_avg:.2f} | Avg Angle3: {angle_avg:.2f}")
    if torque_alert:
        print("  ⚠️ WARNING: Torque3 value out of range!")
    if angle_alert:
        print("  ⚠️ WARNING: Angle3 value out of range!")
    print("-" * 50)

    # Clear and update plots
    ax1.clear()
    ax2.clear()

    ax1.plot(x_data, torque_data, color='blue', label='Torque3')
    ax1.axhline(TORQUE_LIMITS[0], color='red', linestyle='--', label='Min Limit')
    ax1.axhline(TORQUE_LIMITS[1], color='red', linestyle='--', label='Max Limit')
    ax1.set_title('Torque3 Live Plot')
    ax1.set_ylabel('Torque3')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(x_data, angle_data, color='green', label='Angle3')
    ax2.axhline(ANGLE_LIMITS[0], color='red', linestyle='--', label='Min Limit')
    ax2.axhline(ANGLE_LIMITS[1], color='red', linestyle='--', label='Max Limit')
    ax2.set_title('Angle3 Live Plot')
    ax2.set_xlabel('Sample Count')
    ax2.set_ylabel('Angle3')
    ax2.legend()
    ax2.grid(True)

    plt.pause(0.1)  # Give time to render
    time.sleep(0.3)  # Simulate live feed

plt.ioff()
plt.show()
