import pygame
import sys
import random
import math
from settings import Settings
from player import Player
from enemy import Enemy
from menu import Menu
from assets_manager import AssetsManager
from customization import CustomizationScreen

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption("Wizard Quest")
        
        self.clock = pygame.time.Clock()
        self.assets = AssetsManager()
        self.menu = Menu(self)
        self.customization = CustomizationScreen(self.settings, self.assets)
        self.player = None
        self.game_active = False
        
        # Load and play background music
        if self.assets.get_music('background'):
            pygame.mixer.music.load(self.assets.get_music('background'))
            pygame.mixer.music.set_volume(self.settings.music_volume)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            
        # Background elements
        self.stars = []
        self.create_stars()
        
        # Platform elements
        self.platforms = []
        self.create_platforms()
        
        # Enemy elements
        self.enemies = []

    def create_stars(self):
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, self.settings.window_width),
                'y': random.randint(0, self.settings.window_height),
                'size': random.uniform(0.5, 3),
                'speed': random.uniform(0.05, 0.2)
            })
    
    def create_platforms(self):
        # Ground platform - full width at bottom
        self.platforms.append({
            'rect': pygame.Rect(0, self.settings.window_height - 50, self.settings.window_width, 50),
            'color': self.assets.get_color('wood_dark'),
            'texture': 'wood'
        })
        
        # Platform arrangement for better gameplay
        # Left side platform
        self.platforms.append({
            'rect': pygame.Rect(100, 420, 250, 25),
            'color': self.assets.get_color('wood_dark'),
            'texture': 'wood'
        })
        
        # Right side platform
        self.platforms.append({
            'rect': pygame.Rect(450, 420, 250, 25),
            'color': self.assets.get_color('wood_dark'),
            'texture': 'wood'
        })
        
        # Middle platform higher up
        self.platforms.append({
            'rect': pygame.Rect(300, 300, 200, 25),
            'color': self.assets.get_color('wood_dark'),
            'texture': 'wood'
        })
        
        # Two platforms at the top level
        self.platforms.append({
            'rect': pygame.Rect(150, 200, 150, 25),
            'color': self.assets.get_color('wood_dark'),
            'texture': 'wood'
        })
        
        self.platforms.append({
            'rect': pygame.Rect(500, 200, 150, 25),
            'color': self.assets.get_color('wood_dark'),
            'texture': 'wood'
        })
    
    def create_enemies(self):
        # Add enemies at strategic positions
        # Enemy on left platform
        self.enemies.append(Enemy(
            200, 380, self.assets, 
            patrol_min=120, patrol_max=330, 
            speed=1, direction=1
        ))
        
        # Enemy on right platform
        self.enemies.append(Enemy(
            550, 380, self.assets, 
            patrol_min=470, patrol_max=680, 
            speed=1, direction=-1
        ))
        
        # Enemy on middle platform
        self.enemies.append(Enemy(
            350, 260, self.assets, 
            patrol_min=310, patrol_max=490, 
            speed=1.5, direction=1
        ))

    def run(self):
        while True:
            if not self.game_active:
                if self.menu.run():
                    # If start game is clicked, show customization screen
                    if self.customization.run():
                        self.start_game()
            else:
                self._run_game()
            
            self.clock.tick(60)

    def _run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_active = False
                elif event.key == self.settings.spell_hotkey:
                    self.player.cast_spell()
                elif event.key == pygame.K_1:  # 1 key for directed attack
                    self.player.cast_attack(self.enemies)
                elif event.key == pygame.K_p:  # P for pause/settings
                    self.settings.show_settings = True

        # Update stars
        for star in self.stars:
            star['x'] -= star['speed']
            if star['x'] < 0:
                star['x'] = self.settings.window_width
                star['y'] = random.randint(0, self.settings.window_height)
        
        # Update particles
        self.assets.update_particles()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Check for collision with player
            if (enemy.active and self.player.rect.colliderect(enemy.rect) and 
                not self.player.invulnerable):
                self.player.take_damage()
                # Check if player is dead
                if self.player.health <= 0:
                    self.game_active = False
                    return
        
        # Update player
        self.player.update(self.platforms)

        # Draw
        self.draw_game()
        pygame.display.flip()

    def draw_game(self):
        # Draw background
        background = self.assets.get_image('background')
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.assets.get_color('background'))
            
            # Draw stars
            for star in self.stars:
                brightness = 100 + int(155 * star['size'] / 3)
                color = (brightness, brightness, brightness)
                pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), int(star['size']))
        
        # Draw platforms
        for platform in self.platforms:
            pygame.draw.rect(self.screen, platform['color'], platform['rect'])
            # Add wood texture
            if platform['texture'] == 'wood':
                for i in range(0, platform['rect'].width, 20):
                    pygame.draw.line(self.screen, self.assets.get_color('wood_accent'), 
                                  (platform['rect'].left + i, platform['rect'].top),
                                  (platform['rect'].left + i, platform['rect'].bottom), 2)
                
                # Add some detail
                for i in range(max(1, platform['rect'].width // 100)):
                    x = platform['rect'].left + random.randint(10, platform['rect'].width - 10)
                    y = platform['rect'].top + random.randint(2, platform['rect'].height - 2)
                    size = random.randint(2, 4)
                    pygame.draw.circle(self.screen, self.assets.get_color('wood_light'), (x, y), size)
        
        # Draw enemies
        for enemy in self.enemies:
            if enemy.active:
                enemy.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw particles
        self.assets.draw_particles(self.screen)
        
        # Draw player health
        self.draw_health()
    
    def draw_health(self):
        """Draw the player's health bar"""
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = 20
        
        # Background bar
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        
        # Health amount
        health_width = int(bar_width * self.player.health / self.player.max_health)
        if self.player.health > self.player.max_health / 2:
            health_color = (100, 200, 100)  # Green
        elif self.player.health > self.player.max_health / 4:
            health_color = (200, 200, 100)  # Yellow
        else:
            health_color = (200, 100, 100)  # Red
            
        pygame.draw.rect(self.screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Text
        health_text = f"Health: {self.player.health}/{self.player.max_health}"
        health_font = self.assets.get_font('text')
        text_surface = health_font.render(health_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (bar_x + 10, bar_y + bar_height // 2 - text_surface.get_height() // 2))

    def start_game(self):
        self.game_active = True
        self.player = Player(self)
        self.enemies = []
        self.create_enemies()

if __name__ == '__main__':
    game = Game()
    game.run() 