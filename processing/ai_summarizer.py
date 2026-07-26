import os
import sys
import json
import glob
from dotenv import load_dotenv
from google import genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import get_logger

logger = get_logger("ai_summarizer")


def main():
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment")
            return False

        client = genai.Client(api_key=api_key)

        json_files = glob.glob("data/raw/news_*.json")
        if not json_files:
            logger.error("No raw news files found in data/raw/")
            return False

        latest_file = max(json_files)
        logger.info(f"Reading file:{latest_file}")

        with open(latest_file, "r", encoding="utf-8") as file:
            articles = json.load(file)

        headlines = [article["title"] for article in articles[:15]]

        prompt = f"""
Summarize these news headlines into a WhatsApp morning brief. Rules:
- One line per topic/story.
- Start each line with a relevant emoji, then a short punchy one-liner (max ~15 words).
- Plain text only. Do NOT use markdown symbols like #, ##, **, or __ for formatting.
- Cover as many distinct topics as possible from the headlines below.
- Total message must stay under 1400 characters including spaces.

{chr(10).join(headlines)}

"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        summary = response.text

        with open("data/output/ai_morning_brief.txt", "w", encoding="utf-8") as file:
            file.write("📢 AI MORNING PULSE\n\n")
            file.write(summary)

        logger.info("AI Summary saved to data/output/ai_morning_brief.txt")
        return True

    except Exception as e:
        logger.error(f"ai_summarizer failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    main()