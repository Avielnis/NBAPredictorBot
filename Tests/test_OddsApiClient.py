import unittest
import json

from Clients.OddsApiClient import parse_games, Game


class TestParseGames(unittest.TestCase):
    PARSE_GAMES_TESTS = [
        ("oddsData.json", [Game('CHA', 'ORL', 3.9785714285714286, 1.2678571428571426)])
    ]

    def test_parse_games(self):
        for games_json_file_path, expected_games_output in self.PARSE_GAMES_TESTS:
            with open(games_json_file_path, "r") as games_file:
                games_json = json.load(games_file)
                actual_games_output = parse_games(games_json)
                self.assertEqual(actual_games_output, expected_games_output)


if __name__ == '__main__':
    unittest.main()
