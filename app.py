import streamlit as st
import io
from utils.loader import list_airports, list_years, load_metar, load_dew, load_wind
from plot.temp import plot_temp
from plot.dewpoint import plot_dew
from plot.winddirection import plot_winddir
from plot.windspeed import plot_windspeed

st.set_page_config(page_title="气象数据可视化平台", layout="wide")
st.title("气象数据可视化")

choice = st.selectbox("选择数据类型", ["气温热图", "露点热图", "风向热图", "风速热图", "风玫瑰"])
airport = st.selectbox("选择机场", list_airports())

available_years = list_years(airport)

if available_years:
    if len(available_years) > 1:
        year_range = st.select_slider(
            "选择年份区间",
            options=available_years,
            value=(available_years[0], available_years[-1])
        )
        start_year, end_year = year_range
    else:
        start_year = end_year = available_years[0]
        st.info(f"该机场目前只有 {start_year} 年的数据。")
    
    display_year_str = f"{start_year}-{end_year}" if start_year != end_year else f"{start_year}"
else:
    st.error("未找到数据文件")
    st.stop()

if st.button("查询图像"):
    df = None
    if choice == "气温热图":
        df = load_metar(airport, start_year, end_year)
        if df is not None: fig = plot_temp(df, airport, display_year_str)
    elif choice == "露点热图":
        df = load_dew(airport, start_year, end_year)
        if df is not None: fig = plot_dew(df, airport, display_year_str)
    elif choice == "风向热图":
        df = load_wind(airport, start_year, end_year)
        if df is not None: fig = plot_winddir(df, airport, display_year_str)
    elif choice == "风速热图":
        df = load_wind(airport, start_year, end_year)
        if df is not None: fig = plot_windspeed(df, airport, display_year_str)
    
    if df is not None:
        st.pyplot(fig)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        st.download_button(
            label="下载PNG",
            data=buf.getvalue(),
            file_name=f"{airport}_{display_year_str}_{choice}.png",
            mime="image/png"
        )
    else:
        st.warning("所选范围内没有找到有效数据，请检查文件是否存在。")




