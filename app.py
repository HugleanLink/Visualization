import streamlit as st
import io
from utils.loader import list_airports, list_years, load_metar, load_dew, load_wind
from plot.temp import plot_temp
from plot.dewpoint import plot_dew
from plot.winddirection import plot_winddir
from plot.windspeed import plot_windspeed
# from plot.Windrose import plot_wind

st.set_page_config(page_title="气象数据可视化平台", layout="wide")
st.title("气象数据可视化")

choice = st.selectbox("选择数据类型", ["气温热图", "露点热图", "风向热图", "风速热图", "风玫瑰"])
airport = st.selectbox("选择机场", list_airports())


available_years = list_years(airport)
if available_years:
    year_range = st.select_slider(
        "选择年份区间",
        options=available_years,
        value=(available_years[0], available_years[-1]) 
    )
    start_year, end_year = year_range
    display_year_str = f"{start_year}-{end_year}" if start_year != end_year else f"{start_year}"
else:
    st.error("该机场暂无可用数据")
    st.stop()

if st.button("查询图像"):
    with st.spinner('正在处理多年份数据，请稍候...'):
        if choice == "气温热图":
            df = load_metar(airport, start_year, end_year)
            fig = plot_temp(df, airport, display_year_str)
        elif choice == "露点热图":
            df = load_dew(airport, start_year, end_year)
            fig = plot_dew(df, airport, display_year_str)
        elif choice == "风向热图":
            df = load_wind(airport, start_year, end_year)
            fig = plot_winddir(df, airport, display_year_str)
        elif choice == "风速热图":
            df = load_wind(airport, start_year, end_year)
            fig = plot_windspeed(df, airport, display_year_str)
        elif choice == "风玫瑰":
            st.warning("风玫瑰模块尚未完成")
            st.stop()

    st.pyplot(fig)
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300) 
    buf.seek(0)
    st.download_button(
        label="下载PNG",
        data=buf,
        file_name=f"{airport}_{display_year_str}_{choice}.png",
        mime="image/png"
    )






