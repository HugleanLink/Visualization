import os
import pandas as pd

DATA_DIR = "metar_data"


def list_airports():
    """返回所有机场目录"""
    return sorted([
        d for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    ])


def list_years(airport):
    """返回某机场的所有年份文件"""
    airport_path = os.path.join(DATA_DIR, airport)
    return sorted([
        f.replace(".txt", "")
        for f in os.listdir(airport_path)
        if f.endswith(".txt")
    ])


def parse_temperature(metar):
    """从 METAR 中提取温度"""
    parts = metar.split()
    for p in parts:
        if "/" in p and len(p) <= 7 and ("M" in p or p[0].isdigit()):
            t = p.split("/")[0]
            if t.startswith("M"):
                return -int(t[1:])
            else:
                return int(t)
    return None


def load_metar(airport, year):
    """读文件 → 返回解析后的 DataFrame"""
    filepath = os.path.join(DATA_DIR, airport, f"{year}.txt")
    df = pd.read_csv(filepath)

    df.columns = ["ICAO", "Time", "Metar"]
    df["Temp_C"] = df["Metar"].apply(parse_temperature)

    df["Time"] = pd.to_datetime(df["Time"])
    df["month"] = df["Time"].dt.month
    df["hour"] = df["Time"].dt.hour  # 1 小时一个格子

    return df
