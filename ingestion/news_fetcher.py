import feedparser
import json
from datetime import datetime

rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    
feed =feedparser.parse(rss_url)

articles = []

for article in feed.entries:
    articles.append(
        {

            "title": article.title,
            "link": article.link,
            "published": article.published

        }
    )


print(f"Total Articles : {len(articles)}")
print(articles[0])



today = datetime.now().strftime("%Y-%m-%d")

file_name = f"data/raw/news_{today}.json"

with open(file_name, "w", encoding="utf-8") as file:
    json.dump(articles, file, indent=4)

print(f"Saved {len(articles)} articles to {file_name}")



