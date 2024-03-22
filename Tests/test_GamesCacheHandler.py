import unittest
from GamesOddsCacheHandler import GamesOddsCacheHandler
from Clients import OddsApiClient
from Clients.OddsApiClient import Game


class TestRedis(unittest.TestCase):
    redis = GamesOddsCacheHandler()

    def test_redis_insert(self):
        game = Game("team1", "team2", 1, 2)
        self.redis.cache_game_odds(game)
        actual = self.redis.get_game_odds("team1", "team2")
        self.assertEqual(game, actual)

    def test_redis_delete(self):
        self.redis.delete("team1", "team2")
        actual = self.redis.get_game_odds("team1", "team2")
        self.assertEqual(actual, None)

    def test_redis_cache_list(self):
        games = sorted(OddsApiClient.fetch_games_and_odds())
        self.redis.cache_games_list(games)
        actual = sorted(self.redis.get_all_redis_data())
        self.assertEqual(games, actual)


if __name__ == '__main__':
    unittest.main()
