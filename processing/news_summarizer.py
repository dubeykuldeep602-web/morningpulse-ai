import os
import sys
import json
import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import get_logger

logger = get_logger("news_summarizer")


def categorize_news(title):
    title = title.lower()

    if "modi" in title or "india" in title:
        return "India"
    elif "nifty" in title or "sensex" in title or "market" in title or "stock" in title:
        return "Markets"
    elif "ai" in title or "google" in title or "microsoft" in title or "openai" in title:
        return "Technology"
    elif "sports" in title or "cricket" in title or "football" in title:
        return "Sports"
    elif "entertainment" in title or "bollywood" in title or "hollywood" in title:
        return "Entertainment"
    else:
        return "Other"


def main():
    try:
        json_files = glob.glob("data/raw/*.json")
        if not json_files:
            logger.error("No raw news files found in data/raw/")
            return False

        latest_file = max(json_files)
        logger.info(f"Reading file from {latest_file}")

        with open(latest_file, "r", encoding="utf-8") as file:
            articles = json.load(file)

        logger.info(f"Total Articles: {len(articles)}")

        categories = {
            "India": [], "Markets": [], "Technology": [],
            "Sports": [], "Entertainment": [], "Other": []
        }

        for article in articles:
            category = categorize_news(article["title"])
            categories[category].append(article["title"])

        morning_brief = "📢 MORNING PULSE\n\n"
        for category, headlines in categories.items():
            morning_brief += f"\n=== {category} ===\n"
            for headline in headlines[:3]:
                morning_brief += f"• {headline}\n"

        with open("data/output/morning_brief.txt", "w", encoding="utf-8") as file:
            file.write(morning_brief)

        logger.info("Morning brief saved to data/output/morning_brief.txt")
        return True

    except Exception as e:
        logger.error(f"news_summarizer failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    main()