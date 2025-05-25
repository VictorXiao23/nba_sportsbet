import pandas as pd
from datetime import datetime 

df = pd.read_csv("./data/PlayerStatistics.csv")

# remove postseason data
print("Removing postgame specific data...")
df = df.drop(columns=["gameSubLabel", "gameLabel", "seriesGameNumber"])

# remove inactive players
print("Converting gameDate to datetime...")
df["gameDate"] = pd.to_datetime(df["gameDate"])
print("Filtering players active since 2003-10-08...")
cutoff_date = pd.to_datetime("2003-10-08")
df = df[df["gameDate"] >= cutoff_date]

df.to_csv("./data/filtered_stats.csv")
