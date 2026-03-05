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
    min_y = min(available_years)
    max_y = max(available_years)
    mode = st.radio("选择查询模式", ["单年份查询", "年份区间查询"], horizontal=True)
    if mode == "单年份查询":
        start_year = st.number_input(
            f"输入年份 ({min_y} - {max_y})", 
            min_value=min_y, 
            max_value=max_y, 
            value=max_y, 
            step=1
        )
        end_year = start_year
        display_year_str = f"{start_year}"
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.number_input(
                "起始年份", 
                min_value=min_y, 
                max_value=max_y, 
                value=min_y, 
                step=1
            )
        with col2:
            end_year = st.number_input(
                "结束年份", 
                min_value=min_y, 
                max_value=max_y, 
                value=max_y, 
                step=1
            )
        if start_year > end_year:
            st.warning("注意：起始年份大于结束年份，已自动为你调换顺序。")
            start_year, end_year = end_year, start_year   
        display_year_str = f"{start_year}-{end_year}"
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


