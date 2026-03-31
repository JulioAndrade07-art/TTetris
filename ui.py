import pygame

# Constants
BLOCK_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Calculated window sizes
PLAY_WIDTH = GRID_WIDTH * BLOCK_SIZE
PLAY_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
WINDOW_WIDTH = PLAY_WIDTH + 400
WINDOW_HEIGHT = PLAY_HEIGHT + 180

TOP_LEFT_X = 50
TOP_LEFT_Y = 120

import math
tesseract_angle = 0.0

def draw_tesseract_boss(surface, cx, cy, boss_time, boss_time_max):
    global tesseract_angle
    tesseract_angle += 0.04
    
    size = 40
    o_v, i_v = [], []
    
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                # Rotate outer cube around Y/X
                nx = x * math.cos(tesseract_angle) - z * math.sin(tesseract_angle)
                nz = x * math.sin(tesseract_angle) + z * math.cos(tesseract_angle)
                ny = y * math.cos(tesseract_angle*0.7) - nz * math.sin(tesseract_angle*0.7)
                o_v.append((cx + nx * size, cy + ny * size))
                
                # Turn inner "4D" cube opposite
                nx2 = x * math.cos(-tesseract_angle) - z * math.sin(-tesseract_angle)
                nz2 = x * math.sin(-tesseract_angle) + z * math.cos(-tesseract_angle)
                ny2 = y * math.cos(-tesseract_angle*0.7) - nz2 * math.sin(-tesseract_angle*0.7)
                i_v.append((cx + nx2 * (size*0.4), cy + ny2 * (size*0.4)))

    edges = [
        (0,1), (1,3), (3,2), (2,0),
        (4,5), (5,7), (7,6), (6,4),
        (0,4), (1,5), (2,6), (3,7)
    ]
    
    color_outer = (0, 255, 255)
    color_inner = (255, 0, 255)
    color_conn = (100, 100, 255)
    
    # Boss pulse logic upon death doors
    if boss_time and boss_time_max and boss_time < 10000:
        pulse = abs(math.sin(pygame.time.get_ticks() / 150.0))
        color_outer = (255, int(150*pulse), int(150*pulse))
        color_inner = (255, 0, 0)
    
    # Render lines
    for i in range(8):
        pygame.draw.line(surface, color_conn, o_v[i], i_v[i], 1)
        
    for p1, p2 in edges:
        pygame.draw.line(surface, color_outer, o_v[p1], o_v[p2], 2)
        pygame.draw.line(surface, color_inner, i_v[p1], i_v[p2], 2)

# Colors (Neon Vibes)
BG_COLOR = (10, 5, 20)           # Deep dark purple-black
GRID_COLOR = (40, 30, 80)        # Dark violet for grid lines
BORDER_GLOW = (200, 0, 255)      # Neon purple border
TEXT_COLOR = (0, 255, 255)       # Neon cyan for text

pygame.font.init()
FONT_NAME = "Consolas"
FONT = pygame.font.SysFont(FONT_NAME, 22, bold=True)
HUGE_FONT = pygame.font.SysFont(FONT_NAME, 46, bold=True)
SMALL_FONT = pygame.font.SysFont(FONT_NAME, 16, bold=False)

try:
    from PIL import Image
except ImportError:
    Image = None

def load_gif_frames(filepath, width, height, alpha=150):
    if not Image:
        # Fallback to standard pygame un-animated fallback (e.g if no pip pilllow installed yet)
        try:
            bg = pygame.transform.scale(pygame.image.load(filepath), (width, height))
            ov = pygame.Surface((width, height))
            ov.set_alpha(alpha)
            ov.fill((0, 0, 0))
            bg.blit(ov, (0,0))
            return [bg]
        except:
            return []
    try:
        frames = []
        pil_img = Image.open(filepath)
        for frame_index in range(pil_img.n_frames):
            pil_img.seek(frame_index)
            frame_rgba = pil_img.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode).convert_alpha()
            scaled_image = pygame.transform.scale(pygame_image, (width, height))
            
            # Dark transparent overlay over the background for neon readability
            ov = pygame.Surface((width, height))
            ov.set_alpha(alpha)
            ov.fill((0, 0, 0))
            scaled_image.blit(ov, (0, 0))
            
            frames.append(scaled_image)
        return frames
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

BG1_FRAMES = []
BG2_FRAMES = []

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def init_backgrounds():
    global BG1_FRAMES, BG2_FRAMES
    BG1_FRAMES = load_gif_frames(resource_path("bg1.gif"), WINDOW_WIDTH, WINDOW_HEIGHT, alpha=150)
    BG2_FRAMES = load_gif_frames(resource_path("bg2.gif"), WINDOW_WIDTH, WINDOW_HEIGHT, alpha=180)

def get_current_frame(frames):
    if not frames:
        return None
    # Assuming ~10 frames per second standard for GIFs without precise timings parsed
    frame_index = (pygame.time.get_ticks() // 100) % len(frames)
    return frames[frame_index]

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont(FONT_NAME, size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

def draw_grid(surface):
    # Draw horizontal lines
    for i in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRID_COLOR, (TOP_LEFT_X, TOP_LEFT_Y + i*BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i*BLOCK_SIZE))
    # Draw vertical lines
    for j in range(GRID_WIDTH):
        pygame.draw.line(surface, GRID_COLOR, (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

    # Glowing Border
    pygame.draw.rect(surface, (100, 0, 150), (TOP_LEFT_X-5, TOP_LEFT_Y-5, PLAY_WIDTH+10, PLAY_HEIGHT+10), 5)
    pygame.draw.rect(surface, BORDER_GLOW, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 2)

def draw_neon_block(surface, x, y, color, letter):
    rect = (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    inner_rect = (TOP_LEFT_X + x * BLOCK_SIZE + 4, TOP_LEFT_Y + y * BLOCK_SIZE + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8)
    
    # Background (Darker shade)
    bg_color = (max(0, color[0]-150), max(0, color[1]-150), max(0, color[2]-150))
    pygame.draw.rect(surface, bg_color, rect)
    
    # Outer Glow
    glow_color = (color[0]//2, color[1]//2, color[2]//2)
    pygame.draw.rect(surface, glow_color, rect, 2)
    
    # Inner Bright Core
    pygame.draw.rect(surface, color, inner_rect, 2)

    if letter:
        # Neon text
        glow_text = FONT.render(letter, True, color)
        real_text = FONT.render(letter, True, (255, 255, 255))
        
        tx = TOP_LEFT_X + x * BLOCK_SIZE + (BLOCK_SIZE - real_text.get_width()) / 2
        ty = TOP_LEFT_Y + y * BLOCK_SIZE + (BLOCK_SIZE - real_text.get_height()) / 2
        
        # Glow Effect offsets
        surface.blit(glow_text, (tx - 1, ty - 1))
        surface.blit(glow_text, (tx + 1, ty + 1))
        # White Center
        surface.blit(real_text, (tx, ty))

def draw_window(surface, grid, current_piece, next_piece, score, phase, lines, last_word, combo, hardcore, boss_time=None, boss_time_max=None):
    # Retrieve the correct animated background layer from the global frame
    bg_img = get_current_frame(BG2_FRAMES)
    if bg_img:
        surface.blit(bg_img, (0, 0))
    else:
        surface.fill(BG_COLOR)

    # Title
    label = HUGE_FONT.render("NEON TETRIS", 1, (255, 0, 255))
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH + 40, TOP_LEFT_Y))

    # Next Piece display
    next_lbl = SMALL_FONT.render("PROXIMA PECA:", 1, (150, 150, 180))
    surface.blit(next_lbl, (TOP_LEFT_X + PLAY_WIDTH + 40, TOP_LEFT_Y + 60))
    if next_piece:
        for r, row in enumerate(next_piece.shape_matrix):
            for c, val in enumerate(row):
                if val:
                    # Offset to display nicely in the panel (Grid X ~ 11, Grid Y ~ 2.5)
                    draw_neon_block(surface, 11 + c, 2.5 + r, next_piece.color, next_piece.letters[r][c])

    # Draw HUD
    sy = TOP_LEFT_Y + 230
    
    def render_hud_item(title, value, y_pos, color=(0, 255, 255)):
        lbl = SMALL_FONT.render(title, 1, (150, 150, 180))
        val = FONT.render(str(value), 1, color)
        surface.blit(lbl, (TOP_LEFT_X + PLAY_WIDTH + 40, y_pos))
        surface.blit(val, (TOP_LEFT_X + PLAY_WIDTH + 40, y_pos + 20))

    render_hud_item("SCORE", score, sy)
    
    phase_text = f"{phase} / 3" if phase < 4 else "BOSS!"
    phase_color = (255, 255, 0) if phase < 4 else (255, 50, 50)
    render_hud_item("FASE", phase_text, sy + 60, phase_color)
    
    render_hud_item("LINES", lines, sy + 120, (0, 255, 100))
    render_hud_item("COMBO", f"x{combo}", sy + 180, (255, 100, 0))
    
    mode_color = (255, 50, 50) if hardcore else (100, 200, 255)
    render_hud_item("MODE", 'Hardcore' if hardcore else 'Normal', sy + 240, mode_color)

    if boss_time is not None and boss_time_max is not None:
        draw_tesseract_boss(surface, TOP_LEFT_X + (PLAY_WIDTH // 2), 40, boss_time, boss_time_max)

        # Time Bar over grid width (400)
        pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, 90, PLAY_WIDTH, 20))
        time_width = max(0, int(PLAY_WIDTH * (boss_time / boss_time_max)))
        pygame.draw.rect(surface, (0, 255, 255), (TOP_LEFT_X, 90, time_width, 20))
        
        secs = max(0, boss_time / 1000.0)
        lbl = SMALL_FONT.render(f"SOBREVIVA: {secs:.1f}s", 1, (0, 0, 0))
        lbl_x = TOP_LEFT_X + (PLAY_WIDTH // 2) - (lbl.get_width() // 2)
        surface.blit(lbl, (lbl_x, 92))

    if last_word:
        lbl = SMALL_FONT.render("ULTIMA PALAVRA:", 1, (150, 150, 180))
        surface.blit(lbl, (TOP_LEFT_X + PLAY_WIDTH + 40, sy + 320))
        lw_text = HUGE_FONT.render(last_word, 1, (0, 255, 100))
        surface.blit(lw_text, (TOP_LEFT_X + PLAY_WIDTH + 40, sy + 340))

    # Controls help
    help_texts = [
        "ARROWS: Move/Drop",
        "SPACE: Rotate",
        "ENTER: Hard Drop",
        "H: Toggle Hardcore",
        "F1: Debug Word"
    ]
    
    help_y = WINDOW_HEIGHT - 130
    for ht in help_texts:
        l = SMALL_FONT.render(ht, 1, (100, 100, 130))
        surface.blit(l, (TOP_LEFT_X + PLAY_WIDTH + 40, help_y))
        help_y += 20

    # Draw locked grid blocks
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.cells[y][x]
            if cell:
                draw_neon_block(surface, x, y, cell['color'], cell['letter'])

    # Draw current falling piece
    if current_piece:
        for r, row in enumerate(current_piece.shape_matrix):
            for c, val in enumerate(row):
                if val:
                    draw_neon_block(surface, current_piece.x + c, current_piece.y + r, current_piece.color, current_piece.letters[r][c])

    draw_grid(surface)
    pygame.display.update()
