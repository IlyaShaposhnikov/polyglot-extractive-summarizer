import re
from typing import Tuple, Optional

import wikipediaapi


def extract_language_from_url(url: str) -> Optional[str]:
    """
    Extract language code from Wikipedia URL.

    Args:
        url: Wikipedia URL (e.g., 'https://ru.wikipedia.org/wiki/Python')

    Returns:
        Language code (e.g., 'ru') or None if not found.
    """
    pattern = r'https?://([a-z]{2})\.wikipedia\.org'
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    return None


def fetch_wikipedia_article(
        url_or_title: str, language: Optional[str] = None
) -> Tuple[str, str]:
    """
    Fetch Wikipedia article text by URL or title.

    Args:
        url_or_title: Either a full Wikipedia URL or article title.
        language: Language code (e.g., 'ru').
                  Required if url_or_title is a title.
                  Extracted from URL if url_or_title is a URL.

    Returns:
        Tuple of (article_text, language_code).

    Raises:
        ValueError: If language cannot be determined or article not found.
    """
    # Step 1: Determine if input is URL or title
    is_url = url_or_title.startswith(('http://', 'https://'))

    # Step 2: Extract or validate language
    if is_url:
        lang = extract_language_from_url(url_or_title)
        if lang is None:
            raise ValueError(
                f"Cannot extract language from URL: {url_or_title}"
            )
        # Extract article title from URL
        title = url_or_title.split('/wiki/')[-1]
    else:
        if language is None:
            raise ValueError(
                "Language must be provided when using article title"
            )
        lang = language
        title = url_or_title

    # Step 3: Initialize Wikipedia API client
    wiki = wikipediaapi.Wikipedia(
        user_agent=(
            'polyglot-extractive-summarizer (ilia.a.shaposhnikov@gmail.com)'
        ),
        language=lang
    )

    # Step 4: Fetch article
    page = wiki.page(title)

    # Step 5: Check if article exists
    if not page.exists():
        raise ValueError(f"Article '{title}' not found in {lang} Wikipedia")

    # Step 6: Return text and language
    return page.text, lang
