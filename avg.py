import pandas as pd
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go
import os

# File setup
file_paths = [
    "1.csv", "2.csv", "3.csv", "4.csv", "5.csv", "6.csv", "7.csv",
    *[f"synthetic_full_dataset_{i}.csv" for i in range(8, 32)]
]

dataframes = []
for path in file_paths:
    full_path = path
    try:
        df = pd.read_csv(full_path)
        if '#028_Torque3' in df.columns and '#032_Angle3' in df.columns:
            df = df[['#028_Torque3', '#032_Angle3']]
            df = df.apply(pd.to_numeric, errors='coerce').dropna()
            if not df.empty:
                df['source_file'] = path
                dataframes.append(df)
    except Exception as e:
        print(f"Error in {path}: {e}")

if not dataframes:
    print("No valid data found.")
    exit()

df_all = pd.concat(dataframes, ignore_index=True)

# Train Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df_all[['#028_Torque3', '#032_Angle3']])
df_all['anomaly'] = model.predict(df_all[['#028_Torque3', '#032_Angle3']])

# Filter normal data
normal_data = df_all[df_all['anomaly'] == 1]
avg_torque = normal_data['#028_Torque3'].mean()
avg_angle = normal_data['#032_Angle3'].mean()

# --- IMPROVED THRESHOLD OPTIMIZATION ---
torque_dev = 0.1
angle_dev = 0.1
max_torque_dev = 500
max_angle_dev = 500
min_torque_dev = 0.5
min_angle_dev = 1.0

print("\n--- Threshold Optimization ---")
for i in range(15):
    t_low, t_high = avg_torque - torque_dev, avg_torque + torque_dev
    a_low, a_high = avg_angle - angle_dev, avg_angle + angle_dev

    out_t = ((df_all['#028_Torque3'] < t_low) | (df_all['#028_Torque3'] > t_high)).sum()
    out_a = ((df_all['#032_Angle3'] < a_low) | (df_all['#032_Angle3'] > a_high)).sum()

    print(f"Iteration {i+1:2}: Torque Outliers = {out_t:4}, Angle Outliers = {out_a:4} | "
          f"T_dev = {torque_dev:.2f}, A_dev = {angle_dev:.2f}")

    torque_dev = min(max(torque_dev + (10 if out_t > 10 else -5), min_torque_dev), max_torque_dev)
    angle_dev = min(max(angle_dev + (25 if out_a > 10 else -10), min_angle_dev), max_angle_dev)

# Final threshold bounds
torque_low, torque_high = avg_torque - torque_dev, avg_torque + torque_dev
angle_low, angle_high = avg_angle - angle_dev, avg_angle + angle_dev

print(f"\nFinal Torque Range: {torque_low:.2f} to {torque_high:.2f}")
print(f"Final Angle Range: {angle_low:.2f} to {angle_high:.2f}")

# Range classification
def classify_ranges(df, column, low, high):
    return df[column].apply(lambda x: 'Below' if x < low else 'Above' if x > high else 'Within')

df_all['torque_range'] = classify_ranges(df_all, '#028_Torque3', torque_low, torque_high)
df_all['angle_range'] = classify_ranges(df_all, '#032_Angle3', angle_low, angle_high)

# Print range stats
print("\nTorque Range Classification:")
print(df_all['torque_range'].value_counts())
print("\nAngle Range Classification:")
print(df_all['angle_range'].value_counts())

# Plotly visualization
def build_chart(df, value_col, range_col, title):
    grouped = df.groupby(['source_file', range_col])[value_col].count().reset_index()
    pivot = grouped.pivot(index='source_file', columns=range_col, values=value_col).fillna(0)

    fig = go.Figure()
    for category, color in zip(['Below', 'Within', 'Above'], ['red', 'green', 'black']):
        if category in pivot.columns:
            fig.add_trace(go.Bar(
                x=pivot.index,
                y=pivot[category],
                name=category,
                marker_color=color,
                hovertemplate='File: %{x}<br>Entries: %{y}<br>Range: ' + category + '<extra></extra>'
            ))

    fig.update_layout(
        title=title,
        xaxis_title="Source File",
        yaxis_title="Entry Count",
        barmode='stack',
        hovermode='x unified'
    )
    return fig

torque_fig = build_chart(df_all, '#028_Torque3', 'torque_range', 'Torque Entry Distribution per File')
angle_fig = build_chart(df_all, '#032_Angle3', 'angle_range', 'Angle Entry Distribution per File')

torque_fig.show()
angle_fig.show()
