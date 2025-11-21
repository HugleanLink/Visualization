from windrose import WindroseAxes
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib


def plot_wind(df1, airport, year):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = WindroseAxes.from_ax()
    fig.bar(df1['winddir'], df1['windspeed'],
           bins=(0, 4, 8, 12, 16, 20),
           normed=True,
           opening=1,
           edgecolor='#DDDDDD',
           cmap=plt.cm.YlGnBu
           )
    maxscale = fig.get_rmax()
    maxscale = round(maxscale, 2)
    ticks = [3, 6, 9, 12, maxscale]
    fig.set_rticks(ticks)
    fig.set_yticklabels([str(t) + '%' for t in ticks])
    fig.legend(title='风速 (m/s)',
              loc='center left',
              bbox_to_anchor=(0.75, -0.055),
              frameon=True
              )
    fig.set_title(f"{year}全年风玫瑰", fontsize=20)


