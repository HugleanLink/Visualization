import matplotlib.pyplot as plt
import seaborn as sns

def plot_temp(df, airport, year):
    pivot = df.groupby(["month", "hour"])["Temp_C"].mean().unstack()

    fig = plt.figure(figsize=(15, 6))
    sns.heatmap(
        pivot,
        cmap="coolwarm",
        linewidths=0.3,
        cbar_kws={"label": "Temperature (°C)"}
    )
    plt.title(f"{airport} {year} HeatMap")
    plt.xlabel("Hour of Day")
    plt.ylabel("Month")
    plt.xticks(range(24), [f"{h:02d}:00" for h in range(24)], rotation=45)
    plt.yticks(rotation=0)
    return fig
