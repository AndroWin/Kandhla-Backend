"""
Republic of Kandhla - Profanity Filter
REQUIREMENTS.md: "Regex-based bad-word block list managed via Admin panel."
Ye module content posting ke dauran profanity check karta hai.

Admin panel se bad-word list manage hoti hai (Phase 2 mein ProfanityWord model add hoga).
Filhaal default hardcoded list + regex pattern matching use hota hai.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Default bad words list — Admin panel se override hogi
# Ye sirf fallback hai, production mein database se load hogi
DEFAULT_BAD_WORDS = [
    # Common abusive words (Hindi/Hinglish) — placeholder patterns
    r'\bgali\b',
    r'\bgaali\b',
    r'\bbadword\b',
    # English common profanity patterns
    r'\bfuck\w*\b',
    r'\bshit\w*\b',
    r'\bbitch\w*\b',
    r'\bass\b',
    r'\basshole\w*\b',
    r'\bdamn\w*\b',
    r'\bbastard\w*\b',
]


def get_bad_words_list():
    """
    Database se bad words list load karo.
    Admin panel se manage hoti hai.
    Agar database available nahi hai toh default list use hogi.
    """
    try:
        # Future: ProfanityWord model se load hoga
        # from moderation.models import ProfanityWord
        # words = ProfanityWord.objects.filter(is_active=True).values_list('pattern', flat=True)
        # if words:
        #     return list(words)
        pass
    except Exception as e:
        logger.warning(f"Bad words list database se load nahi ho paayi: {e}")

    return DEFAULT_BAD_WORDS


def check_profanity(text):
    """
    Text mein profanity check karo.

    Args:
        text (str): Check karne wala text content.

    Returns:
        tuple: (is_profane: bool, matched_words: list)
            - is_profane: True agar profanity detected
            - matched_words: Matched patterns ki list
    """
    if not text:
        return False, []

    bad_words = get_bad_words_list()
    matched = []

    text_lower = text.lower()

    for pattern in bad_words:
        try:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matched.append(pattern.replace(r'\b', '').replace(r'\w*', '*'))
        except re.error as e:
            logger.error(f"Invalid profanity regex pattern '{pattern}': {e}")
            continue

    return bool(matched), matched


def clean_text(text):
    """
    Text se profane words ko asterisks se replace karo.
    Optional utility — future use ke liye.

    Args:
        text (str): Original text.

    Returns:
        str: Cleaned text with profanity replaced by ***
    """
    if not text:
        return text

    bad_words = get_bad_words_list()
    cleaned = text

    for pattern in bad_words:
        try:
            cleaned = re.sub(
                pattern,
                '***',
                cleaned,
                flags=re.IGNORECASE,
            )
        except re.error:
            continue

    return cleaned
