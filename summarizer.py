from typing import List, Optional

from sumy.nlp.tokenizers import Tokenizer

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
        raise ValueError(f"Unsupported language: '{language}'. Supported: {supported}")
    
    lang_name = LANGUAGE_MAP[language]
    
    # Step 2: Tokenize text into sentences
    tokenizer = Tokenizer(lang_name)
    sentences = list(tokenizer.to_sentences(text))
    
    # Step 3: Calculate target_count.
    # Priority: max_sents > sum_ratio > default (0.2).
    # Ensure target_count does not exceed the total number of sentences.
    
    # Step 4: Initialize sumy parser and summarizer for the given language.
    # Run the summarization algorithm to get the top sentences.
    
    # Step 5: Map the selected sentences back to their original indices.
    # Sort them by index to preserve the original text order.
    
    # Step 6: Return the sorted list of sentences.
    
    pass
