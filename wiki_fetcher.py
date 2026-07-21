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
    # Regex to match Wikipedia URL pattern: https://xx.wikipedia.org/...
    pattern = r'https?://([a-z]{2})\.wikipedia\.org'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    return None


def fetch_wikipedia_article(url_or_title: str, language: Optional[str] = None) -> Tuple[str, str]:
    """
    Fetch Wikipedia article text by URL or title.
    
    Args:
        url_or_title: Either a full Wikipedia URL or article title.
        language: Language code (e.g., 'ru'). Required if url_or_title is a title.
                  Extracted from URL if url_or_title is a URL.
    
    Returns:
        Tuple of (article_text, language_code).
    
    Raises:
        ValueError: If language cannot be determined or article not found.
    """
    # Step 1: Determine if input is URL or title
    # Step 2: Extract language from URL if needed
    # Step 3: Validate language
    # Step 4: Initialize Wikipedia API client
    # Step 5: Fetch article
    # Step 6: Return text and language
    
    pass
