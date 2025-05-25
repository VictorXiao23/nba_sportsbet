import pandas as pd
import time
import os
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

# === Configuration ===
SEASON = "2023-24"
CACHE_FILE = "./data/all_active_gamelogs.csv"
SLEEP_BETWEEN_REQUESTS = 1.5

# === Get all active players ===
def get_all_active_players():
    return players.get_active_players()

# === Fetch player game logs ===
def get_game_logs(player_id, player_name):
    try:
        gamelog = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=SEASON,
            season_type_all_star="Regular Season"
        )
        df = gamelog.get_data_frames()[0]
        df["PLAYER_NAME"] = player_name

        df.drop(columns=['PLUS_MINUS', 'VIDEO_AVAILABLE'], inplace=True, errors='ignore')

        return df
    except Exception as e:
        print(f"❌ Error fetching logs for {player_name}: {e}")
        return pd.DataFrame()


# === Main script ===
def main():
    all_logs = []
    player_list = get_all_active_players()
    print(f"📋 Found {len(player_list)} active players.")

    for idx, player in enumerate(player_list):
        pid = player['id']
        name = player['full_name']
        print(f"[{idx+1}/{len(player_list)}] ⏳ Fetching logs for {name}...")

        logs = get_game_logs(pid, name)
        if not logs.empty:
            all_logs.append(logs)

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    if not all_logs:
        print("❌ No logs fetched.")
        return

    combined_df = pd.concat(all_logs)
    combined_df.sort_values(by=["PLAYER_NAME", "GAME_DATE"], ascending=[True, False], inplace=True)
    combined_df.to_csv(CACHE_FILE, index=False)
    print(f"✅ Saved {len(combined_df)} game logs to {CACHE_FILE}")

if __name__ == "__main__":
    main()
