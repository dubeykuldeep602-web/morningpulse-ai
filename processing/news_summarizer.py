import json
import glob


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


# Load news file
json_files = glob.glob("data/raw/*.json")

latest_file = max(json_files)

print(f"Reading file from {latest_file}")

with open(latest_file, "r", encoding="utf-8") as file:
    articles = json.load(file)
    
print(f"Total Articles: {len(articles)}")


# Create categories
categories = {
    "India": [],
    "Markets": [],
    "Technology": [],
    "Sports": [],
    "Entertainment": [],
    "Other": []
}


# Categorize articles
for article in articles:
    category = categorize_news(article["title"])
    categories[category].append(article["title"])


# Create report
morning_brief = "📢 MORNING PULSE\n\n"

for category, headlines in categories.items():

    morning_brief += f"\n=== {category} ===\n"

    for headline in headlines[:3]:
        morning_brief += f"• {headline}\n"


# Save report
with open("data/output/morning_brief.txt", "w", encoding="utf-8") as file:
    file.write(morning_brief)

print("Morning brief saved to data/output/morning_brief.txt")