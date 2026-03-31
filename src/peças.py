import random

# Tetromino shapes (0 represents empty, 1 represents a block)
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'Z': [[1, 1, 0],
          [0, 1, 1]]
}

COLORS = {
    'I': (0, 255, 255),    # Cyan
    'J': (40, 100, 255),   # Blue
    'L': (255, 120, 0),    # Orange
    'O': (255, 255, 0),    # Yellow
    'S': (0, 255, 100),    # Lime
    'T': (200, 0, 255),    # Purple
    'Z': (255, 0, 100)     # Neon Pink
}

# Portuguese letter approximate relative frequencies
WEIGHTED_LETTERS = (
    "A" * 14 + "E" * 11 + "I" * 6 + "O" * 10 + "U" * 5 +
    "S" * 8 + "R" * 6 + "N" * 5 + "D" * 5 + "M" * 5 + "T" * 4 + "C" * 4 + "L" * 3 + "P" * 3 + "V" * 2 +
    "G" * 1 + "B" * 1 + "F" * 1 + "H" * 1 + "Z" * 1 + "X" * 1 + "Q" * 1 + "J" * 1 + "Ç" * 1
)
# Includes accented letters occasionally to allow making valid words, but to keep it simple
# It's better to just stick to A-Z and let the dictionary matcher be lenient, or we add accented letters.
# The vocabulary might have accents. Thus, let's include some accented letters optionally, 
# or just allow matching ignoring accents. In `palavras.py` we used exact match. 
# We'll stick to exact match and include standard letters. Rare accents make the game impossible, 
# so we might need `palavras.py` to unaccent words from `words.js` to match unaccented A-Z.
# For now, stick to basic letters.

def get_random_letter():
    return random.choice(WEIGHTED_LETTERS)

def get_boss_symbol():
    return random.choice(['+', '*', '/', '-', '@', '#', '!', '?'])

class Piece:
    def __init__(self, x, y, is_boss_piece=False):
        self.shape_name = random.choice(list(SHAPES.keys()))
        self.shape_matrix = SHAPES[self.shape_name]
        self.color = COLORS[self.shape_name]
        self.x = x
        self.y = y
        self.rotation = 0
        
        # Assign a random letter (or boss symbol) to each block
        self.letters = []
        for row in self.shape_matrix:
            row_letters = []
            for val in row:
                if val:
                    if is_boss_piece:
                        row_letters.append(get_boss_symbol())
                    else:
                        row_letters.append(get_random_letter())
                else:
                    row_letters.append(None)
            self.letters.append(row_letters)

    def rotate(self):
        """Rotates the matrix 90 degrees clockwise."""
        self.shape_matrix = [list(r) for r in zip(*self.shape_matrix[::-1])]
        self.letters = [list(r) for r in zip(*self.letters[::-1])]
