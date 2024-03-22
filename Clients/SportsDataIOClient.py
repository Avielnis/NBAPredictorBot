import json
import pandas as pd
import requests
import csv
from datetime import datetime, timedelta
from api_settings import SPORTS_DATA_API_KEY


class SportsDataIOClient:
    @staticmethod
    def get_games_by_date(date_to_fetch: str) -> json:
        url = f'https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{date_to_fetch}?format=json&key={SPORTS_DATA_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def get_game_stats_by_id(game_id: str) -> json:
        url = f'https://api.sportsdata.io/v3/nba/stats/json/BoxScore/{game_id}?format=json&key={SPORTS_DATA_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


def get_last_n_days_dates(n_days: int, offset: datetime = datetime.now()) -> list[str]:
    last_30_days = [offset - timedelta(days=x) for x in range(n_days)]
    formatted_dates = [day.strftime('%Y-%b-%d').upper() for day in last_30_days]
    return formatted_dates


def save_to_csv(games_to_save: json, file_path: str):
    with (open(file_path, mode='a', newline='') as csvfile):
        fieldnames = ['GameID', 'Season', 'Day', 'HomeTeam', 'AwayTeam', 'HomeTeamScore', 'AwayTeamScore']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for game in games_to_save:
            if game['HomeTeamScore'] is None or game['AwayTeamScore'] is None or game['HomeTeam'] in [None, '', 'WEST',
                                                                                                      'EAST']:
                continue

            writer.writerow({
                'GameID': game['GameID'],
                'Season': game['Season'],
                'Day': game['Day'],
                'HomeTeam': game['HomeTeam'],
                'AwayTeam': game['AwayTeam'],
                'HomeTeamScore': game['HomeTeamScore'],
                'AwayTeamScore': game['AwayTeamScore']
            })


# if __name__ == '__main__':
    # file_path = '../DataSets/nba_games.csv'
    # client = SportsDataIOClient()
    # offset = datetime.now() - timedelta(days=151)
    # dates = get_last_n_days_dates(50, offset)
    # all_games = []
    # for date in dates:
    # #     games = client.get_games_by_date(date)
    # #     if games:
    # #         all_games.extend(games)
    # # save_to_csv(all_games, 'DataSets/nba_games.csv')
    # stats_data_frame = []
    # with (open(file_path, mode='r', newline='') as csvfile):
    #     reader = csv.DictReader(csvfile)
    #     for i, row in enumerate(reader):
    #         if (i < 625):
    #             continue
    #         game_id = row['GameID']
    #
    #         print(f"Fetching stats for game {game_id}")
    #
    #         game_stats = client.get_game_stats_by_id(game_id)
    #         if game_stats:
    #             is_first_home_team = game_stats['TeamGames'][0]['HomeOrAway'] == 'Home'
    #             home_team_stats = game_stats['TeamGames'][0] if is_first_home_team else game_stats['TeamGames'][1]
    #             away_team_stats = game_stats['TeamGames'][1] if is_first_home_team else game_stats['TeamGames'][0]
    #
    #             # add home_ prefix to all keys in home_team_stats
    #             home_team_stats = {f'home_{key}': value for key, value in home_team_stats.items()}
    #             # add away_ prefix to all keys in away_team_stats
    #             away_team_stats = {f'away_{key}': value for key, value in away_team_stats.items()}
    #
    #             # merge home and away team stats
    #             game_stats = {**home_team_stats, **away_team_stats, 'GameID': game_id}
    #             stats_data_frame.append(game_stats)
    #         else:
    #             print(f"Failed to fetch stats for game {game_id}")
    #         sleep(0.1)
    #
    # # save to json file
    # with (open('DataSets/nba_games_with_team_stats_new.json', mode='w', newline='') as jsonfile):
    #     json.dump(stats_data_frame, jsonfile)
    # with (open('DataSets/nba_games_with_team_stats_new.json', mode='r', newline='') as jsonfile):
    #     stats_data_frame = json.load(jsonfile)
    #
    # with (open('DataSets/nba_games_with_team_stats_new.csv', mode='a', newline='') as csvfile):
    #     fieldnames = stats_data_frame[0].keys()
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     for game in stats_data_frame:
    #         writer.writerow(game)

    # combine nba_games.csv and nba_games_with_team_stats_new.csv
    # df_games = pd.read_csv('DataSets/nba_games.csv')
    # df_stats = pd.read_csv('DataSets/nba_games_with_team_stats_new.csv')
    # df = pd.merge(df_games, df_stats, on='GameID')
    # df.to_csv('DataSets/nba_games_with_team_stats_final_set.csv', index=False)

    # get a list of all the unique teams
    # df = pd.read_csv('../DataSets/nba_games.csv')
    # teams = df['HomeTeam'].unique()
    # print(teams)


