from openai import OpenAI
from api_settings import OPENAI_KEY
from Clients import NewsApiClient


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_KEY)

    def get_bytes_stream(self, text):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )

        # speech_file_path = Path(__file__).parent / "helpme.mp3"
        # response.stream_to_file(speech_file_path)
        return response.content

    def get_argument_paragraph(self, winning_team, losing_team):
        winning_team_articles = NewsApiClient.get_news(winning_team),
        losing_team_articles = NewsApiClient.get_news(losing_team)
        prompt = f"""Write a short paragraph about why the {winning_team} would win the {losing_team} in their upcoming nba match.
        In your answer include reasons and facts from the following news articles: 
        {winning_team_articles}
        {losing_team_articles}"""
        message = [{"role": "user", "content": prompt}]

        response = self.client.chat.completions.create(
            messages=message,
            model="gpt-3.5-turbo"
        )

        answer = response.choices[0].message.content
        return answer

    @staticmethod
    def get_bytes_stream_helpme():
        with open("helpme.mp3", "rb") as file:
            return file.read()


if __name__ == "__main__":
    winning_team = "Los Angeles Lakers"
    losing_team = "Los Angeles Clippers"
    client = OpenAIClient()
    answer = client.get_argument_paragraph(winning_team, losing_team)
    print(answer)
