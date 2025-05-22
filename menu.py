import pygame
import random
import math

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.assets = game.assets
        
        # Menu states
        self.main_menu = True
        self.settings_menu = False
        
        # Button dimensions
        self.button_width = 200
        self.button_height = 50
        self.button_margin = 20
        
        # Animation elements
        self.particles = []
        self.frame = 0
        self.stars = []
        self.create_stars()
        
        # Create buttons
        self.create_buttons()
    
    def create_stars(self):
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, self.settings.window_width),
                'y': random.randint(0, self.settings.window_height),
                'size': random.uniform(0.5, 3),
                'pulse_speed': random.uniform(0.02, 0.1),
                'pulse': random.uniform(0, 3.14)
            })
    
    def create_buttons(self):
        # Main menu buttons
        self.start_button = pygame.Rect(
            self.settings.window_width//2 - self.button_width//2,
            self.settings.window_height//2 - self.button_height,
            self.button_width,
            self.button_height
        )
        
        self.settings_button = pygame.Rect(
            self.settings.window_width//2 - self.button_width//2,
            self.settings.window_height//2 + self.button_margin,
            self.button_width,
            self.button_height
        )
        
        # Settings menu buttons
        self.volume_slider = pygame.Rect(
            self.settings.window_width//2 - self.button_width//2,
            self.settings.window_height//2 - self.button_height,
            self.button_width,
            10
        )
        
        self.window_size_button = pygame.Rect(
            self.settings.window_width//2 - self.button_width//2,
            self.settings.window_height//2 + self.button_margin//2,
            self.button_width,
            self.button_height
        )
        
        self.back_button = pygame.Rect(
            self.settings.window_width//2 - self.button_width//2,
            self.settings.window_height//2 + self.button_margin * 3,
            self.button_width,
            self.button_height
        )
    
    def run(self):
        while True:
            self.frame += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.main_menu:
                        if self.start_button.collidepoint(mouse_pos):
                            # Create particles at button click
                            self.create_button_particles(self.start_button.centerx, self.start_button.centery)
                            return True
                        elif self.settings_button.collidepoint(mouse_pos):
                            self.main_menu = False
                            self.settings_menu = True
                            # Create particles at button click
                            self.create_button_particles(self.settings_button.centerx, self.settings_button.centery)
                    
                    elif self.settings_menu:
                        if self.volume_slider.collidepoint(mouse_pos):
                            # Update volume based on mouse x position
                            volume = (mouse_pos[0] - self.volume_slider.x) / self.volume_slider.width
                            self.settings.update_music_volume(volume)
                            # Create particles at slider
                            self.create_button_particles(mouse_pos[0], self.volume_slider.centery)
                        elif self.window_size_button.collidepoint(mouse_pos):
                            # Toggle between 800x600 and 1024x768
                            if self.settings.window_width == 800:
                                self.settings.update_window_size(1024, 768)
                            else:
                                self.settings.update_window_size(800, 600)
                            self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
                            self.create_buttons()
                            self.create_stars()
                            # Create particles at button click
                            self.create_button_particles(self.window_size_button.centerx, self.window_size_button.centery)
                        elif self.back_button.collidepoint(mouse_pos):
                            self.main_menu = True
                            self.settings_menu = False
                            # Create particles at button click
                            self.create_button_particles(self.back_button.centerx, self.back_button.centery)
            
            # Update animations
            self.update_animations()
            
            # Draw
            self.draw_background()
            
            if self.main_menu:
                self.draw_main_menu()
            else:
                self.draw_settings_menu()
            
            # Draw particles
            self.draw_particles()
            
            pygame.display.flip()
    
    def create_button_particles(self, x, y):
        # Get gold color for particles
        gold_color = self.assets.get_color('magic_gold')
        # Ensure it's a tuple
        if not isinstance(gold_color, tuple):
            gold_color = (255, 215, 0)  # Default gold
        
        for _ in range(20):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(0.5, 3)
            size = random.uniform(1, 3)
            lifetime = random.randint(20, 40)
            
            self.particles.append({
                'x': x,
                'y': y,
                'dx': speed * math.cos(angle),
                'dy': speed * math.sin(angle),
                'size': size,
                'color': gold_color,
                'lifetime': lifetime
            })
    
    def update_animations(self):
        # Update stars
        for star in self.stars:
            star['pulse'] += star['pulse_speed']
            if star['pulse'] > 6.28:
                star['pulse'] = 0
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw_background(self):
        # Draw background image if available
        background = self.assets.get_image('background')
        if background:
            self.screen.blit(background, (0, 0))
        else:
            # Fallback to gradient background
            self.screen.fill(self.assets.get_color('background'))
            
            # Draw animated stars
            for star in self.stars:
                size = star['size'] * (0.7 + 0.3 * math.sin(star['pulse']))
                brightness = 150 + int(105 * math.sin(star['pulse']))
                color = (brightness, brightness, brightness)
                pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), size)
    
    def draw_particles(self):
        for particle in self.particles:
            # Calculate transparency based on lifetime
            fade_ratio = particle['lifetime'] / 40
            
            # Just use fixed colors based on fade_ratio
            if fade_ratio > 0.7:
                color = (255, 255, 200)  # Bright white-yellow
            elif fade_ratio > 0.4:
                color = (200, 200, 100)  # Medium yellow
            else:
                color = (150, 100, 50)   # Dark orange-brown
            
            # Draw with fixed color
            pygame.draw.circle(
                self.screen, 
                color, 
                (int(particle['x']), int(particle['y'])), 
                max(1, int(particle['size'] * fade_ratio))
            )
    
    def draw_main_menu(self):
        # Draw title with magical effect
        title_y = self.settings.window_height//4
        title_offset = math.sin(self.frame * 0.05) * 5
        
        # Glowing outline
        for offset in range(3, 0, -1):
            title_shadow = self.assets.get_font('title').render("Wizard Quest", True, self.assets.get_color('magic_purple'))
            shadow_rect = title_shadow.get_rect(center=(self.settings.window_width//2 + offset, title_y + offset + title_offset))
            alpha = 100 - offset * 30
            title_shadow.set_alpha(alpha)
            self.screen.blit(title_shadow, shadow_rect)
        
        # Main title
        title = self.assets.get_font('title').render("Wizard Quest", True, self.assets.get_color('magic_blue'))
        title_rect = title.get_rect(center=(self.settings.window_width//2, title_y + title_offset))
        self.screen.blit(title, title_rect)
        
        # Draw decorative elements
        staff_img = self.assets.get_image('wizard_staff')
        if staff_img:
            staff_rotation = math.sin(self.frame * 0.02) * 10
            rotated_staff = pygame.transform.rotate(staff_img, staff_rotation)
            self.screen.blit(rotated_staff, (self.settings.window_width//4 - rotated_staff.get_width()//2, title_y))
            self.screen.blit(pygame.transform.flip(rotated_staff, True, False), 
                          (3*self.settings.window_width//4 - rotated_staff.get_width()//2, title_y))
        
        # Draw buttons with wooden texture
        button_image = self.assets.get_image('button_wood')
        hover = pygame.mouse.get_pos()
        
        # Start button
        if self.start_button.collidepoint(hover):
            # Highlight effect
            pygame.draw.rect(self.screen, self.assets.get_color('magic_gold'), 
                          pygame.Rect(self.start_button.left-5, self.start_button.top-5, 
                                   self.start_button.width+10, self.start_button.height+10), 3)
            
            # Create occasional sparkle particles
            if random.random() < 0.1:
                self.create_button_particles(random.randint(self.start_button.left, self.start_button.right),
                                          random.randint(self.start_button.top, self.start_button.bottom))
        
        if button_image:
            self.screen.blit(button_image, self.start_button)
        else:
            pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), self.start_button)
            pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), self.start_button, 2)
        
        start_text = self.assets.get_font('button').render("Start Game", True, self.assets.get_color('text_light'))
        self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width()//2,
                                    self.start_button.centery - start_text.get_height()//2))
        
        # Settings button
        if self.settings_button.collidepoint(hover):
            # Highlight effect
            pygame.draw.rect(self.screen, self.assets.get_color('magic_gold'), 
                          pygame.Rect(self.settings_button.left-5, self.settings_button.top-5, 
                                   self.settings_button.width+10, self.settings_button.height+10), 3)
            
            if random.random() < 0.1:
                self.create_button_particles(random.randint(self.settings_button.left, self.settings_button.right),
                                          random.randint(self.settings_button.top, self.settings_button.bottom))
        
        if button_image:
            self.screen.blit(button_image, self.settings_button)
        else:
            pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), self.settings_button)
            pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), self.settings_button, 2)
        
        settings_text = self.assets.get_font('button').render("Settings", True, self.assets.get_color('text_light'))
        self.screen.blit(settings_text, (self.settings_button.centerx - settings_text.get_width()//2,
                                       self.settings_button.centery - settings_text.get_height()//2))
    
    def draw_settings_menu(self):
        # Draw title
        title = self.assets.get_font('title').render("Settings", True, self.assets.get_color('text_light'))
        title_rect = title.get_rect(center=(self.settings.window_width//2, self.settings.window_height//4))
        self.screen.blit(title, title_rect)
        
        # Draw wooden panel background
        panel_image = self.assets.get_image('panel_wood')
        panel_rect = pygame.Rect(
            self.settings.window_width//2 - 200,
            self.settings.window_height//2 - 150,
            400,
            300
        )
        
        if panel_image:
            self.screen.blit(panel_image, panel_rect)
        else:
            pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), panel_rect)
            pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), panel_rect, 4)
        
        # Draw volume slider with visual indicator
        pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), self.volume_slider)
        pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), self.volume_slider, 2)
        
        # Draw volume indicator
        volume_pos = self.volume_slider.x + int(self.volume_slider.width * self.settings.music_volume)
        volume_indicator = pygame.Rect(volume_pos - 5, self.volume_slider.y - 5, 10, 20)
        pygame.draw.rect(self.screen, self.assets.get_color('magic_gold'), volume_indicator)
        
        volume_text = self.assets.get_font('button').render(f"Music Volume: {int(self.settings.music_volume * 100)}%", True, self.assets.get_color('text_light'))
        self.screen.blit(volume_text, (self.volume_slider.x, self.volume_slider.y - 30))
        
        # Draw buttons with hover effects
        hover = pygame.mouse.get_pos()
        button_image = self.assets.get_image('button_wood')
        
        # Window size button
        if self.window_size_button.collidepoint(hover):
            pygame.draw.rect(self.screen, self.assets.get_color('magic_gold'), 
                          pygame.Rect(self.window_size_button.left-5, self.window_size_button.top-5, 
                                   self.window_size_button.width+10, self.window_size_button.height+10), 3)
        
        if button_image:
            self.screen.blit(button_image, self.window_size_button)
        else:
            pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), self.window_size_button)
            pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), self.window_size_button, 2)
        
        size_text = self.assets.get_font('button').render(f"Window Size: {self.settings.window_width}x{self.settings.window_height}", True, self.assets.get_color('text_light'))
        self.screen.blit(size_text, (self.window_size_button.centerx - size_text.get_width()//2,
                                   self.window_size_button.centery - size_text.get_height()//2))
        
        # Back button
        if self.back_button.collidepoint(hover):
            pygame.draw.rect(self.screen, self.assets.get_color('magic_gold'), 
                          pygame.Rect(self.back_button.left-5, self.back_button.top-5, 
                                   self.back_button.width+10, self.back_button.height+10), 3)
        
        if button_image:
            self.screen.blit(button_image, self.back_button)
        else:
            pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), self.back_button)
            pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), self.back_button, 2)
        
        back_text = self.assets.get_font('button').render("Back", True, self.assets.get_color('text_light'))
        self.screen.blit(back_text, (self.back_button.centerx - back_text.get_width()//2,
                                   self.back_button.centery - back_text.get_height()//2)) 