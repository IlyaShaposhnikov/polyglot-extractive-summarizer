from typing import List, Optional

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer

from languages import LANGUAGE_MAP


def summarize(
    text: str,
    language: str,
    max_sents: Optional[int] = None,
    sum_ratio: Optional[float] = None
) -> List[str]:
    """
    Extractive summarization of the given text using TextRank.

    Args:
        text: The input text to summarize.
        language: Language code (e.g., 'en', 'ru').
        max_sents: Absolute number of sentences in the summary.
        sum_ratio: Proportion of the original text length (0.0 to 1.0).
                   Ignored if max_sents is provided.
                   Defaults to 0.2 if neither is provided.

    Returns:
        A list of sentences forming the summary in their original order.
    """
    if language not in LANGUAGE_MAP:
        supported = ', '.join(LANGUAGE_MAP.keys())
        raise ValueError(
            f"Unsupported language: '{language}'. Supported: {supported}"
        )

    lang_name = LANGUAGE_MAP[language]

    # Parse text and extract sentences
    tokenizer = Tokenizer(lang_name)
    parser = PlaintextParser.from_string(text, tokenizer)
    sentences = parser.document.sentences
    total = len(sentences)

    if total == 0:
        return []

    # Calculate target sentence count
    if max_sents is not None:
        if max_sents <= 0:
            raise ValueError("max_sents must be a positive integer")
        target_count = max_sents
    elif sum_ratio is not None:
        if not (0.0 < sum_ratio <= 1.0):
            raise ValueError("sum_ratio must be in range (0.0, 1.0]")
        target_count = round(total * sum_ratio)
    else:
        target_count = round(total * 0.2)

    target_count = max(1, min(target_count, total))

    # Generate summary
    summarizer = TextRankSummarizer()
    summary_sents = summarizer(parser.document, sentences_count=target_count)

    # Restore original order using object indices
    sent_index = {sent: idx for idx, sent in enumerate(sentences)}
    indices = sorted(sent_index[sent] for sent in summary_sents)

    return [str(sentences[i]) for i in indices]
