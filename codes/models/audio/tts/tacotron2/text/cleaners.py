"""
Mixed Urdu-English Text Cleaner for Humanized TTS

This cleaner processes Urdu text while seamlessly handling interspersed English words.
It expands abbreviations, normalizes numbers, handles punctuation, and prepares text
for natural-sounding text-to-speech synthesis.
"""

import re
from .numbers_urdu import normalize_numbers_urdu
from unidecode import unidecode  # For English transliteration if needed

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# Define common Urdu abbreviations and their expanded forms:
_abbreviations_urdu = [
    (re.compile(r'\bجناب\b', re.IGNORECASE), 'جناب محترم'),
    (re.compile(r'\bڈاکٹر\b', re.IGNORECASE), 'ڈاکٹر'),
    (re.compile(r'\bمحترمہ\b', re.IGNORECASE), 'محترمہ'),
    (re.compile(r'\bپروف\b', re.IGNORECASE), 'پروفیسر'),
    (re.compile(r'\bایم ایل اے\b', re.IGNORECASE), 'رکن صوبائی اسمبلی'),
    (re.compile(r'\bایم این اے\b', re.IGNORECASE), 'رکن قومی اسمبلی'),
    # Add more abbreviations as needed
]

# Urdu-specific punctuation normalization:
_punctuation_replacements = {
    '۔': '.',  # Urdu full stop to period
    '،': ',',  # Urdu comma to English comma
    '؛': ';',  # Urdu semicolon to English semicolon
    '؟': '?',  # Urdu question mark to English question mark
    '!' : '!', # Urdu exclamation mark to English exclamation mark
    '“': '"',  # Urdu opening quotation mark to English
    '”': '"',  # Urdu closing quotation mark to English
    '‘': "'",  # Urdu single quote to English
    '’': "'",  # Urdu single quote to English
}

# Special characters to be removed or normalized:
_special_characters = ['؂', '؃', '؏', '؎', 'ؐ', 'ؑ', 'ؒ', 'ؓ', 'ؔ', 'ؕ', 'ؖ', 'ؗ', 'ؘ', 'ؙ', 'ؚ']

# Language detection regex for simple Urdu and English separation:
_urdu_regex = re.compile(r'[\u0600-\u06FF]+')  # Matches Urdu script
_english_regex = re.compile(r'[a-zA-Z]+')      # Matches English words


def normalize_punctuation(text):
    '''Normalize Urdu punctuation marks.'''
    for urdu_punct, english_punct in _punctuation_replacements.items():
        text = text.replace(urdu_punct, english_punct)
    return text


def remove_special_characters(text):
    '''Remove unnecessary special characters from Urdu text.'''
    for char in _special_characters:
        text = text.replace(char, '')
    return text


def expand_abbreviations_urdu(text):
    '''Expand common Urdu abbreviations to their full forms.'''
    for regex, replacement in _abbreviations_urdu:
        text = re.sub(regex, replacement, text)
    return text


def normalize_numbers_mixed(text):
    '''
    Normalize Urdu and English numbers:
    Convert Urdu numerals to Arabic numerals (1, 2, 3) and retain English numbers.
    '''
    text = normalize_numbers_urdu(text)  # Custom function for Urdu numerals
    return text


def process_mixed_language(text):
    '''
    Process mixed Urdu-English text:
    Retains English words and ensures Urdu-specific cleaning.
    '''
    # Split by whitespace to process word by word
    words = text.split()
    processed_words = []

    for word in words:
        if _urdu_regex.search(word):  # If the word is Urdu
            word = normalize_numbers_urdu(word)
            word = expand_abbreviations_urdu(word)
        elif _english_regex.search(word):  # If the word is English
            word = unidecode(word)  # Ensure ASCII compatibility
        processed_words.append(word)

    return ' '.join(processed_words)


def collapse_whitespace(text):
    '''Collapse multiple spaces into a single space.'''
    return re.sub(_whitespace_re, ' ', text)


def humanize_mixed_cleaners(text):
    '''
    Full pipeline for humanizing mixed Urdu-English text:
    Normalizes punctuation, removes special characters, expands abbreviations,
    processes mixed language, and collapses whitespace.
    '''
    text = normalize_punctuation(text)
    text = remove_special_characters(text)
    text = process_mixed_language(text)
    text = collapse_whitespace(text)
    return text
