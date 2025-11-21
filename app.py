import streamlit as st
import io
from utils.loader import list_airports, list_years, load_metar,load_dew,load_wind
from plot.temp import plot_temp
from plot.dewpoint import plot_dew
from plot.winddirection import plot_winddir
from plot.windspeed import plot_windspeed
from plot.Windrose import plot_wind


st.set_page_config(page_title="气象数据可视化", layout="wide")
st.title("气象数据可视化系统")
choice = st.selectbox("选择数据类型", ["气温热图", "露点热图", "风向热图", "风速热图", "风玫瑰"])
airport = st.selectbox("选择机场", list_airports())
year = st.selectbox("选择年份", list_years(airport))
if st.button("查询图像"):
    df = load_metar(airport, year)
    #df1 = load_wind(airport, year)
    df2 = load_dew(airport, year)
    if choice == "气温热图":
        fig = plot_temp(df, airport, year)
    elif choice == "露点热图":
        fig = plot_dew(df2, airport, year)
    elif choice == "风向热图":
        fig = plot_winddir(df1,airport,year)
    elif choice == "风速热图":
        fig = plot_windspeed(df1,airport,year)
    elif choice == "风玫瑰":
        st.warning("风玫瑰模块尚未完成")
        st.stop()


    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=1280)
    buf.seek(0)
    st.download_button(
        label="下载PNG",
        data=buf,
        file_name=f"{airport}_{year}_{choice}.png",
        mime="image/png"
    )

