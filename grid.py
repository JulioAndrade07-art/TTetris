class Grid:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        # grid cells will be dicts: {'color': (r,g,b), 'letter': 'A'} or None
        self.cells = [[None for _ in range(width)] for _ in range(height)]

    def is_valid_position(self, piece, move_x=0, move_y=0):
        for r, row in enumerate(piece.shape_matrix):
            for c, val in enumerate(row):
                if val:
                    new_x = piece.x + c + move_x
                    new_y = piece.y + r + move_y
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    if new_y >= 0 and self.cells[new_y][new_x] is not None:
                        return False
        return True

    def lock_piece(self, piece):
        for r, row in enumerate(piece.shape_matrix):
            for c, val in enumerate(row):
                if val:
                    grid_y = int(piece.y + r)
                    grid_x = int(piece.x + c)
                    if 0 <= grid_y < self.height:
                        self.cells[grid_y][grid_x] = {
                            'color': piece.color,
                            'letter': piece.letters[r][c]
                        }

    def clear_lines(self):
        cleared_lines_info = [] # List of {'chars': list, 'colors': list}
        
        lines_to_clear = []
        for y in range(self.height):
            if all(self.cells[y][x] is not None for x in range(self.width)):
                lines_to_clear.append(y)
                
        if not lines_to_clear:
            return cleared_lines_info
            
        for y in lines_to_clear:
            chars = [self.cells[y][x]['letter'] for x in range(self.width)]
            colors = [self.cells[y][x]['color'] for x in range(self.width)]
            cleared_lines_info.append({'chars': chars, 'colors': colors})
            
        # Remove the lines and insert new empty lines at the top
        for y in reversed(lines_to_clear):
            del self.cells[y]
            self.cells.insert(0, [None for _ in range(self.width)])
            
        return cleared_lines_info

    def add_garbage_lines(self, amount, letter_func):
        import random
        for _ in range(amount):
            # Destroy the top row inherently
            del self.cells[0]
            
            hole = random.randint(0, self.width - 1)
            new_line = []
            for x in range(self.width):
                if x == hole:
                    new_line.append(None)
                else:
                    new_line.append({
                        'color': (80, 80, 80), # Grey unyielding garbage hue
                        'letter': letter_func()
                    })
            self.cells.append(new_line)
