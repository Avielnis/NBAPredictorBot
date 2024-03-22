from __future__ import annotations

import redis
import logging
from Clients import OddsApiClient
from Clients.OddsApiClient import Game
from api_settings import AZURE_REDIS_PASS, REDIS_PORT, REDIS_HOST
import json


class GamesOddsCacheHandler:
    def __init__(self):
        # self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.redis_client = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=AZURE_REDIS_PASS,
            ssl=True,
            decode_responses=True,
            db=0
        )

    def cache_game_odds(self, game: Game):
        ttl_in_seconds = 4 * 60 * 60  # 4 hours
        key = str((game.home_team, game.away_team))
        value = str((game.home_team_price, game.away_team_price))
        self.redis_client.setex(key, ttl_in_seconds, value)

    def cache_games_list(self, games) -> int:
        if games is None:
            logging.warning("failed to fetch new games")
            return 0
        elif len(games) == 0:
            logging.warning("fetched empty list of games")
            return 0

        for game in games:
            self.cache_game_odds(game)
        logging.info("stored updated games list")
        return len(games)

    def get_game_odds(self, home_team, away_team) -> Game | None:
        key = str((home_team, away_team))
        cached_answer: str = self.redis_client.get(key)
        if cached_answer is not None:
            home_team_price, away_team_price = eval(cached_answer)
            game = Game(home_team, away_team, home_team_price, away_team_price)
            logging.info(f"return odds of {game}")
            return game

        if len(self.redis_client.keys('*')) == 0:
            games = OddsApiClient.fetch_games_and_odds()
            num_games_cached = self.cache_games_list(games)
            if num_games_cached > 0:
                return self.get_game_odds(home_team, away_team)
        else:
            logging.info(f"didn't find game odds for {home_team} VS {away_team}")
            return None

    def print_all_redis_data(self) -> list[tuple]:
        all_keys = self.redis_client.keys('*')

        lst = []
        for key in all_keys:
            value = self.redis_client.get(key)
            lst.append((key, value))
            print(f'{key}: {value}')
        return lst

    def get_all_redis_data(self):
        all_keys = self.redis_client.keys('*')

        lst = []
        for key in all_keys:
            value = self.redis_client.get(key)
            home_team, away_team = eval(key)
            home_score, away_score = eval(value)
            lst.append(Game(home_team, away_team, home_score, away_score))
        return lst

    def delete(self, home_team, away_team):
        key = str((home_team, away_team))
        result = self.redis_client.delete(key)
        if result > 0:
            logging.info(f'The key "{key}" was deleted successfully.')
        else:
            logging.error(f'The key "{key}" does not exist in the Redis instance.')


class ResponsesCacheHandler:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=AZURE_REDIS_PASS,
            ssl=True,
            decode_responses=True,
            db=1
        )

    def cache_response(self, home_team, away_team, response_dict):
        ttl_in_seconds = 4 * 60 * 60  # 4 hours
        key = str((home_team, away_team))
        value = json.dumps(response_dict)
        self.redis_client.setex(key, ttl_in_seconds, value)
        logging.info(f"cached {home_team} VS {away_team}")

    def get_response(self, home_team, away_team):
        key = str((home_team, away_team))
        cached_answer: str = self.redis_client.get(key)
        if not cached_answer:
            logging.info(f"Not found in cache {home_team} VS {away_team}")
            return None
        logging.info(f"Found in cache {home_team} VS {away_team}")

        return json.loads(cached_answer)  # None if does not exist

    def delete(self, home_team, away_team):
        key = str((home_team, away_team))
        result = self.redis_client.delete(key)
        if result > 0:
            logging.info(f'The key "{key}" was deleted successfully.')
        else:
            logging.error(f'The key "{key}" does not exist in the Redis instance.')

    def get_all_responses_data(self):
        all_keys = self.redis_client.keys('*')

        lst = []
        for key in all_keys:
            value = self.redis_client.get(key)
            lst.append((eval(key), value))
        return lst


if __name__ == '__main__':
    handler = ResponsesCacheHandler()
    # handler.cache_response("Aviel", "Lapushin", {"message": "some text"})
    # response = handler.get_response("Aviel", "Lapushin")
    # print(response)
    # handler.delete("DAL", "ATL")
    print(handler.get_all_responses_data())
