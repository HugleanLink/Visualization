import matplotlib.pyplot as plt
import seaborn as sns


def plot_winddir(df1,airport,year):
    pivot = df1.groupby(["month", "hour"])["winddir"].mean().unstack()
    fig = plt.figure(figsize=(15, 6))
    sns.heatmap(pivot,cmap="twilight",linewidths=0.3,vmin=0,vmax=360,cbar_kws={"label": "Wind Direction(°)"})
    plt.title(f"{year} WindDirection HeatMap")
    plt.xlabel("Time")
    plt.ylabel("Month")
    plt.xticks(range(24), [f"{h:02d}:00" for h in range(24)], rotation=45)
    plt.yticks(rotation=0)
    return fig

