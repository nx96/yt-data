import re
from typing import Optional


def remove_accented_chars(text: str) -> str:
    accented = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    for word, initial in accented.items():
        text = text.replace(word.lower(), initial)
    return text

def remove_special_chars(text: str, remove_digits: Optional[bool] = False) -> str:
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    if remove_digits:
            pattern = re.compile(r'[^a-zA-Z\s]')
    
    return pattern.sub('', text)

def remove_extra_whitespace(text: str) -> str:  
    return re.sub('\s+', ' ',text)

