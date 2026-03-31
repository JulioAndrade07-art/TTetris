import pygame
import sys
from grid import Grid
from peças import Piece
import palavras
from ui import draw_window, draw_text_middle, WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris Words")

try:
    icon_img = pygame.image.load(resource_path("icon.jpg"))
    pygame.display.set_icon(icon_img)
except:
    pass

import ui
ui.init_backgrounds()

try:
    sfx_point = pygame.mixer.Sound(resource_path("sfx_point.mp3"))
except:
    sfx_point = None

current_volume = 0.5
try:
    pygame.mixer.music.load(resource_path("theme.mp3"))
    pygame.mixer.music.set_volume(current_volume)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"BGM Error: {e}")

def main(difficulty='normal'):
    grid = Grid()
    current_piece = Piece(3, 0)
    next_piece = Piece(3, 0)
    
    clock = pygame.time.Clock()
    fall_time = 0
    
    if difficulty == 'facil':
        fall_speed = 0.6
        boss_time_max = 30000
        boss_attack_rate = 15000
        word_min_len = 3
        word_max_len = 10
    elif difficulty == 'dificil':
        fall_speed = 0.25
        boss_time_max = 90000
        boss_attack_rate = 7000
        word_min_len = 8
        word_max_len = 10
    else:
        fall_speed = 0.4
        boss_time_max = 60000
        boss_attack_rate = 10000
        word_min_len = 3
        word_max_len = 7
    
    score = 0
    lines_cleared = 0
    phase = 1
    boss_time = boss_time_max
    boss_attack_timer = 0
    last_word = ""
    combo = 1
    hardcore_mode = False
    
    run = True
    game_over = False
    game_won = False

    while run:
        dt = clock.tick(60)
        fall_time += dt

        # Phase progression
        if phase == 1 and lines_cleared >= 5:
            phase = 2
        elif phase == 2 and lines_cleared >= 10:
            phase = 3
        elif phase == 3 and lines_cleared >= 15:
            phase = 4 # Boss Phase!

        # Boss Attack Logic
        if phase == 4 and not game_over and not game_won:
            boss_time -= dt
            if boss_time <= 0:
                game_won = True
                
            boss_attack_timer += dt
            if boss_attack_timer > boss_attack_rate: # Scales with difficulty
                boss_attack_timer = 0
                import peças
                grid.add_garbage_lines(1, peças.get_boss_symbol)

        # Speed modifiers based on phase
        current_speed = fall_speed - ((phase - 1) * 0.05)
        if current_speed < 0.1:
            current_speed = 0.1

        # Piece falling logic
        if not game_over and not game_won and fall_time / 1000 > current_speed:
            fall_time = 0
            if grid.is_valid_position(current_piece, move_y=1):
                current_piece.y += 1
            else:
                grid.lock_piece(current_piece)
                cleared_lines = grid.clear_lines()
                
                # Scoring Logic
                lines_this_turn = len(cleared_lines)
                if lines_this_turn > 0:
                    if sfx_point:
                        sfx_point.play()
                    lines_cleared += lines_this_turn
                    words_found = 0
                    for line_info in cleared_lines:
                        chars = line_info['chars']
                        best_word_info = palavras.find_best_word(chars, min_len=word_min_len, max_len=word_max_len)
                        
                        if best_word_info:
                            pos, word, word_score = best_word_info
                            score += word_score * combo
                            last_word = word
                            words_found += 1
                        else:
                            if not hardcore_mode:
                                score += 1 * combo
                    
                    if words_found > 0:
                        combo += 1
                    else:
                        combo = 1
                
                # Check game over condition
                current_piece = next_piece
                import random
                is_boss = (phase == 4 and random.random() < 0.3)
                next_piece = Piece(3, 0, is_boss_piece=is_boss)
                if not grid.is_valid_position(current_piece):
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    if grid.is_valid_position(current_piece, move_x=-1):
                        current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if grid.is_valid_position(current_piece, move_x=1):
                        current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if grid.is_valid_position(current_piece, move_y=1):
                        current_piece.y += 1
                elif event.key == pygame.K_SPACE:
                    current_piece.rotate()
                    if not grid.is_valid_position(current_piece):
                        # Simple kick back (revert rotation)
                        for _ in range(3):
                            current_piece.rotate()
                elif event.key == pygame.K_RETURN:
                    # Hard drop
                    while grid.is_valid_position(current_piece, move_y=1):
                        current_piece.y += 1
                    fall_time = 999999 # force immediate lock on next tick
                elif event.key == pygame.K_h:
                    hardcore_mode = not hardcore_mode
                elif event.key == pygame.K_F1:
                    # Cheat key: populate the bottom row with the word "PEDRA" wrapped in random chars
                    # This demonstrates recognizing a 5 letter word
                    grid.cells[grid.height-1] = [
                        {'color': (150,150,150), 'letter': 'X'},
                        {'color': (150,150,150), 'letter': 'Y'},
                        {'color': (255,0,0), 'letter': 'P'},
                        {'color': (255,0,0), 'letter': 'E'},
                        {'color': (255,0,0), 'letter': 'D'},
                        {'color': (255,0,0), 'letter': 'R'},
                        {'color': (255,0,0), 'letter': 'A'},
                        {'color': (150,150,150), 'letter': 'Z'},
                        {'color': (150,150,150), 'letter': 'W'},
                        {'color': (150,150,150), 'letter': 'K'},
                    ]
                    # We don't automatically clear it, the next block drop that fills a line will trigger logic,
                    # but wait, the cheat just sets the bottom line which is ALREADY FULL!
                    # Next piece drop will trigger clear_lines if it locks, or even immediately if we run it!
                    pass

        draw_window(WIN, grid, current_piece, next_piece, score, phase, lines_cleared, last_word, combo, hardcore_mode, boss_time=boss_time if phase==4 else None, boss_time_max=boss_time_max if phase==4 else None)

        if game_won:
            draw_text_middle(WIN, "VOCE SOBREVIVEU!", 50, (0, 255, 100))
            pygame.display.update()
            pygame.time.delay(4000)
            run = False
        elif game_over:
            draw_text_middle(WIN, "GAME OVER", 60, (255, 0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False

def draw_button(surface, text, font, color, rect, hover=False):
    # draws a neon hollow button
    bg_color = (max(0, color[0]-150), max(0, color[1]-150), max(0, color[2]-150))
    if hover:
        bg_color = (max(0, color[0]-100), max(0, color[1]-100), max(0, color[2]-100))
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, color, rect, 2)
    
    text_surf = font.render(text, 1, color)
    surface.blit(text_surf, (rect[0] + (rect[2] - text_surf.get_width())//2, rect[1] + (rect[3] - text_surf.get_height())//2))

def tutorial_screen():
    import ui
    run = True
    while run:
        bg_img = ui.get_current_frame(ui.BG1_FRAMES)
        if bg_img:
            WIN.blit(bg_img, (0, 0))
        else:
            WIN.fill(ui.BG_COLOR)
        pygame.draw.rect(WIN, ui.BORDER_GLOW, (20, 20, ui.WINDOW_WIDTH-40, ui.WINDOW_HEIGHT-40), 3)

        title = ui.HUGE_FONT.render("TUTORIAL", 1, (0, 255, 255))
        WIN.blit(title, (ui.WINDOW_WIDTH//2 - title.get_width()//2, 50))

        lines = [
            "Bem-vindo ao NEON TETRIS WORDS!",
            "",
            "OBJETIVO:",
            "  Forme linhas horizontais completas para limpar a grade.",
            "  BONUS: Se a linha formar palavras em portugues (4+ letras),",
            "  voce ganha +10 pontos extras e multiplica seu Combo!",
            "",
            "CONTROLES:",
            "  [ESQUERDA / DIREITA] Move a peca",
            "  [BAIXO] Acelera a queda",
            "  [ESPACO] Gira a peca",
            "  [ENTER] Queda Instantanea (Hard Drop)",
            "  [H] Ativa Modo Hardcore",
            "",
            "MODO HARDCORE:",
            "  Normalmente, qualquer linha limpa da +1 ponto.",
            "  No modo Hardcore, linhas sem palavras valem 0 pontos!",
            "",
            "Pressione [ESC] para voltar ao Menu"
        ]

        sy = 150
        for line in lines:
            text_surf = ui.FONT.render(line, 1, (200, 200, 255))
            WIN.blit(text_surf, (50, sy))
            sy += 35
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

def difficulty_menu():
    import ui
    import sys
    run = True
    while run:
        bg_img = ui.get_current_frame(ui.BG1_FRAMES)
        if bg_img:
            WIN.blit(bg_img, (0, 0))
        else:
            WIN.fill(ui.BG_COLOR)
        
        title = ui.HUGE_FONT.render("DIFICULDADE", 1, (0, 255, 255))
        WIN.blit(title, (ui.WINDOW_WIDTH//2 - title.get_width()//2, 100))

        mx, my = pygame.mouse.get_pos()
        btn_w, btn_h = 250, 60
        btn_x = ui.WINDOW_WIDTH//2 - btn_w//2

        btn_facil = (btn_x, 250, btn_w, btn_h)
        btn_normal = (btn_x, 350, btn_w, btn_h)
        btn_dificil = (btn_x, 450, btn_w, btn_h)
        btn_voltar = (btn_x, 550, btn_w, btn_h)

        h_facil = btn_facil[0] <= mx <= btn_facil[0]+btn_facil[2] and btn_facil[1] <= my <= btn_facil[1]+btn_facil[3]
        h_norm = btn_normal[0] <= mx <= btn_normal[0]+btn_normal[2] and btn_normal[1] <= my <= btn_normal[1]+btn_normal[3]
        h_dif = btn_dificil[0] <= mx <= btn_dificil[0]+btn_dificil[2] and btn_dificil[1] <= my <= btn_dificil[1]+btn_dificil[3]
        h_vol = btn_voltar[0] <= mx <= btn_voltar[0]+btn_voltar[2] and btn_voltar[1] <= my <= btn_voltar[1]+btn_voltar[3]

        draw_button(WIN, "FACIL", ui.FONT, (0, 255, 100), btn_facil, h_facil)
        draw_button(WIN, "NORMAL", ui.FONT, (255, 255, 0), btn_normal, h_norm)
        draw_button(WIN, "DIFICIL", ui.FONT, (255, 0, 100), btn_dificil, h_dif)
        draw_button(WIN, "VOLTAR", ui.FONT, (150, 150, 150), btn_voltar, h_vol)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if h_facil:
                    main('facil')
                    run = False
                elif h_norm:
                    main('normal')
                    run = False
                elif h_dif:
                    main('dificil')
                    run = False
                elif h_vol:
                    run = False

def start_menu():
    global current_volume
    import ui
    run = True
    while run:
        bg_img = ui.get_current_frame(ui.BG1_FRAMES)
        if bg_img:
            WIN.blit(bg_img, (0, 0))
        else:
            WIN.fill(ui.BG_COLOR)
        
        # Title
        title = ui.HUGE_FONT.render("NEON TETRIS", 1, (255, 0, 255))
        WIN.blit(title, (ui.WINDOW_WIDTH//2 - title.get_width()//2, 100))

        subtitle = ui.FONT.render("W O R D S", 1, (0, 255, 255))
        WIN.blit(subtitle, (ui.WINDOW_WIDTH//2 - subtitle.get_width()//2, 160))

        # Buttons
        mx, my = pygame.mouse.get_pos()

        btn_w, btn_h = 250, 60
        btn_x = ui.WINDOW_WIDTH//2 - btn_w//2

        play_rect = (btn_x, 260, btn_w, btn_h)
        tut_rect = (btn_x, 340, btn_w, btn_h)
        vol_rect = (btn_x, 420, btn_w, btn_h)
        quit_rect = (btn_x, 500, btn_w, btn_h)

        play_hover = play_rect[0] <= mx <= play_rect[0]+play_rect[2] and play_rect[1] <= my <= play_rect[1]+play_rect[3]
        tut_hover = tut_rect[0] <= mx <= tut_rect[0]+tut_rect[2] and tut_rect[1] <= my <= tut_rect[1]+tut_rect[3]
        vol_hover = vol_rect[0] <= mx <= vol_rect[0]+vol_rect[2] and vol_rect[1] <= my <= vol_rect[1]+vol_rect[3]
        quit_hover = quit_rect[0] <= mx <= quit_rect[0]+quit_rect[2] and quit_rect[1] <= my <= quit_rect[1]+quit_rect[3]

        draw_button(WIN, "JOGAR", ui.FONT, (0, 255, 100), play_rect, play_hover)
        draw_button(WIN, "TUTORIAL", ui.FONT, (255, 255, 0), tut_rect, tut_hover)
        
        vol_text = f"MUSICA: {int(current_volume * 100)}%"
        draw_button(WIN, vol_text, ui.FONT, (100, 200, 255), vol_rect, vol_hover)
        
        draw_button(WIN, "SAIR", ui.FONT, (255, 0, 100), quit_rect, quit_hover)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_hover:
                        difficulty_menu()
                    elif tut_hover:
                        tutorial_screen()
                    elif vol_hover:
                        current_volume -= 0.5
                        if current_volume < 0:
                            current_volume = 1.0
                        pygame.mixer.music.set_volume(current_volume)
                    elif quit_hover:
                        run = False
                        pygame.quit()
                        sys.exit()

if __name__ == '__main__':
    start_menu()
