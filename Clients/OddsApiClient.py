import requests
import json
import logging
from api_settings import ODDS_API_KEY
from config import TEAMS_FULL_NAME_TO_SHORT


class Game:
    def __init__(self, home_team, away_team, home_team_price, away_team_price):
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_price = home_team_price
        self.away_team_price = away_team_price

    def predict_winner(self) -> int:
        return 1 if self.away_team_price > self.home_team_price else 0

    def __eq__(self, other) -> bool:
        return self.home_team == other.home_team and self.away_team == other.away_team \
               and self.home_team_price == other.home_team_price and self.away_team_price == other.away_team_price

    def __lt__(self, other) -> bool:
        total_price_self = self.home_team_price + self.away_team_price
        total_price_other = other.home_team_price + other.away_team_price
        return total_price_self < total_price_other


def fetch_games_and_odds():
    games = None
    # Returns a list of upcoming and live games with recent odds for a given sport, region and market
    url = f'https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey={ODDS_API_KEY}&regions=us'
    try:
        response = requests.get(url)

        if response.status_code == 200:
            odds_data = response.json()
            games = parse_games(odds_data)
            logging.info("Parsed games successfully")
        else:
            logging.error(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        logging.error(f"Error: {e}")

    return games


def parse_games(odds_data_json: json) -> list[Game]:
    parsed_games = []
    for game in odds_data_json:
        home_team = game["home_team"]
        away_team = game["away_team"]
        bookmakers = game["bookmakers"]
        home_team_price, away_team_price = parse_prices(bookmakers, home_team)
        home_team_short = TEAMS_FULL_NAME_TO_SHORT[home_team]
        away_team_short = TEAMS_FULL_NAME_TO_SHORT[away_team]
        parsed_games.append(Game(home_team_short, away_team_short, home_team_price, away_team_price))

    return parsed_games


def parse_prices(bookmakers: json, home_team) -> tuple[int, int]:
    num_markets = 0
    home_team_price = 0
    away_team_price = 0

    for bookmaker in bookmakers:
        for market in bookmaker["markets"]:
            num_markets += 1
            outcomes = market["outcomes"]
            first_outcome, second_outcome = outcomes[0], outcomes[1]
            if first_outcome["name"] == home_team:
                home_team_price += first_outcome["price"]
                away_team_price += second_outcome["price"]
            else:
                away_team_price += first_outcome["price"]
                home_team_price += second_outcome["price"]

    home_team_price /= num_markets
    away_team_price /= num_markets

    return home_team_price, away_team_price


if __name__ == "__main__":
    games = fetch_games_and_odds()
