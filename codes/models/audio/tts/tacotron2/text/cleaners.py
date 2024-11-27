import re
from unidecode import unidecode
from numbers import normalize_numbers

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
    ('mrs', 'misess'),
    ('mr', 'mister'),
    ('dr', 'doctor'),
    ('st', 'saint'),
    ('co', 'company'),
    ('jr', 'junior'),
    ('maj', 'major'),
    ('gen', 'general'),
    ('drs', 'doctors'),
    ('rev', 'reverend'),
    ('lt', 'lieutenant'),
    ('hon', 'honorable'),
    ('sgt', 'sergeant'),
    ('capt', 'captain'),
    ('esq', 'esquire'),
    ('ltd', 'limited'),
    ('col', 'colonel'),
    ('ft', 'fort'),
]]

def expand_abbreviations(text):
    """Expand common abbreviations."""
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text

def expand_numbers(text):
    """Expand numbers to words."""
    return normalize_numbers(text)

def lowercase(text):
    """Convert text to lowercase."""
    return text.lower()

def collapse_whitespace(text):
    """Collapse multiple whitespaces to a single space."""
    return re.sub(_whitespace_re, ' ', text)

def convert_to_ascii(text):
    """Convert text to ASCII representation."""
    return unidecode(text)

def normalize_urdu_text(text):
    """
    Normalize Urdu text:
    - Normalize Arabic-Urdu numerals
    - Remove extra spaces
    """
    # Normalize Arabic-Urdu numerals to standard form
    urdu_to_arabic_numerals = str.maketrans(
        '۰۱۲۳۴۵۶۷۸۹',
        '0123456789'
    )
    text = text.translate(urdu_to_arabic_numerals)
    
    # Remove extra spaces and normalize punctuation
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def basic_cleaners(text):
    """
    Basic pipeline that lowercases and collapses whitespace 
    without transliteration.
    """
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text

def transliteration_cleaners(text):
    """
    Pipeline for non-English text that transliterates to ASCII.
    """
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text

def english_cleaners(text):
    """
    Pipeline for English text, including normalization.
    """
    text = lowercase(text)
    text = expand_abbreviations(text)
    text = expand_numbers(text)
    text = collapse_whitespace(text)
    text = text.replace('"', '')
    return text

def urdu_cleaners(text):
    """
    Pipeline for Urdu text cleaning.
    """
    text = normalize_urdu_text(text)
    text = collapse_whitespace(text)
    text = text.replace('٫', '.').replace('٪', '%')
    return text

def multilingual_cleaners(text, language='english'):
    """
    Comprehensive multilingual text cleaning
    
    Args:
        text (str): Input text to clean
        language (str): 'english' or 'urdu'
    
    Returns:
        str: Cleaned text
    """
    if language == 'urdu':
        return urdu_cleaners(text)
    elif language == 'english':
        return english_cleaners(text)
    else:
        # Fallback to transliteration
        return transliteration_cleaners(text)
