# Neon Tetris Words

![Icon](assets/67cdf844-cc1e-4ace-b299-d964ae65e561.jpg)

**Neon Tetris Words** é um jogo arcade 2D com temática neon que combina as mecânicas clássicas de Tetris com o desafio de formar palavras. Sobreviva à queda das peças, complete linhas e forme palavras válidas em português para ganhar pontos extras e acumular combos!

*[English version below](#english-version)*

---

## 🇧🇷 Português (PT-BR)

### Características Principais
* **Clássico + Palavras**: Linhas completas dão pontos, mas se você formar palavras (3+ letras), ganhará pontos bônus e multiplicadores de combo!
* **Dificuldades Dinâmicas**: Jogue no Fácil, Normal ou Difícil.
* **Batalha contra o Chefe**: Na fase 4, você precisará sobreviver contra peças corrompidas e ataques contínuos.
* **Modo Hardcore**: Linhas normais não dão pontos. Apenas palavras formadas pontuam!
* **Estética Neon**: Gráficos brilhantes, GIFs animados de fundo e música imersiva.

### Controles
| Tecla | Ação |
|---|---|
| `⬅️` / `➡️` | Mover a peça para a esquerda / direita |
| `⬇️` | Acelerar a queda |
| `ESPAÇO` | Girar a peça |
| `ENTER` | Queda Rápida (Hard Drop) |
| `H` | Ativar/Desativar modo Hardcore |
| `ESC` | Voltar aos menus (Tutorial) |

### Como Executar do Código Fonte
Certifique-se de que o Python 3 está instalado em seu computador.
1. Clone este repositório.
2. No diretório raiz, instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode o jogo:
   ```bash
   python src/main.py
   ```

### Como Compilar o Executável (.exe)
Se desejar gerar o arquivo `.exe` para Windows:
```bash
pip install pyinstaller
pyinstaller Neon_Tetris.spec
```
O arquivo final ficará disponível na pasta `dist/`.

---

<br>

<a name="english-version"></a>
## 🇺🇸 English Version

**Neon Tetris Words** is a 2D neon-themed arcade game that combines classic Tetris mechanics with a word-building challenge. Survive the falling pieces, clear lines, and form valid words in Portuguese to earn extra points and stack combos!

### Key Features
* **Classic + Words**: Clearing lines gives points, but forming words grants bonus points and combo multipliers!
* **Dynamic Difficulties**: Play on Easy, Normal, or Hard.
* **Boss Battle**: In Phase 4, you must survive against corrupted pieces and continuous hazard attacks.
* **Hardcore Mode**: Ordinary line clears yield zero points. You must form words to score!
* **Neon Aesthetic**: Bright graphics, animated background GIFs, and immersive music.

### Controls
| Key | Action |
|---|---|
| `⬅️` / `➡️` | Move piece left / right |
| `⬇️` | Soft drop (accelerate fall) |
| `SPACE` | Rotate piece |
| `ENTER` | Hard Drop (instant fall) |
| `H` | Toggle Hardcore mode |
| `ESC` | Back to menus (Tutorial screen) |

### How to Run from Source
Ensure you have Python 3 installed.
1. Clone this repository.
2. In the root directory, install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python src/main.py
   ```

### How to Build Executable
If you wish to create the `.exe` file again (for Windows):
```bash
pip install pyinstaller
pyinstaller Neon_Tetris.spec
```
The resulting executable will be available in the `dist/` folder.
