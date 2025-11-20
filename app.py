import streamlit as st
from utils.loader import list_airports, list_years, load_metar
from plot.temp import plot_temp

st.title("METAR 温度热图")

airport = st.selectbox("选择机场", list_airports())
year = st.selectbox("选择年份", list_years(airport))
df = load_metar(airport, year)
fig = plot_temp(df, airport, year)
st.pyplot(fig)
