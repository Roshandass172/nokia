import pandas as pd
import time

file_path = r"C:\Users\Rosh05\Downloads\synthetic_full_dataset_15.csv"
df = pd.read_csv(file_path)

TORQUE_COL = '#028_Torque3'
ANGLE_COL = '#032_Angle3'

TORQUE_LIMITS = (1.0, 100.0)  
ANGLE_LIMITS = (0.0, 3800.0)   


torque_sum = 0.0
angle_sum = 0.0
count = 0

print("🔧 Starting AI-based live monitoring...\n")


for index, row in df.iterrows():
    torque = row[TORQUE_COL]
    angle = row[ANGLE_COL]
    count += 1


    torque_sum += torque
    angle_sum += angle
    torque_avg = torque_sum / count
    angle_avg = angle_sum / count

  
    torque_alert = not (TORQUE_LIMITS[0] <= torque <= TORQUE_LIMITS[1])
    angle_alert = not (ANGLE_LIMITS[0] <= angle <= ANGLE_LIMITS[1])

    print(f"[{count}] Torque3: {torque:.2f} | Angle3: {angle:.2f}")
    print(f"     → Avg Torque3: {torque_avg:.2f} | Avg Angle3: {angle_avg:.2f}")

    if torque_alert:
        print("  ⚠️ ALERT: Torque3 value out of range!")

    if angle_alert:
        print("  ⚠️ ALERT: Angle3 value out of range!")

    print("-" * 50)


    time.sleep(0.5)   
