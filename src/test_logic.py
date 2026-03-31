import palavras

print(f"Loaded {len(palavras.VALID_WORDS)} words.")

def test_find_word(word_str):
    chars = list(word_str.ljust(10, 'X'))[:10]
    best = palavras.find_best_word(chars)
    print(f"Chars: {''.join(chars)} -> Best word found: {best}")

test_find_word("XAPEDRAXYZ")
test_find_word("ABACAXIXXX")
test_find_word("XABAFAXXXX")
test_find_word("RANDOMCHAR")
