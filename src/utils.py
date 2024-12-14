import re
from typing import Optional

def delete_emojis(text):     
    emoji_pattern = re.compile( 
        "[" "\U0001F600-\U0001F64F" 
        "\U0001F300-\U0001F5FF" 
        "\U0001F680-\U0001F6FF" 
        "\U0001F700-\U0001F77F" 
        "\U0001F780-\U0001F7FF" 
        "\U0001F800-\U0001F8FF" 
        "\U0001F900-\U0001F9FF" 
        "\U0001FA00-\U0001FA6F" 
        "\U00002700-\U000027BF" 
        "\U000024C2-\U0001F251"
        "\U0001fae1" 
        "\u231A"
        "]+", flags=re.UNICODE ) 
    return emoji_pattern.sub(r'', text) 

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
    return re.sub('\s+', '',text)

def apply_all_format(text: str) -> str:
    text = remove_accented_chars(text)
    text = remove_special_chars(text)
    text = remove_extra_whitespace(text)
    return text.lower()

def list_without_empty(string: str, split: str) -> Optional[str]:
    list = string.split(split)
    return [x for x in list if x]

def parse_duration_to_seconds(duration):
    duration = duration.replace("PT", "")
    duration = duration.replace("S", "")

    if "H" in duration:
        replace = "*3600"
        if len(list_without_empty(duration,"H")) > 1:
            replace = replace + "+"
        duration = duration.replace("H", replace)
    
    if "M" in duration:
        replace = "*60"
        if len(list_without_empty(duration,"M")) > 1:
            replace = replace + "+"
        duration = duration.replace("M", replace)

    return int(eval(duration))