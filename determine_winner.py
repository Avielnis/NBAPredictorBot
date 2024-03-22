from Clients.OddsApiClient import Game
import config
import logging

ODDS_THRESHOLD = 0.75


def determine_winner(model_prediction: int, game: Game) -> tuple[str, str]:
    if model_prediction == 1 and game.predict_winner() == 1:
        logging.info("Both Model and Odds agreed on Winner")
        return game.home_team, game.away_team

    if model_prediction == 0 and game.predict_winner() == 0:
        logging.info("Both Model and Odds agreed on Winner")
        return game.away_team, game.home_team

    logging.info("Both Model and Odds didn't agree on Winner")
    if model_prediction == 1 and (1 / game.away_team_price) > ODDS_THRESHOLD:
        logging.info("Odds too good for away team - picking away")
        logging.info("Choosing odds prediction")
        return game.away_team, game.home_team
    elif model_prediction == 1 and (1 / game.away_team_price) <= ODDS_THRESHOLD:
        logging.info("Odds not good enough for away team - picking home")
        logging.info("Choosing model prediction")
        return game.home_team, game.away_team
    elif model_prediction == 0 and (1 / game.home_team_price) > ODDS_THRESHOLD:
        logging.info("Odds too good for home team - picking home")
        logging.info("Choosing odds prediction")
        return game.home_team, game.away_team
    else:
        logging.info("Odds not good enough for home team - picking away")
        logging.info("Choosing model prediction")
        return game.away_team, game.home_team
