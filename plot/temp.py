import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_temp(df, airport, year):
    df = df[(df["Temp_C"] > -60) & (df["Temp_C"] < 60)].copy()
    pivot = df.groupby(["month", "hour"])["Temp_C"].mean().unstack()
    pivot = pivot.reindex(index=range(1, 13), columns=range(24))
    # pivot = pivot.interpolate(axis=1).limit(2) 
    fig = plt.figure(figsize=(15, 7))
    ax = sns.heatmap(
        pivot, 
        cmap="coolwarm", 
        linewidths=0.1, 
        cbar_kws={"label": "Temperature (°C)"},
        annot=show_annot,        
        fmt=".1f",               
        annot_kws={"size": 8}    
    )
    plt.title(f"{airport} {year} Temperature HeatMap", fontsize=15, pad=20)
    plt.xlabel("Hour" , fontsize=12)
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


