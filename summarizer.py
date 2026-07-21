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
    Extractive summarization of the given text.

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

    # Step 1: Validate language
    if language not in LANGUAGE_MAP:
        supported = ', '.join(LANGUAGE_MAP.keys())
        raise ValueError(
            f"Unsupported language: '{language}'. Supported: {supported}"
        )

    lang_name = LANGUAGE_MAP[language]

    # Step 2: Tokenize text into sentences
    tokenizer = Tokenizer(lang_name)
    sentences = list(tokenizer.to_sentences(text))

    if not sentences:
        return []

    total = len(sentences)

    # Step 3: Calculate target_count
    if max_sents is not None and max_sents > 0:
        target_count = max_sents
    elif sum_ratio is not None and 0.0 < sum_ratio <= 1.0:
        target_count = round(total * sum_ratio)
    else:
        target_count = round(total * 0.2)

    target_count = max(1, min(target_count, total))

    # Step 4: Initialize sumy parser and summarizer
    parser = PlaintextParser.from_string(text, tokenizer)
    summarizer = TextRankSummarizer()

    summary_sentences = summarizer(
        parser.document, sentences_count=target_count
    )
    selected_texts = [str(sent) for sent in summary_sentences]

    # Step 5: Restore original order
    sent_to_idx = {sent: idx for idx, sent in enumerate(sentences)}
    indexed_selected = [(sent_to_idx[text], text) for text in selected_texts]
    indexed_selected.sort(key=lambda x: x[0])
    result = [text for _, text in indexed_selected]

    # Step 6: Return the sorted list
    return result
