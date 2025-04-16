import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Step 1: Load data
file_paths = [
    "1.csv", "2.csv", "3.csv",
    "4.csv", "5.csv", "6.csv",
    "7.csv"
]
dataframes = []
for path in file_paths:
    df = pd.read_csv(path)
    # Keep only the two relevant columns
    df = df[['#028_Torque3', '#032_Angle3']]
    dataframes.append(df)

# Combine all data
df = pd.concat(dataframes, ignore_index=True)

# Step 2: Clean data
df = df.apply(pd.to_numeric, errors='coerce').dropna()

# Step 3: Train Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df)

# Predict outliers (-1 = anomaly, 1 = normal)
df['anomaly'] = model.predict(df)

# Optional: Save average of "normal" entries
normal_data = df[df['anomaly'] == 1]
avg_torque = normal_data['#028_Torque3'].mean()
avg_angle = normal_data['#032_Angle3'].mean()

print(f"Average Torque (normal): {avg_torque:.2f}")
print(f"Average Angle (normal): {avg_angle:.2f}")

# Step 4: Visualize
plt.figure(figsize=(10,6))
colors = df['anomaly'].map({1: 'green', -1: 'red'})
plt.scatter(df['#028_Torque3'], df['#032_Angle3'], c=colors, label='Data')
plt.xlabel('Torque3')
plt.ylabel('Angle3')
plt.title('Normal vs Error Entries')
plt.grid(True)
plt.show()
