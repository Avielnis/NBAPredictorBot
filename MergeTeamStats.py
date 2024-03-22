import requests
import pandas as pd
from api_settings import SPORTS_DATA_API_KEY

df_games = pd.read_csv('DataSets/nba_games.csv')


def fetch_teams_stats_remote():
    seasons = df_games['Season'].unique()

    team_stats = []
    for season in seasons:
        url = f'https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/{season}?key={SPORTS_DATA_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            season_stats = response.json()
            team_stats.extend(season_stats)
    return team_stats


def fetch_team_stats_local():
    return pd.read_json('DataSets/teamStats2024.json')


def create_dataset(df_stats):
    # Add to all home_
    df_home_team_stats = df_stats.add_prefix('home_')
    # Add to all away_
    df_away_team_stats = df_stats.add_prefix('away_')

    # merge correctly
    df = pd.merge(df_games, df_home_team_stats, left_on=['HomeTeam'], right_on=['home_Team'],
                  suffixes=('', '_team_stats'))
    df = pd.merge(df, df_away_team_stats, left_on=['AwayTeam'], right_on=['away_Team'],
                  suffixes=('', '_opponent_stats'))
    df = df.dropna(axis=1)

    # drop unneeded cols
    features_to_drop = ['GameID', 'Day', 'home_StatID', 'away_StatID', 'home_GlobalTeamID', 'away_GlobalTeamID',
                        'home_Name', 'away_Name', 'home_OpponentStat', 'away_OpponentStat', 'home_Team', 'away_Team',
                        'home_TeamID', 'away_TeamID']
    df = df.drop(features_to_drop, axis=1)
    unique_counts = df.nunique()
    columns_to_remove = unique_counts[unique_counts == 1].index

    df_cleaned = df.drop(columns=columns_to_remove)
    return df_cleaned


def save_to_csv(df, filename):
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    df_stats = fetch_team_stats_local()
    df_cleaned = create_dataset(df_stats)
    save_to_csv(df_cleaned, 'DataSets/nba_games_with_team_stats.csv')
