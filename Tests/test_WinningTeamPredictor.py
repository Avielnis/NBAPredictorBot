import unittest
from WinningTeamPredictor import WinningTeamPredictor


class TestWinningTeamPredictor(unittest.TestCase):

    TEST_MODEL = "lorWinningModel_v3.pkl"
    TEST_DATA_SET = "test_nba_games_data_set.csv"
    PREDICTOR = WinningTeamPredictor(TEST_DATA_SET, TEST_MODEL)

    def test_predict_winner(self):
        home_team_name = 'BOS'
        away_team_name = 'NY'
        predicted_winner = self.PREDICTOR.predict_winner(home_team_name, away_team_name)
        self.assertEqual(predicted_winner, 1, "Prediction should be 1")

    def test_load_model(self):
        self.assertIsNotNone(self.PREDICTOR.model, "Model should not be None after initialization")

    def test_create_prediction_data(self):
        home_team_name = 'BOS'
        away_team_name = 'NY'
        home_team_encoded = self.PREDICTOR.label_encoder.transform([home_team_name])[0]
        away_team_encoded = self.PREDICTOR.label_encoder.transform([away_team_name])[0]

        prediction_data = self.PREDICTOR.create_prediction_data(home_team_encoded, away_team_encoded)
        self.assertEqual(prediction_data.size, 73)


if __name__ == '__main__':
    unittest.main()
