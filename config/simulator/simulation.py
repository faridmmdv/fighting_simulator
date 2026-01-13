from pathlib import Path
import pandas as pd
from django.conf import settings

DATA_DIR = Path(settings.BASE_DIR).parent / "data" / "raw"

def load_fight_stats():
    path = DATA_DIR / "ufc_event_fight_stats.csv"
    return pd.read_csv(path)

def guess_name_cols(df):
    # try common name column patterns
    candidates = [c for c in df.columns if "fighter" in c.lower() and "name" in c.lower()]
    return candidates

def build_fighter_profiles(df: pd.DataFrame):
    """
    Builds simple per-fighter aggregates from fight stats.
    We'll keep it flexible because column names differ by dataset.
    """
    cols = [c.lower() for c in df.columns]

    # Find a fighter column (common ones)
    fighter_col = None
    for c in df.columns:
        if c.lower() in ["fighter", "fighter_name", "name", "red_fighter", "blue_fighter"]:
            fighter_col = c
            break

    if fighter_col is None:
        # fallback: pick first column containing 'fighter'
        for c in df.columns:
            if "fighter" in c.lower():
                fighter_col = c
                break

    if fighter_col is None:
        raise ValueError(f"Could not find fighter column. Columns: {list(df.columns)[:80]}")

    # Find weight class column if exists
    wc_col = None
    for c in df.columns:
        if "weight" in c.lower() and "class" in c.lower():
            wc_col = c
            break
        if c.lower() == "weight_class":
            wc_col = c
            break

    # Very basic profile: fight count + primary weight class (mode)
    g = df.groupby(fighter_col)
    profiles = pd.DataFrame({
        "fighter": g.size().index,
        "fights": g.size().values,
    })

    if wc_col is not None:
        wc_mode = g[wc_col].agg(lambda x: x.dropna().astype(str).mode().iloc[0] if len(x.dropna()) else None)
        profiles["primary_weight_class"] = profiles["fighter"].map(wc_mode.to_dict())
    else:
        profiles["primary_weight_class"] = None

    return profiles
