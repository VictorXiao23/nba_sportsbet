from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time

def get_player_id(name):
    player = players.find_players_by_full_name(name)
    return player[0]['id'] if player else None

def get_player_stats(player_name):
    player_id = get_player_id(player_name)
    if not player_id:
        print(f"Player {player_name} not found.")
        return

    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season_type_all_star='Regular Season')
    df = gamelog.get_data_frames()[0]

    df = df.sort_values('GAME_DATE', ascending=False)

    df.drop(columns=['PLUS_MINUS', 'VIDEO_AVAILABLE'], inplace=True)

    print(df.head(10))
