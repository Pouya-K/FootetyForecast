import requests
import pandas as pd
import os

SEASONS = ["2122", "2223", "2324", "2425", "2526"]
CURRENT_SEASON = "2526"

BASE_URL = "https://www.football-data.co.uk/mmz4281/{season}/E0.csv"

os.makedirs("ml/data/raw", exist_ok=True)

#download data from all seasons and save locally
for season in SEASONS:
    filepath = f"ml/data/raw/E0_{season}.csv"
    if season != CURRENT_SEASON and os.path.exists(filepath):
        print(f"{season} already exists, skipping it")
        continue

    url = BASE_URL.format(season = season)
    response = requests.get(url)

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"Downloaded {season}")

#combine all data files into one big file
dfs = []
for season in SEASONS:
    filepath = f"ml/data/raw/E0_{season}.csv"
    df = pd.read_csv(filepath)
    df["season"] = season
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
print(f"Combined: {len(combined)} total matches")  

#clean up and only keep relevant data
cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR",
        "HC", "AC", "HY", "AY", "HR", "AR", "season"]
combined = combined[cols]

combined["Date"] = pd.to_datetime(combined["Date"], dayfirst=True)
combined["home_cards"] = combined["HY"] + combined["HR"]
combined["away_cards"] = combined["AY"] + combined["AR"]
combined = combined.dropna(subset=["FTR"])
combined = combined.sort_values("Date").reset_index(drop=True)

combined.to_csv("ml/data/epl_combined.csv", index=False)
print(f"Saved {len(combined)} cleaned matches")
