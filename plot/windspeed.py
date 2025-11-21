import matplotlib.pyplot as plt
import seaborn as sns


def plot_windspeed(df1,airport,year):
    pivot = df1.groupby(["month", "hour"])["windspeed"].mean().unstack()
    fig = plt.figure(figsize=(15, 6))
    sns.heatmap(pivot,cmap="Blues",linewidths=0.3,cbar_kws={"label": "Wind Speed(°)"})
    plt.title(f"{year} WindSpeed HeatMap")
    plt.xlabel("Time")
    plt.ylabel("Month")
    plt.xticks(range(24), [f"{h:02d}:00" for h in range(24)], rotation=45)
    plt.yticks(rotation=0)

    return fig
