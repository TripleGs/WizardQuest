import json
import os
import pygame

class Settings:
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.music_volume = 0.5
        self.spell_hotkey = pygame.K_1
        self.show_settings = False
        
        # Default wizard customization
        self.wizard_customization = {
            'color': (180, 30, 30),  # Crimson
            'color_name': 'Crimson',
            'hat': 'pointed',
            'staff': 'wooden',
            'magic_color': (220, 180, 40),  # Gold
            'magic_power': 1.0
        }
        
        # Load settings if they exist
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.window_width = settings.get('window_width', self.window_width)
                self.window_height = settings.get('window_height', self.window_height)
                self.music_volume = settings.get('music_volume', self.music_volume)
                self.spell_hotkey = settings.get('spell_hotkey', self.spell_hotkey)
                
                # Load wizard customization if available
                if 'wizard_customization' in settings:
                    # Convert color tuples which JSON stores as lists
                    wizard_settings = settings['wizard_customization']
                    if 'color' in wizard_settings:
                        wizard_settings['color'] = tuple(wizard_settings['color'])
                    if 'magic_color' in wizard_settings:
                        wizard_settings['magic_color'] = tuple(wizard_settings['magic_color'])
                    
                    self.wizard_customization.update(wizard_settings)
    
    def save_settings(self):
        settings = {
            'window_width': self.window_width,
            'window_height': self.window_height,
            'music_volume': self.music_volume,
            'spell_hotkey': self.spell_hotkey,
            'wizard_customization': self.wizard_customization
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    
    def update_window_size(self, width, height):
        self.window_width = width
        self.window_height = height
        self.save_settings()
    
    def update_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        self.save_settings()
    
    def update_spell_hotkey(self, key):
        self.spell_hotkey = key
        self.save_settings() 