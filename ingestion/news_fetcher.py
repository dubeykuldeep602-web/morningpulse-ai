import os
import sys
import feedparser
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import get_logger

logger = get_logger("news_fetcher")

RSS_URL = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"


def main():
    try:
        feed = feedparser.parse(RSS_URL)

        if not feed.entries:
            logger.error("No articles found in RSS feed")
            return False

        articles = []
        for article in feed.entries:
            articles.append({
                "title": article.title,
                "link": article.link,
                "published": article.published
            })

        logger.info(f"Total Articles: {len(articles)}")

        os.makedirs("data/raw", exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        file_name = f"data/raw/news_{today}.json"

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(articles, file, indent=4)

        logger.info(f"Saved {len(articles)} articles to {file_name}")
        return True

    except Exception as e:
        logger.error(f"news_fetcher failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    main()