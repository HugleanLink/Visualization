import os
import re
import pandas as pd
import random


DATA_DIR = "metar_data"


def list_airports():
    return sorted([d for d in os.listdir(DATA_DIR)if os.path.isdir(os.path.join(DATA_DIR, d))])


def list_years(airport):
    airport_path = os.path.join(DATA_DIR, airport)
    return sorted([f.replace(".txt", "")for f in os.listdir(airport_path)if f.endswith(".txt")])


TEMP_PATTERN = re.compile(r"\b(M?\d{1,2})/(M?\d{1,2})\b")
def parse_temperature(metar):
    match = TEMP_PATTERN.search(metar)
    if not match:
        return None
    t = match.group(1)
    if t.startswith("M"):
        return -int(t[1:])
    return int(t)


def load_metar(airport, year):
    filepath = os.path.join(DATA_DIR, airport, f"{year}.txt")
    df = pd.read_csv(filepath)
    df.columns = ["ICAO", "Time", "Metar"]
    df["Temp_C"] = df["Metar"].apply(parse_temperature)
    df["Time"] = pd.to_datetime(df["Time"])
    df["month"] = df["Time"].dt.month
    df["hour"] = df["Time"].dt.hour
    return df


def prase_dewpoint(metar):
    match = TEMP_PATTERN.search(metar)
    if not match:
        return None
    t = match.group(2)
    if t.startswith("M"):
        return -int(t[1:])
    return int(t)


def load_dew(airport, year):
    filepath = os.path.join(DATA_DIR, airport, f"{year}.txt")
    df2 = pd.read_csv(filepath)
    df2.columns = ["ICAO", "Time", "Metar"]
    df2["Temp_C"] = df2["Metar"].apply(prase_dewpoint)
    df2["Time"] = pd.to_datetime(df2["Time"])
    df2["month"] = df2["Time"].dt.month
    df2["hour"] = df2["Time"].dt.hour
    return df2


def prase_wind(metar):
    pattern = r'(VRB|\d{3})(\d{2,3})(?:G\d{2,3})?(KT|MPS)'
    m = re.search(pattern, metar)
    if not m:
        return None,None
    direction = m.group(1)
    speed = m.group(2)
    unit = m.group(3)
    if direction != "VRB":
        direction=int(direction)
    else:
        direction=random.randint(0,359)
    if unit == "KT":
        speed=int(speed)*0.514
    return direction, speed


def load_wind(airport, year):
    filepath = os.path.join(DATA_DIR, airport, f"{year}.txt")
    df1 = pd.read_csv(filepath)
    df1.columns = ["ICAO", "Time", "Metar"]
    wind_dirs=[]
    wind_speeds=[]
    for metar in df1["Metar"]:
        d,s = prase_wind(metar)
        wind_dirs.append(d)
        wind_speeds.append(s)
        df1["winddir"] = wind_dirs
        df1["windspeed"] = wind_speeds
        df1["Time"] = pd.to_datetime(df1["Time"])
        df1["month"] = df1["Time"].dt.month
        df1["hour"] = df1["Time"].dt.hour
        return df1
