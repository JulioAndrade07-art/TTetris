import os
import sys
import unicodedata

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Read the massive new utf8 dict file
WORDS_FILE_PATH = resource_path("data/br-utf8.txt")

def strip_accents(text):
    # Unicodedata normalizes specific accented strings like 'ã' into base characters 'a'
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def load_words():
    words = set()
    try:
        with open(WORDS_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue
                clean_word = strip_accents(word).upper()
                words.add(clean_word)
    except Exception as e:
        print(f"Error loading words: {e}")
    return words

VALID_WORDS = load_words()

def get_word_score(word):
    if len(word) < 3:
        return 0
    # Base word score scales with sizing
    score = 10 + (len(word) - 3) * 5
    rare_letters = "QZJXWKYC"
    for char in word:
        if char in rare_letters:
            score += 5
    return score

def find_best_word(row_chars, min_len=3, max_len=10):
    s = "".join(row_chars).upper()
    best_word = None
    best_score = -1
    best_pos = None

    n = len(s)
    lower_bound = max(3, min_len)
    upper_bound = min(n, max_len)
    
    for length in range(lower_bound, upper_bound + 1):
        for i in range(n - length + 1):
            sub = s[i:i+length]
            if sub in VALID_WORDS:
                score = get_word_score(sub)
                if score > best_score:
                    best_score = score
                    best_word = sub
                    best_pos = (i, i+length-1)
                    
    if best_word:
        return best_pos, best_word, best_score
    return None
