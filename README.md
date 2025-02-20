# Python Game Collection

English | [简体中文](README-cn.md)

A collection of classic arcade and puzzle games built with Pygame, featuring seven entertaining games: Breakout, Snake, Pacman, Tetris, Pong, Gomoku(Five in a Row) and 2048. The project implements smooth menu transitions, gamepad support, and modern UI design. Perfect for game development learning and entertainment.

## Quick Start

### System Requirements

- Python 3.8+
- Pygame 2.0+
- Other dependencies listed in requirements.txt

### Installation

1. Ensure Python 3.8 or higher is installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

```bash
# Run the game menu
python main.py
```

## Game List

1. **Breakout**
   - Classic brick-breaking game
   - Different colored bricks with varying point values
   - Angle-based ball bounce mechanics

2. **Snake**
   - Modern take on the classic snake game
   - Smooth controls and collision detection
   - Score tracking and progressive difficulty

3. **Pacman**
   - Simplified Pacman-style game
   - Multiple colored enemies
   - Collect dots for points

4. **Tetris**
   - Classic block-stacking puzzle game
   - Multiple block shapes
   - Line clearing mechanics

5. **Pong**
   - Two-player competitive pong game
   - Angle-based ball physics
   - First to 5 points wins

## Project Structure

```
.
├── main.py          # Main program entry
├── games/           # Game modules directory
│   ├── __init__.py
│   ├── breakout.py  # Breakout game
│   ├── snake.py     # Snake game
│   ├── pacman.py    # Pacman game
│   ├── tetris.py    # Tetris game
│   ├── pong.py      # Pong game
│   ├── gomoku.py    # Gomoku game
│   └── game2048.py  # 2048 game
├── requirements.txt  # Project dependencies
├── build.py         # Build script
└── resources/       # Resource files
    └── icon.ico     # Application icon
```

## Controls

### Keyboard Controls
- Arrow keys: Navigate menus and control games
- Enter: Select menu items
- ESC: Pause game/return to menu
- R: Restart game
- I: Show/hide instructions

### Gamepad Controls
- Left stick/D-pad: Navigate menus and control games
- A button: Select/confirm
- B button: Back/cancel
- Start button: Pause game
- X/Y buttons: Game-specific extra controls

### Game-Specific Controls

#### Breakout
- Left/Right arrows: Move paddle
- Gamepad: Use left stick or D-pad to move paddle

#### Snake
- Arrow keys: Change direction
- Gamepad: Use left stick or D-pad to move

#### Pacman
- Arrow keys: Move character
- Gamepad: Use left stick or D-pad to move

#### Tetris
- Left/Right: Move block
- Up: Rotate block
- Down: Speed up falling
- Space: Drop instantly
- Gamepad: Left stick/D-pad to move, A button to rotate

#### Pong
- Player 1: W/S keys
- Player 2: Up/Down arrows
- Gamepad 1: Left stick controls left paddle
- Gamepad 2: Left stick controls right paddle

#### Gomoku
- Mouse: Click to place stones
- Gamepad: Use left stick/D-pad to move cursor, A button to place stone

#### 2048
- Arrow keys: Slide tiles
- Gamepad: Use left stick/D-pad to move tiles

## Features

- Smooth menu transitions and scaling animations
- Complete gamepad support
- Tutorial system for each game
- Pause menu with save/quit options
- Progressive game difficulty
- Score tracking system
- Modern UI and visual feedback

## Screenshots

> Screenshots to be added

## Development Notes

The game collection uses a modular design where each game is implemented as an independent module with consistent interfaces, making it easy to add new games to the collection.

### Adding New Games

To add a new game, follow these steps:

1. Create a new Python file
2. Implement the Game class with required methods:
   - `__init__()`: Initialize game state
   - `run()`: Main game loop
   - `handle_input()`: Process user input
   - `update()`: Update game state
   - `draw()`: Render graphics
3. Add game information to `main.py`

## Recent Updates

- Added gamepad support for all games
- Implemented pause menu with "Continue" and "Return to Main Menu" options
- Added tutorial system
- Added Gomoku and 2048 games
- Improved UI with smooth transitions and visual feedback
- Added sound effects to enhance game experience

## Building for Distribution

This project uses PyInstaller for packaging into standalone executables.

### Build Steps

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run build command:
   ```bash
   # Windows
   pyinstaller build.py --onefile --noconsole --icon=icon.ico --name="GameCollection"
   ```

3. The executable will be generated in the `dist` directory

### Build Configuration

- `--onefile`: Package all dependencies into a single executable
- `--noconsole`: Hide console window when running
- `--icon`: Set application icon
- `--name`: Specify output executable name

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit Pull Requests.