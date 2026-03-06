import streamlit as st
import io
import pandas as pd
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
        start_year = st.number_input(f"输入年份 ({min_y} - {max_y})", min_value=min_y, max_value=max_y, value=max_y, step=1)
        end_year = start_year
        display_year_str = f"{start_year}"
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.number_input("起始年份", min_value=min_y, max_value=max_y, value=min_y, step=1)
        with col2:
            end_year = st.number_input("结束年份", min_value=min_y, max_value=max_y, value=max_y, step=1)
        
        if start_year > end_year:
            st.warning("起始年份需小于结束年份，已自动调换顺序")
            start_year, end_year = end_year, start_year   
        display_year_str = f"{start_year}-{end_year}"
else:
    st.error("未找到数据文件")
    st.stop()

timezone_choice = st.radio("选择时间显示标准", ["国际标准时间UTC+0", "北京时间UTC+8"], horizontal=True)
show_annot = st.checkbox("在热图中显示具体数值", value=False)


if st.button("生成图像"):
    with st.spinner('正在处理数据'):
        df = None
        fig = None
        if choice == "气温热图":
            df = load_metar(airport, start_year, end_year)
        elif choice == "露点热图":
            df = load_dew(airport, start_year, end_year)
        elif choice in ["风速热图", "风向热图"]:
            df = load_wind(airport, start_year, end_year)
        elif choice == "风玫瑰":
            st.warning("风玫瑰尚未完成")
            st.stop()


        if df is not None:
            if timezone_choice == "北京时间UTC+8":
                df["Time"] = pd.to_datetime(df["Time"]) + pd.Timedelta(hours=8)
                df["month"] = df["Time"].dt.month
                df["hour"] = df["Time"].dt.hour
                plot_title_suffix = f"{display_year_str} (UTC+8)"
            else:
                plot_title_suffix = f"{display_year_str} (UTC)"
            

            if choice == "气温热图":
                fig = plot_temp(df, airport, plot_title_suffix, show_annot=show_annot)
            elif choice == "露点热图":
                fig = plot_dew(df, airport, plot_title_suffix, show_annot=show_annot)
            elif choice == "风向热图":
                fig = plot_winddir(df, airport, plot_title_suffix, show_annot=show_annot)
            elif choice == "风速热图":
                fig = plot_windspeed(df, airport, plot_title_suffix, show_annot=show_annot)
            

            if fig is not None:
                st.caption(f"当前共基于{len(df)}条报文生成图表")
                st.pyplot(fig)
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=1280)
                st.download_button(
                    label="下载PNG图像",
                    data=buf.getvalue(),
                    file_name=f"{airport}_{display_year_str}_{choice}.png",
                    mime="image/png"
                )
        else:
            st.warning("所选范围内无有效数据")
