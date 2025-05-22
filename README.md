# Wizard Quest

A 2D platformer game where you play as a customizable wizard who can cast spells.

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```
   python main.py
   ```

2. Controls:
   - Left/Right Arrow Keys: Move
   - Space: Jump
   - Assigned Key: Cast spell (default is 1)
   - SPACE: Jump
   - ESC: Return to menu
   - P: Open settings during gameplay

3. Features:
   - Customizable wizard character with different robe colors and magic effects
   - Start menu with game options
   - Settings menu to adjust:
     - Music volume
     - Window size
   - In-game settings to change spell hotkey
   - Advanced platformer mechanics with smooth movement
   - Particle effects for spells and movement

## Spell Casting

- Press the assigned spell key to cast a magical spell
- The spell will travel in the direction the wizard is facing
- Each spell creates beautiful particle effects

## Game Structure

- `main.py`: Main game loop and initialization
- `player.py`: Player class with movement and spell casting
- `menu.py`: Menu system and settings interface
- `settings.py`: Game settings management
- `customization.py`: Character customization system
- `assets_manager.py`: Game assets and resources handling