from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "6171c86231c94c1b89336f713c75cf28"

CATEGORIES = {
    "general": "General News",
    "business": "Economy & Finance",
    "politics": "Politics",
    "sports": "Sports"
}

def fetch_headlines(category, country='us', max_articles=5):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country={country}&apiKey={API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    seen_titles = set()
    unique_articles = []

    for article in articles:
        title = article["title"]
        if title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append({
                "title": title,
                "source": article["source"]["name"],
                "url": article["url"]
            })

        if len(unique_articles) >= max_articles:
            break

    if not unique_articles:
        return [f"No unique articles found for {CATEGORIES.get(category, category)}."]
    
    return unique_articles


    if not articles:
        return [f"No articles found for {CATEGORIES.get(category, category)}."]

    return [{
        "title": article["title"],
        "source": article["source"]["name"],
        "url": article["url"]
    } for article in articles]




@app.route("/")
def home():
    news_data = {cat: fetch_headlines(cat) for cat in CATEGORIES}
    today = datetime.now().strftime("%Y-%m-%d")

    html = """
    <html>
    <head>
    <title>🗞 Daily News Agent</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to right, #f0f4ff, #eaf2ff);
            color: #333;
        }
        header {
            background-color: #003366;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 900px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        }
        h2 {
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
            color: #003366;
        }
        .headline {
            margin: 10px 0;
            font-size: 1.05em;
        }
        footer {
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
            color: #666;
        }
    </style>
    </head>
    <body>
    <header>
        <h1>🗞 Daily News Headlines – {{ today }}</h1>
    </header>
    <div class="container">
        {% for category, headlines in news_data.items() %}
            <div class="section">
                <h2>{{ categories[category] }}</h2>
                {% for headline in headlines %}
                    <div class="headline">
                     • <a href="{{ headline.url }}" target="_blank">{{ headline.title }} ({{ headline.source }})</a>
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
    </div>
    <footer>
        Powered by NewsAPI • Built by Pedro 😎
    </footer>
    </body>
    </html>
    """

    return render_template_string(html, news_data=news_data, categories=CATEGORIES, today=today)

if __name__ == "__main__":
    if __name__ == "__main__":
        import os
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
