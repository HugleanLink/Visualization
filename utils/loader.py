import os
import re
import pandas as pd
import xarray as xr
import random

DATA_DIR = "metar_data"

TEMP_PATTERN = re.compile(r"\b(M?\d{1,2})/(M?\d{1,2})\b")

def parse_temperature(metar):
    if not isinstance(metar, str): return None
    match = TEMP_PATTERN.search(metar)
    if not match: return None
    t = match.group(1)
    return -int(t[1:]) if t.startswith("M") else int(t)

def prase_dewpoint(metar):
    if not isinstance(metar, str): return None
    match = TEMP_PATTERN.search(metar)
    if not match: return None
    t = match.group(2)
    return -int(t[1:]) if t.startswith("M") else int(t)

def load_metar(airport, start_year, end_year):
    df = _load_base_range(airport, start_year, end_year)
    if df is not None:
        df["Temp_C"] = df["Metar"].apply(parse_temperature)
    return df

def load_dew(airport, start_year, end_year):
    df = _load_base_range(airport, start_year, end_year)
    if df is not None:
        df["Temp_C"] = df["Metar"].apply(prase_dewpoint)
    return df

def load_wind(airport, start_year, end_year):
    df = _load_base_range(airport, start_year, end_year)
    if df is not None:
        def prase_winddir(metar):
            wind_regex = re.compile(r'(VRB|\d{3})(\d{2,3})(?:G\d{2,3})?(KT|MPS)')
            m = wind_regex.search(str(metar))
            if not m: return None
            direction = m.group(1)
            return random.randint(0, 359) if direction == "VRB" else int(direction)

        def prase_windspeed(metar):
            wind_regex = re.compile(r'(VRB|\d{3})(\d{2,3})(?:G\d{2,3})?(KT|MPS)')
            m = wind_regex.search(str(metar))
            if not m: return None
            speed = int(m.group(2))
            return speed * 0.514 if m.group(3) == "KT" else speed

        df["winddir"] = df["Metar"].apply(prase_winddir)
        df["windspeed"] = df["Metar"].apply(prase_windspeed)
    return df

def _load_base_range(airport, start_year, end_year):
    dfs = []
    for y in range(int(start_year), int(end_year) + 1):
        filepath = os.path.join(DATA_DIR, airport, f"{y}.txt")
        if os.path.exists(filepath):
            try:
                temp_df = pd.read_csv(filepath)
                temp_df.columns = ["ICAO", "Time", "Metar"]
                dfs.append(temp_df)
            except Exception as e:
                print(f"读取文件 {filepath} 出错: {e}")
    
    if not dfs:
        return None
    
    full_df = pd.concat(dfs, ignore_index=True)
    full_df["Time"] = pd.to_datetime(full_df["Time"])
    full_df["month"] = full_df["Time"].dt.month
    full_df["hour"] = full_df["Time"].dt.hour
    return full_df

def list_airports():
    if not os.path.exists(DATA_DIR): return []
    return sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])

def list_years(airport):
    airport_path = os.path.join(DATA_DIR, airport)
    if not os.path.exists(airport_path): return []
    years = [f.replace(".txt", "") for f in os.listdir(airport_path) if f.endswith(".txt")]
    return sorted([int(y) for y in years if y.isdigit()])
