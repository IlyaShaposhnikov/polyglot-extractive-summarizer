import argparse
import logging
import sys

from summarizer import summarize
from wiki_fetcher import fetch_wikipedia_article
from file_handler import read_text_file

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr
    )
    logging.getLogger("wikipediaapi").setLevel(logging.WARNING)


def restricted_float(value: str) -> float:
    """
    Validate that the ratio is between 0.0 (exclusive) and 1.0 (inclusive).
    """
    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid float value: '{value}'")
    if not (0.0 < f <= 1.0):
        raise argparse.ArgumentTypeError(
            "Ratio must be between 0.0 (exclusive) and 1.0 (inclusive)"
        )
    return f


def main(
    source: str,
    is_file: bool,
    language: str,
    max_sents: int | None,
    sum_ratio: float | None
) -> None:
    """Fetch text from source and print its extractive summary."""
    try:
        if is_file:
            logger.info("Reading local file '%s'...", source)
            text, lang = read_text_file(source, language=language)
        else:
            logger.info("Fetching Wikipedia article '%s'...", source)
            text, lang = fetch_wikipedia_article(source, language=language)

        logger.info(
            "Text acquired. Language: '%s', Length: %d chars", lang, len(text)
        )

        logger.info("Summarizing...")
        summary = summarize(
            text=text,
            language=lang,
            max_sents=max_sents,
            sum_ratio=sum_ratio
        )
        logger.info("Summary generated (%d sentences)", len(summary))

        if not summary:
            logger.warning("No summary could be generated (empty result).")
            return

        print("\n" + "=" * 50)
        for i, sentence in enumerate(summary, 1):
            print(f"{i}. {sentence}")
        print("=" * 50 + "\n")

    except (ValueError, FileNotFoundError, UnicodeDecodeError) as e:
        logger.error("Input error: %s", e)
    except ConnectionError as e:
        logger.error("Network error: %s", e)
    except Exception:
        logger.exception("Unexpected error")


if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(
        description=(
            "Extractive summarizer for Wikipedia articles "
            "and local text files."
        )
    )
    parser.add_argument(
        "source",
        help="Wikipedia article URL/title OR path to a local .txt file"
    )
    parser.add_argument(
        "-f", "--file",
        action="store_true",
        help="Treat the source as a local file path instead of Wikipedia"
    )
    parser.add_argument(
        "-l", "--language",
        default=None,
        help="Language code (e.g., 'en', 'ru'). Required for local files."
    )

    size_group = parser.add_mutually_exclusive_group()
    size_group.add_argument(
        "-n", "--max-sents",
        type=int,
        help="Absolute number of sentences in the summary"
    )
    size_group.add_argument(
        "-r", "--ratio",
        type=restricted_float,
        help="Proportion of the original text length (e.g., 0.1 for 10%%)"
    )

    args = parser.parse_args()

    if args.file and args.language is None:
        parser.error("--language is required when using --file")

    # Fallback to 'en' only for Wikipedia
    # if language is not explicitly provided
    language = args.language or "en"

    main(
        source=args.source,
        is_file=args.file,
        language=language,
        max_sents=args.max_sents,
        sum_ratio=args.ratio
    )
