import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_windspeed(df1, airport, year, show_annot=False):
    df1 = df1[(df1["windspeed"] >= 0) & (df1["windspeed"] < 100)].copy()
    pivot = df1.groupby(["month", "hour"])["windspeed"].mean().unstack()
    pivot = pivot.reindex(index=range(1, 13), columns=range(24))
    fig = plt.figure(figsize=(15, 7))
    ax = sns.heatmap(
        pivot,
        cmap="Blues",
        linewidths=0.1,
        cbar_kws={"label": "Wind Speed (m/s)"},
        annot=show_annot,
        fmt=".1f",
        annot_kws={"size": 8}
    )
    plt.title(f"{airport} {year} Wind Speed HeatMap", fontsize=15, pad=20)
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
