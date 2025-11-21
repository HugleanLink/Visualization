import streamlit as st
from utils.loader import list_airports, list_years, load_metar
from plot.temp import plot_temp

st.set_page_config(page_title="气象数据可视化",layout="wide")
st.title("气象数据可视化系统")
choice = st.selectbox("选择数据类型",["气温热图","露点热图","风向热图","风速热图","风玫瑰"])
airport = st.selectbox("选择机场", list_airports())
year = st.selectbox("选择年份", list_years(airport))
if st.button("查询图像"):
    df = load_metar(airport, year)
    if choice == "气温热图":
        fig = plot_temp(df, airport, year)
    elif choice == "露点热图":
        st.warning("露点模块尚未完成")
        st.stop()
    elif choice == "风向热图":
        st.warning("风向模块尚未完成")
        st.stop()
    elif choice == "风速热图":
        st.warning("风速模块尚未完成")
        st.stop()
    elif choice == "风玫瑰":
        st.warning("风玫瑰模块尚未完成")
        st.stop()
    st.pyplot(fig)
