import os
import re
import pandas as pd

DATA_DIR = "metar_data"


def list_airports():
    return sorted([
        d for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    ])


def list_years(airport):
    airport_path = os.path.join(DATA_DIR, airport)
    return sorted([
        f.replace(".txt", "")
        for f in os.listdir(airport_path)
        if f.endswith(".txt")
    ])



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
