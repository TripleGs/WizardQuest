import pygame
import os
import random
import math

class AssetsManager:
    def __init__(self):
        self.assets_dir = 'assets'
        self.images_dir = os.path.join(self.assets_dir, 'images')
        self.fonts_dir = os.path.join(self.assets_dir, 'fonts')
        self.music_dir = os.path.join(self.assets_dir, 'music')
        
        # Create directories if they don't exist
        for directory in [self.assets_dir, self.images_dir, self.fonts_dir, self.music_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Colors
        self.colors = {
            'wood_light': (210, 180, 140),
            'wood_dark': (139, 69, 19),
            'wood_accent': (160, 82, 45),
            'text_light': (255, 255, 255),
            'text_dark': (50, 50, 50),
            'magic_blue': (100, 149, 237),
            'magic_purple': (147, 112, 219),
            'magic_gold': (255, 215, 0),
            'background': (20, 12, 28),
            'background_light': (35, 25, 45),
            'stars': (255, 255, 220)
        }
        
        # Create placeholder images if they don't exist
        self.create_placeholder_images()
        
        # Initialize pygame font
        pygame.font.init()
        
        try:
            # Try to load the custom font
            self.fonts = {
                'title': pygame.font.Font(os.path.join(self.fonts_dir, 'MedievalSharp-Regular.ttf'), 64),
                'subtitle': pygame.font.Font(os.path.join(self.fonts_dir, 'MedievalSharp-Regular.ttf'), 48),
                'button': pygame.font.Font(os.path.join(self.fonts_dir, 'MedievalSharp-Regular.ttf'), 36),
                'text': pygame.font.Font(os.path.join(self.fonts_dir, 'MedievalSharp-Regular.ttf'), 24)
            }
        except:
            # Fallback to system font
            self.fonts = {
                'title': pygame.font.SysFont('serif', 64, bold=True),
                'subtitle': pygame.font.SysFont('serif', 48, bold=True),
                'button': pygame.font.SysFont('serif', 36),
                'text': pygame.font.SysFont('serif', 24)
            }
        
        # Load images
        self.images = {}
        self.load_images()
        
        # Load music
        self.music = {}
        self.load_music()
        
        # Create particles for visual effects
        self.particles = []
    
    def load_images(self):
        # Load actual images
        for filename in os.listdir(self.images_dir):
            if filename.endswith(('.png', '.jpg', '.bmp')):
                name = os.path.splitext(filename)[0]
                self.images[name] = pygame.image.load(os.path.join(self.images_dir, filename)).convert_alpha()
    
    def load_music(self):
        for filename in os.listdir(self.music_dir):
            if filename.endswith(('.mp3', '.wav')):
                name = os.path.splitext(filename)[0]
                self.music[name] = os.path.join(self.music_dir, filename)
    
    def create_placeholder_images(self):
        # Create wooden button background with texture
        button = pygame.Surface((200, 50))
        button.fill(self.colors['wood_dark'])
        # Add wood grain texture
        for i in range(10):
            x = random.randint(0, 200)
            width = random.randint(1, 3)
            pygame.draw.line(button, (130, 60, 10), (x, 0), (x, 50), width)
        pygame.draw.rect(button, self.colors['wood_light'], (2, 2, 196, 46))
        # Add more texture details
        for i in range(5):
            x = random.randint(5, 195)
            y = random.randint(5, 45)
            radius = random.randint(2, 5)
            pygame.draw.circle(button, (180, 150, 120), (x, y), radius)
        pygame.draw.rect(button, self.colors['wood_accent'], (2, 2, 196, 46), 2)
        pygame.image.save(button, os.path.join(self.images_dir, 'button_wood.png'))
        
        # Create wooden panel background with texture
        panel = pygame.Surface((400, 300))
        panel.fill(self.colors['wood_dark'])
        # Add wood grain texture
        for i in range(30):
            x = random.randint(0, 400)
            width = random.randint(1, 4)
            pygame.draw.line(panel, (130, 60, 10), (x, 0), (x, 300), width)
        pygame.draw.rect(panel, self.colors['wood_light'], (4, 4, 392, 292))
        # Add more texture details
        for i in range(20):
            x = random.randint(10, 390)
            y = random.randint(10, 290)
            radius = random.randint(3, 7)
            pygame.draw.circle(panel, (180, 150, 120), (x, y), radius)
        pygame.draw.rect(panel, self.colors['wood_accent'], (4, 4, 392, 292), 4)
        pygame.image.save(panel, os.path.join(self.images_dir, 'panel_wood.png'))
        
        # Create magic effect with glow
        magic = pygame.Surface((64, 64), pygame.SRCALPHA)
        for radius in range(30, 0, -1):
            alpha = min(255, radius * 8)
            color = list(self.colors['magic_blue'])
            color.append(alpha if radius > 15 else alpha // 2)
            pygame.draw.circle(magic, color, (32, 32), radius)
            
            if radius < 20:
                color = list(self.colors['magic_purple'])
                color.append(alpha)
                pygame.draw.circle(magic, color, (32, 32), radius // 2)
        pygame.image.save(magic, os.path.join(self.images_dir, 'magic_effect.png'))
        
        # Create starry background
        background = pygame.Surface((800, 600))
        background.fill(self.colors['background'])
        # Add gradient effect
        for y in range(600):
            alpha = min(255, y // 3)
            pygame.draw.line(background, (15, 10, 20), (0, y), (800, y))
        # Add stars
        for i in range(200):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            radius = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(background, (brightness, brightness, brightness), (x, y), radius)
        pygame.image.save(background, os.path.join(self.images_dir, 'background.png'))
        
        # Create wizard hat
        hat = pygame.Surface((80, 60), pygame.SRCALPHA)  # Smaller dimensions
        # Base hat
        pygame.draw.polygon(hat, self.colors['wood_dark'], [(40, 0), (0, 60), (80, 60)])
        # Add texture
        for i in range(8):
            pygame.draw.line(hat, (70, 40, 10), 
                          (40, i*7), 
                          (40 + i*5, 60), 
                          2)
        # Add band
        pygame.draw.rect(hat, self.colors['magic_gold'], (5, 45, 70, 8))
        # Add star
        pygame.draw.polygon(hat, self.colors['stars'], 
                         [(40, 25), (45, 35), (55, 35), (48, 43), 
                          (50, 55), (40, 49), (30, 55), (32, 43), 
                          (25, 35), (35, 35)])
        pygame.image.save(hat, os.path.join(self.images_dir, 'wizard_hat.png'))
        
        # Create wizard staff
        staff = pygame.Surface((30, 200), pygame.SRCALPHA)
        # Staff base
        pygame.draw.rect(staff, (120, 80, 40), (10, 30, 10, 170))
        # Add texture
        for i in range(5):
            pygame.draw.line(staff, (70, 40, 10), (10, 30 + i*30), (20, 30 + i*30), 2)
        # Staff crystal
        for radius in range(20, 0, -1):
            alpha = min(255, radius * 10)
            color = list(self.colors['magic_blue'])
            color.append(alpha if radius > 10 else alpha // 2)
            pygame.draw.circle(staff, color, (15, 15), radius)
        pygame.image.save(staff, os.path.join(self.images_dir, 'wizard_staff.png'))
    
    def get_font(self, name):
        return self.fonts.get(name, self.fonts['text'])
    
    def get_color(self, name):
        return self.colors.get(name, (255, 255, 255))
    
    def get_image(self, name):
        return self.images.get(name)
    
    def get_music(self, name):
        return self.music.get(name)
    
    def create_particles(self, x, y, color, count=10, speed=2, size=3, lifetime=30):
        # Ensure the color is a valid tuple with at least 3 elements (RGB)
        if not isinstance(color, tuple) or len(color) < 3:
            # Default to blue if invalid
            color = (100, 149, 237)
        else:
            # Make sure we only use RGB components
            color = color[:3]
        
        # Ensure size is an integer
        size = int(size)
        if size < 1:
            size = 1
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_val = random.uniform(0.5, speed)
            lifetime_val = random.randint(lifetime // 2, lifetime)
            size_val = random.randint(1, size)
            
            self.particles.append({
                'x': x,
                'y': y,
                'dx': speed_val * math.cos(angle),
                'dy': speed_val * math.sin(angle),
                'color': color,
                'size': size_val,
                'lifetime': lifetime_val,
                'max_lifetime': lifetime_val
            })
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, surface):
        for particle in self.particles:
            # Calculate transparency based on lifetime
            fade_ratio = particle['lifetime'] / particle['max_lifetime']
            
            # Get base color
            if 'color' in particle and isinstance(particle['color'], tuple) and len(particle['color']) >= 3:
                base_color = particle['color'][:3]  # Ensure only RGB components
            else:
                base_color = (255, 200, 100)  # Default gold if invalid color
            
            # Fade color to white as the particle ages
            if fade_ratio > 0.7:
                color = base_color  # Original color
            elif fade_ratio > 0.4:
                # Blend toward white
                color = (
                    int(base_color[0] * 0.7 + 255 * 0.3),
                    int(base_color[1] * 0.7 + 255 * 0.3),
                    int(base_color[2] * 0.7 + 255 * 0.3)
                )
            else:
                # Fade more toward white
                color = (
                    int(base_color[0] * 0.3 + 255 * 0.7),
                    int(base_color[1] * 0.3 + 255 * 0.7),
                    int(base_color[2] * 0.3 + 255 * 0.7)
                )
            
            # Draw the particle
            pygame.draw.circle(
                surface, 
                color, 
                (int(particle['x']), int(particle['y'])), 
                max(1, int(particle['size'] * fade_ratio))
            ) 