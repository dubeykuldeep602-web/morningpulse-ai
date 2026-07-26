import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.logger import get_logger
from processing.news_summarizer import main as run_news_summarizer
from processing.ai_summarizer import main as run_ai_summarizer

logger = get_logger("main")


def run_pipeline():
    logger.info("===== Pipeline run started =====")

    news_ok = run_news_summarizer()
    if news_ok:
        logger.info("Step 1/2 (rule-based summary) succeeded")
    else:
        logger.warning("Step 1/2 (rule-based summary) failed - continuing anyway")

    ai_ok = run_ai_summarizer()
    if ai_ok:
        logger.info("Step 2/2 (AI summary) succeeded")
    else:
        logger.warning("Step 2/2 (AI summary) failed")

    if not news_ok and not ai_ok:
        logger.error("Both summarizers failed - no output generated today")
    elif ai_ok:
        logger.info("Pipeline completed - AI summary available")
    else:
        logger.info("Pipeline completed - falling back to rule-based summary only")

    logger.info("===== Pipeline run finished =====")


if __name__ == "__main__":
    run_pipeline()