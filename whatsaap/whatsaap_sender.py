import os
import sys
from dotenv import load_dotenv
from twilio.rest import Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import get_logger

logger = get_logger("whatsapp_sender")


def get_summary_text():
    ai_path = "data/output/ai_morning_brief.txt"
    fallback_path = "data/output/morning_brief.txt"

    if os.path.exists(ai_path):
        logger.info(f"Using AI summary from {ai_path}")
        with open(ai_path, "r", encoding="utf-8") as file:
            return file.read()

    if os.path.exists(fallback_path):
        logger.warning(f"AI summary not found, falling back to {fallback_path}")
        with open(fallback_path, "r", encoding="utf-8") as file:
            return file.read()

    logger.error("No summary file found - nothing to send")
    return None


def main():
    try:
        load_dotenv()

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_WHATSAPP_FROM")
        to_number = os.getenv("MY_WHATSAPP_NUMBER")

        if not all([account_sid, auth_token, from_number, to_number]):
            logger.error("Missing Twilio credentials or numbers in .env")
            return False

        summary = get_summary_text()
        if not summary:
            return False

        # WhatsApp messages have a length limit; trim if needed
        if len(summary) > 1600:
            summary = summary[:1550] + "\n\n...(truncated)"

        client = Client(account_sid, auth_token)

        # Split into chunks under Twilio's 1600-char WhatsApp limit
        chunk_size = 1500
        chunks = [summary[i:i + chunk_size] for i in range(0, len(summary), chunk_size)]

        for idx, chunk in enumerate(chunks, start=1):
            if len(chunks) > 1:
                chunk = f"({idx}/{len(chunks)})\n\n{chunk}"

            message = client.messages.create(
                from_=from_number,
                to=to_number,
                body=chunk
            )
            logger.info(f"WhatsApp message part {idx}/{len(chunks)} sent (SID: {message.sid})")

        return True

    except Exception as e:
        logger.error(f"whatsapp_sender failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    main()