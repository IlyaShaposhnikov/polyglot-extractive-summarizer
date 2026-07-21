import re
from typing import Optional, Tuple
from urllib.parse import unquote, urlparse

import wikipediaapi


def extract_language_from_url(url: str) -> Optional[str]:
    """Extract language code from a Wikipedia URL."""
    hostname = urlparse(url).hostname or ""
    match = re.match(r"^([a-z]{2})(?:\.m|\.zero)?\.wikipedia\.org$", hostname)
    return match.group(1) if match else None


def fetch_wikipedia_article(
    url_or_title: str,
    language: Optional[str] = None,
    user_agent: str = "Polyglot Summarizer/1.0"
) -> Tuple[str, str]:
    """
    Fetch Wikipedia article text by URL or title.

    Args:
        url_or_title: Full Wikipedia URL or article title.
        language: Language code (e.g., 'ru'). Required if title is provided.
        user_agent: User-Agent string for the API client.

    Returns:
        Tuple of (article_text, language_code).

    Raises:
        ValueError: If language cannot be determined, title is empty,
                    or article is not found.
        ConnectionError: If a network error occurs.
    """
    is_url = url_or_title.startswith(("http://", "https://"))

    if is_url:
        lang = extract_language_from_url(url_or_title)
        if not lang:
            raise ValueError(
                f"Cannot extract language from URL: {url_or_title}"
            )

        parsed = urlparse(url_or_title)
        if (
            not parsed.path.startswith("/wiki/")
            or len(parsed.path) <= len("/wiki/")
        ):
            raise ValueError(f"Invalid Wikipedia URL format: {url_or_title}")

        # Extract, decode, and clean the title
        title = unquote(parsed.path.split("/wiki/", 1)[1])
        title = title.split("#")[0]  # Remove URL fragments
    else:
        if not language:
            raise ValueError(
                "Language must be provided when using an article title"
            )
        lang = language
        title = url_or_title

    if not title.strip():
        raise ValueError("Article title cannot be empty")

    wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=lang)

    try:
        page = wiki.page(title)
    except Exception as e:
        raise ConnectionError(
            f"Network error while fetching article '{title}': {e}"
        ) from e

    if not page.exists():
        raise ValueError(f"Article '{title}' not found in {lang} Wikipedia")

    return page.text, lang
