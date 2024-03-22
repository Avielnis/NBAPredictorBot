import logging
import config
from api_settings import TELEGRAM_BOT_TOKEN
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import base64


fast_api_url = "http://127.0.0.1:8000"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f"{fast_api_url}/")
    message: str = response.json()["message"]
    message = message.replace("API", "API bot")
    await update.message.reply_text(message)


async def help_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f"{fast_api_url}/help").json()
    help_message = response["message"]
    voice_byte_stream64 = response["voice_byte_stream64"]
    await update.message.reply_text(help_message)
    await send_voice(update, context, voice_byte_stream64)


async def predict_winner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text("Missing teams arguments")
        return
    params = {"home_team_short": context.args[0], "away_team_short": context.args[1]}
    try:
        await update.message.reply_text("Calculating odds..\nPlease Wait.")
        response = requests.post(f"{fast_api_url}/predict_winner", json=params).json()
        message = response["message"]
        argument_paragraph = response["argument_paragraph"]
        voice_byte_stream64 = response["voice_byte_stream64"]

        for sentence in message.split("\n"):
            if sentence != '' and sentence is not None:
                await update.message.reply_text(sentence)
        await update.message.reply_text(argument_paragraph)
        await send_voice(update, context, voice_byte_stream64)

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Failed to fetch odds. Please try again later.")


async def send_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, audio_byte_stream64):
    audio_byte_stream = base64.b64decode(audio_byte_stream64)
    await context.bot.send_voice(chat_id=update.message.chat_id, voice=audio_byte_stream)


def main():
    logging.info("Starting bot")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_me))
    app.add_handler(CommandHandler("predict", predict_winner))

    app.run_polling()


if __name__ == '__main__':
    main()
