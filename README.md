# Wizard Quest

A 2D platformer game where you play as a customizable wizard who can cast spells and battle enemies.

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
   - 1: Cast attack spell (auto-targets nearest enemy)
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
   - Combat system with enemy AI
   - Auto-targeting attack spells that home in on enemies
   - Particle effects for spells, movement, and combat

## Combat System

- Press "1" to cast an attack spell that automatically targets the nearest enemy
- The attack will track and follow enemies as they move
- Enemies patrol platforms and will damage you on contact
- Successfully hitting an enemy with your attack will defeat them
- Close-range attacks have an immediate effect

## Game Structure

- `main.py`: Main game loop and initialization
- `player.py`: Player class with movement and spell casting
- `enemy.py`: Enemy behavior and combat logic
- `menu.py`: Menu system and settings interface
- `settings.py`: Game settings management
- `customization.py`: Character customization system
- `assets_manager.py`: Game assets and resources handling