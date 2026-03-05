import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_winddir(df1, airport, year):
    temp_df = df1.copy()
    temp_df = temp_df.dropna(subset=['winddir']) 
    temp_df['u_comp'] = np.sin(np.radians(temp_df['winddir']))
    temp_df['v_comp'] = np.cos(np.radians(temp_df['winddir']))
    grouped = temp_df.groupby(["month", "hour"])
    u_mean = grouped['u_comp'].mean()
    v_mean = grouped['v_comp'].mean()
    mean_dir = (np.degrees(np.arctan2(u_mean, v_mean)) + 360) % 360
    pivot = mean_dir.unstack()
    

    fig = plt.figure(figsize=(15, 6))
    ax = sns.heatmap(pivot, cmap="Set3", linewidths=0.3, vmin=0, vmax=360, cbar_kws={"label": "Wind Direction(°)"})
    cbar = ax.figure.axes[-1]
    cbar.set_yticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
    cbar.set_yticklabels(["0°", "30°", "60°", "90°", "120°", "150°", "180°", "210°", "240°", "270°", "300°", "330°", "360°"])
    plt.title(f"{year} WindDirection HeatMap")
    plt.xlabel("Time")
    plt.ylabel("Month")
    plt.xticks(range(24), [f"{h:02d}:00" for h in range(24)], rotation=45)
    plt.yticks(rotation=0)
    return fig
