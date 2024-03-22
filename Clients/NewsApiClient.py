import requests
import urllib.parse
from api_settings import NEWS_API_KEY


def get_news(query: str) -> str:
    query = urllib.parse.quote(query)
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=relevancy&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response["articles"][:3]
    text = [article["title"] + article["description"] + article["content"] for article in articles]
    return "\n".join(text)


if __name__ == "__main__":
    news = get_news("Miami Heat")
    print(news)
