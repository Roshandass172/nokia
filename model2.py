import pandas as pd
from sklearn.ensemble import IsolationForest

# Load dataset
df = pd.read_csv("combined_dataset.csv")
df = df[['#028_Torque3', '#032_Angle3']].apply(pd.to_numeric, errors='coerce').dropna()

# Detect anomalies
model = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = model.fit_predict(df)

# Filter normal data
normal_df = df[df['anomaly'] == 1]
avg_torque = normal_df['#028_Torque3'].mean()
avg_angle = normal_df['#032_Angle3'].mean()

# Initial thresholds
torque_dev = 2.0
angle_dev = 3.0

# Iteratively adjust thresholds to reduce outliers
for i in range(10):
    low_t, high_t = avg_torque - torque_dev, avg_torque + torque_dev
    low_a, high_a = avg_angle - angle_dev, avg_angle + angle_dev

    out_t = ((df['#028_Torque3'] < low_t) | (df['#028_Torque3'] > high_t)).sum()
    out_a = ((df['#032_Angle3'] < low_a) | (df['#032_Angle3'] > high_a)).sum()

    print(f"Iteration {i+1}: Torque Outliers = {out_t}, Angle Outliers = {out_a}")

    # Adjust thresholds dynamically
    if out_t > 10:
        torque_dev += 0.5
    else:
        torque_dev -= 0.2

    if out_a > 10:
        angle_dev += 0.5
    else:
        angle_dev -= 0.2

# Final optimized ranges
print(f"Optimized Torque Range: {avg_torque - torque_dev:.2f} to {avg_torque + torque_dev:.2f}")
print(f"Optimized Angle Range: {avg_angle - angle_dev:.2f} to {avg_angle + angle_dev:.2f}")

