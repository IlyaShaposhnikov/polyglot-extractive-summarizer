import logging
from pathlib import Path
from typing import Tuple

from languages import LANGUAGE_MAP

logger = logging.getLogger(__name__)


def read_text_file(file_path: str, language: str) -> Tuple[str, str]:
    """
    Read text content from a local .txt file.

    Args:
        file_path: Path to the text file.
        language: Language code (e.g., 'en', 'ru'). Must be supported.

    Returns:
        Tuple of (file_content, language_code).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the language is not provided, not supported,
                    or file is empty.
        UnicodeDecodeError: If the file is not valid UTF-8.
    """
    if not language:
        raise ValueError("Language code must be provided")

    if language not in LANGUAGE_MAP:
        supported = ", ".join(LANGUAGE_MAP.keys())
        raise ValueError(
            f"Unsupported language: '{language}'. Supported: {supported}"
        )

    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Text file not found: {path}")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"File '{path}' is not valid UTF-8. Please save it as UTF-8."
        ) from e

    if not text.strip():
        raise ValueError(f"File '{path}' is empty")

    logger.info(
        "Successfully read %d characters from '%s'", len(text), path.name
    )

    return text, language
