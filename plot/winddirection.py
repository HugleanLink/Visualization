import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_winddir(df1, airport, year, show_annot=False):
    temp_df = df1.copy()
    temp_df = temp_df.dropna(subset=['winddir']) 
    

    temp_df['u_comp'] = np.sin(np.radians(temp_df['winddir']))
    temp_df['v_comp'] = np.cos(np.radians(temp_df['winddir']))
    

    grouped = temp_df.groupby(["month", "hour"])
    u_mean = grouped['u_comp'].mean()
    v_mean = grouped['v_comp'].mean()

    
    mean_dir = (np.degrees(np.arctan2(u_mean, v_mean)) + 360) % 360

    
    pivot = mean_dir.unstack()
    pivot = pivot.reindex(index=range(1, 13), columns=range(24))
    
    fig = plt.figure(figsize=(15, 7))
    
    ax = sns.heatmap(
        pivot, 
        cmap="Set3", 
        linewidths=0.1, 
        vmin=0, 
        vmax=360, 
        cbar_kws={"label": "Wind Direction (°)"},
        annot=show_annot,
        fmt=".0f",          
        annot_kws={"size": 7}
    )

    cbar = ax.figure.axes[-1]
    ticks = [0, 45, 90, 135, 180, 225, 270, 315, 360]
    cbar.set_yticks(ticks)
    cbar.set_yticklabels([f"{t}°" for t in ticks])
    

    plt.title(f"{airport} {year} Wind Direction HeatMap", fontsize=15, pad=20)
    plt.xlabel("Local Hour" if "UTC+8" in str(year) else "UTC Hour", fontsize=12)
    plt.ylabel("Month", fontsize=12)
    

    plt.xticks(
        np.arange(24) + 0.5, 
        [f"{h:02d}:00" for h in range(24)], 
        rotation=45
    )
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    plt.yticks(
        np.arange(12) + 0.5, 
        month_names, 
        rotation=0
    )
    plt.tight_layout()
    return fig
