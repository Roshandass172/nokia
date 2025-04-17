import pandas as pd
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go
import os

# File setup
data_folder = "/home/ubuntu/Desktop/nokia"
file_paths = [
    "1.csv", "2.csv", "3.csv", "4.csv", "5.csv", "6.csv", "7.csv",
    *[f"synthetic_full_dataset_{i}.csv" for i in range(8, 32)]
]

dataframes = []
for path in file_paths:
    full_path = os.path.join(data_folder, path)
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

# Adjusted thresholds
deviation_torque = 1.5
deviation_angle = 10.0

torque_low, torque_high = avg_torque - deviation_torque, avg_torque + deviation_torque
angle_low, angle_high = avg_angle - deviation_angle, avg_angle + deviation_angle

print(f"\nAverage Torque: {avg_torque:.2f} | Range: {torque_low:.2f} - {torque_high:.2f}")
print(f"Average Angle: {avg_angle:.2f} | Range: {angle_low:.2f} - {angle_high:.2f}")

# Range classification
def classify_ranges(df, column, low, high):
    conditions = []
    for val in df[column]:
        if val < low:
            conditions.append('Below')
        elif val > high:
            conditions.append('Above')
        else:
            conditions.append('Within')
    return conditions

df_all['torque_range'] = classify_ranges(df_all, '#028_Torque3', torque_low, torque_high)
df_all['angle_range'] = classify_ranges(df_all, '#032_Angle3', angle_low, angle_high)

# Print classification counts
print("\nTorque Range Classification:")
print(df_all['torque_range'].value_counts())

print("\nAngle Range Classification:")
print(df_all['angle_range'].value_counts())

# Count per file and range category
def build_chart(df, value_col, range_col, title):
    grouped = df.groupby(['source_file', range_col])[value_col].count().reset_index()
    pivot = grouped.pivot(index='source_file', columns=range_col, values=value_col).fillna(0)

    fig = go.Figure()
    for category, color in zip(['Below', 'Within', 'Above'], ['red', 'black', 'green']):
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

# Build and show both interactive charts
torque_fig = build_chart(df_all, '#028_Torque3', 'torque_range', 'Torque Entry Distribution per File')
angle_fig = build_chart(df_all, '#032_Angle3', 'angle_range', 'Angle Entry Distribution per File')

torque_fig.show()
angle_fig.show()
