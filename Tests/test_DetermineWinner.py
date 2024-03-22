import unittest
from determine_winner import determine_winner
from Clients.OddsApiClient import Game


class TestDetermineWinner(unittest.TestCase):
    def test_both_agree_on_winner_home(self):
        game = Game("HomeTeam", "AwayTeam", 1.5, 2.0)
        self.assertEqual(determine_winner(1, game), ("HomeTeam", "AwayTeam"))

    def test_both_agree_on_winner_away(self):
        game = Game("HomeTeam", "AwayTeam", 2.0, 1.5)
        self.assertEqual(determine_winner(0, game), ("AwayTeam", "HomeTeam"))

    def test_model_pred_home_odds_good(self):
        game = Game("HomeTeam", "AwayTeam", 2.0, 3.0)
        self.assertEqual(determine_winner(1, game), ("HomeTeam", "AwayTeam"))

    def test_model_pred_home_odds_not_good(self):
        game = Game("HomeTeam", "AwayTeam", 3.0, 1.15)
        self.assertEqual(determine_winner(1, game), ("AwayTeam", "HomeTeam"))

    def test_model_pred_away_odds_good(self):
        game = Game("HomeTeam", "AwayTeam", 3.0, 2.0)
        self.assertEqual(determine_winner(0, game), ("AwayTeam", "HomeTeam"))

    def test_model_pred_away_odds_not_good(self):
        game = Game("HomeTeam", "AwayTeam", 1.15, 3.0)
        self.assertEqual(determine_winner(0, game), ("HomeTeam", "AwayTeam"))


if __name__ == '__main__':
    unittest.main()
