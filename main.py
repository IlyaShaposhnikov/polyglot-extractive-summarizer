import argparse
import logging
import sys

from summarizer import summarize
from wiki_fetcher import fetch_wikipedia_article


def setup_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr  # Separate logs from standard output
    )
    logging.getLogger("wikipediaapi").setLevel(logging.WARNING)


def main(url_or_title: str, language: str, max_sents: int) -> None:
    """Fetch a Wikipedia article and print its extractive summary."""
    try:
        logging.info("Fetching article '%s'...", url_or_title)
        text, lang = fetch_wikipedia_article(url_or_title, language=language)
        logging.info(
            "Article fetched. Language: '%s', Length: %d chars",
            lang, len(text)
        )

        logging.info("Summarizing...")
        summary = summarize(text=text, language=lang, max_sents=max_sents)
        logging.info("Summary generated (%d sentences)", len(summary))

        if not summary:
            logging.warning("No summary could be generated (empty result).")
            return

        print("\n" + "=" * 50)
        for i, sentence in enumerate(summary, 1):
            print(f"{i}. {sentence}")
        print("=" * 50 + "\n")

    except ValueError as ve:
        logging.error("Validation error: %s", ve)
    except ConnectionError as ce:
        logging.error("Network error: %s", ce)
    except Exception:
        logging.exception("Unexpected error")


if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Extractive summarizer for Wikipedia articles."
    )
    parser.add_argument("url_or_title", help="Wikipedia article URL or title")
    parser.add_argument(
        "-l", "--language", default="en",
        help="Language code (e.g., 'en', 'ru')"
    )
    parser.add_argument(
        "-n", "--max-sents", type=int, default=5,
        help="Number of sentences in summary"
    )

    args = parser.parse_args()
    main(args.url_or_title, args.language, args.max_sents)
