import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_dew(df2, airport, year, show_annot=False):
    df2 = df2[(df2["Temp_C"] > -60) & (df2["Temp_C"] < 50)].copy()
    pivot = df2.groupby(["month", "hour"])["Temp_C"].mean().unstack()
    pivot = pivot.reindex(index=range(1, 13), columns=range(24))
    fig = plt.figure(figsize=(15, 7))
    ax = sns.heatmap(
        pivot, 
        cmap="coolwarm", 
        linewidths=0.1, 
        cbar_kws={"label": "Dew Point (°C)"},
        annot=show_annot,        
        fmt=".1f",              
        annot_kws={"size": 8}     
    )
    
    plt.title(f"{airport} {year} Dew Point HeatMap", fontsize=15, pad=20)
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
