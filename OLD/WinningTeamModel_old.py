import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


class WinningTeamModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.label_encoder = LabelEncoder()

    def train_model(self):
        if self.model:
            raise ValueError('Model already trained')

        df = pd.read_csv('../DataSets/nba_games_with_team_stats.csv')

        df['HomeTeam'] = self.label_encoder.fit_transform(df['HomeTeam'])
        df['AwayTeam'] = self.label_encoder.transform(df['AwayTeam'])

        X = df[['HomeTeam', 'AwayTeam']]
        y = df['HomeTeamScore'] > df['AwayTeamScore']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        logreg_model = LogisticRegression()
        logreg_model.fit(X_train, y_train)

        y_pred = logreg_model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')
        print(classification_report(y_test, y_pred))

        self.model = logreg_model
        joblib.dump(self.model, self.model_path)

        return logreg_model

    def predict_winner(self, home_team, away_team):
        if not self.model:
            raise ValueError('Model not trained yet')

        home_team_encoded = self.label_encoder.transform([home_team])[0]
        away_team_encoded = self.label_encoder.transform([away_team])[0]
        winning_team_prediction = self.model.predict([[home_team_encoded, away_team_encoded]])
        if winning_team_prediction[0]:
            return home_team
        else:
            return away_team


if __name__ == '__main__':
    model = WinningTeamModel(model_path='WinningTeamModel_v1.pkl')
    model.train_model()
    print('Model trained and saved to WinningTeamModel_v1.pkl')

    prediction = model.predict_winner('CHI', 'MIA')
    print(f'{prediction} will win')
