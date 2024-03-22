import logging
import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import os
import joblib


class WinningTeamPredictor:
    MODEL_FILE_PATH = "Models/lorWinningModel_v3.pkl"
    DATA_FILE_PATH = "DataSets/nba_games_with_team_stats_final_set.csv"

    def __init__(self, data_file_path: str = DATA_FILE_PATH, model_file_path: str = MODEL_FILE_PATH):
        self.label_encoder = LabelEncoder()
        self.data = self.load_data(data_file_path)
        self.model = self.load_model(model_file_path)
        if not self.model:
            self.train_model()

    def load_data(self, data_file_path: str):
        data = pd.read_csv(data_file_path)

        categorical_columns = ['HomeTeam', 'AwayTeam']
        for col in categorical_columns:
            data[col] = self.label_encoder.fit_transform(data[col])

        data['Winner'] = (data['HomeTeamScore'] > data['AwayTeamScore']).astype(int)

        return data

    def train_model(self):
        labels = self.data['Winner']
        data = self.data.drop(['Winner', 'HomeTeamScore', 'AwayTeamScore'], axis=1)

        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f'Accuracy: {accuracy:.2f}')
        logging.info(classification_report(y_test, y_pred))

        logging.info(f"saving model at {self.MODEL_FILE_PATH}")
        joblib.dump(self.model, self.MODEL_FILE_PATH)

    def predict_winner(self, home_team: str, away_team: str) -> int:
        home_team_encoded = self.label_encoder.transform([home_team])[0]
        away_team_encoded = self.label_encoder.transform([away_team])[0]

        prediction_data = self.create_prediction_data(home_team_encoded, away_team_encoded)

        winner = self.model.predict(prediction_data)[0]

        return winner

    def create_prediction_data(self, home_team: str, away_team: str):
        home_team_data = self.data[self.data['HomeTeam'] == home_team]
        away_team_data = self.data[self.data['AwayTeam'] == away_team]

        home_team_aggregated = home_team_data.mean().to_frame().transpose()
        away_team_aggregated = away_team_data.mean().to_frame().transpose()

        features = home_team_aggregated.columns

        values = []
        for feature in features:
            if feature.startswith('home') or feature.startswith("Home"):
                values.append(home_team_aggregated[feature][0])
            else:
                values.append(away_team_aggregated[feature][0])

        dataFrame = pd.DataFrame([values], columns=features)
        dataFrame = dataFrame.drop(['Winner', 'HomeTeamScore', 'AwayTeamScore'], axis=1)

        return dataFrame

    @staticmethod
    def load_model(model_path: str):
        if os.path.exists(model_path):
            logging.info(f"loading model from {model_path}")
            return joblib.load(model_path)
        return None


if __name__ == "__main__":
    home_team_name = 'NY'
    away_team_name = 'MEM'

    predictor = WinningTeamPredictor()
    prediction = predictor.predict_winner(home_team_name, away_team_name)

    if prediction == 1:
        print(f"{home_team_name} is predicted to win.")
    else:
        print(f"{away_team_name} is predicted to win.")
