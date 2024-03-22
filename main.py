from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import base64
from WinningTeamPredictor import WinningTeamPredictor
from GamesOddsCacheHandler import GamesOddsCacheHandler, ResponsesCacheHandler
from config import TEAMS_SHORT_TO_FULL_NAME
from Clients.OpenAIClient import OpenAIClient
from determine_winner import determine_winner

app = FastAPI()
model = WinningTeamPredictor()
games_cache_handler = GamesOddsCacheHandler()
openAiClient = OpenAIClient()
responseCacheHandler = ResponsesCacheHandler()


class PredictionRequest(BaseModel):
    home_team_short: str
    away_team_short: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the Sports Gambling API! Use /predict to make predictions."}


@app.get("/help")
def help_me():
    teams_string = "\n".join([f"{abbreviation} : {team}" for abbreviation, team in TEAMS_SHORT_TO_FULL_NAME.items()])
    help_message = f"Available teams:\n{teams_string} \n\n " \
                   f"Available commands:\n/predict <home team abbreviation> <away team abbreviation> " \
                   f"- Predict who will win."
    voice_byte_stream64 = get_voice_byte_stream("dont worry we will help you.", helpme=True)
    return {"message": help_message, "voice_byte_stream64": voice_byte_stream64}


def get_voice_byte_stream(text, helpme=False):
    if helpme:
        voice_byte_stream = openAiClient.get_bytes_stream_helpme()
    else:
        voice_byte_stream = openAiClient.get_bytes_stream(text)
    return base64.b64encode(voice_byte_stream).decode("utf-8")


@app.post("/predict_winner")
def predict_winner(request: PredictionRequest):
    home_team_short, away_team_short = request.home_team_short, request.away_team_short
    response = responseCacheHandler.get_response(home_team_short, away_team_short)
    if response:
        logging.info("prediction return from cache")
        return response

    out_message = ""
    try:
        # predict using model
        prediction = model.predict_winner(home_team_short, away_team_short)

        # fetch odds from cache
        game = games_cache_handler.get_game_odds(home_team_short, away_team_short)

        # if the odds doesn't exist in the cache, predict using only the model
        if game is None:
            out_message += "The game doesn't exist in the odds database. Predicting using only my brain... \n"
            winner, loser = (home_team_short, away_team_short) if prediction == 1 \
                else (away_team_short, home_team_short)

        else:  # if the odds exist in the cache, predict using both the model and the odds
            winner, loser = determine_winner(prediction, game)

        logging.info(f"home team: {home_team_short}, away team: {away_team_short}, winner: {winner}")

        response_dict = generate_prediction_output(winner, loser, out_message)
        responseCacheHandler.cache_response(home_team_short, away_team_short, response_dict)
        return response_dict

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch odds. Please try again later.")


def generate_prediction_output(winner: str, loser: str, out_message: str) -> dict:
    winner, loser = TEAMS_SHORT_TO_FULL_NAME[winner], TEAMS_SHORT_TO_FULL_NAME[loser]
    out_message += f"{winner} is predicted to win.\n"

    argument_paragraph = openAiClient.get_argument_paragraph(winner, loser)
    voice_byte_stream64 = get_voice_byte_stream(argument_paragraph)

    return {
        "message": out_message,
        "winner": winner,
        "argument_paragraph": argument_paragraph,
        "voice_byte_stream64": voice_byte_stream64
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
