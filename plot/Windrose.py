import matplotlib.pyplot as plt
import matplotlib
from windrose import WindroseAxes
import pandas as pd
import numpy as np

def plot_windrose(df, airport, year):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
    matplotlib.rcParams['axes.unicode_minus'] = False


    temp_df = df.copy()
    temp_df = temp_df.dropna(subset=['winddir', 'windspeed'])
    temp_df = temp_df[(temp_df['windspeed'] >= 0) & (temp_df['windspeed'] < 30)]
    fig = plt.figure(figsize=(10, 8))
    ax = WindroseAxes.from_ax(fig=fig)
    ax.bar(
        temp_df['winddir'], 
        temp_df['windspeed'],
        bins=(0, 4, 8, 12, 16, 20),
        normed=True,
        opening=1,
        edgecolor='#DDDDDD',
        cmap=plt.cm.YlGnBu
    )
    maxscale = ax.get_rmax()
    maxscale = round(maxscale, 2)
    ticks = [3, 6, 9, 12]
    if maxscale > 12:
        ticks.append(maxscale)
    ax.set_yticks(ticks)  
    ax.set_yticklabels([str(t) + '%' for t in ticks])
    ax.legend(
        title='风速 (m/s)',
        loc='center left',
        bbox_to_anchor=(1.05, 0.5),
        frameon=True
    )
    ax.set_title(f"{airport} {year} Wind Rose", fontsize=20, pad=30)
    sample_count = len(temp_df)
    plt.text(
        0.5, -0.1, 
        f"样本量: {sample_count} 组",
        ha='center', va='center', 
        transform=ax.transAxes, 
        fontsize=12
    )
    plt.tight_layout()
    return fig
