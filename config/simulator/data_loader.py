import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "raw")

def load_fighters():
    path = os.path.join(DATA_DIR, "ufc_fighters.csv")
    df = pd.read_csv(path)
    return df
