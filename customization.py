import pygame
import random
import math
import sys

class CustomizationScreen:
    def __init__(self, settings, assets):
        self.settings = settings
        self.assets = assets
        self.screen = pygame.display.get_surface()
        self.running = True
        self.next_screen = None
        
        # Initialize animations
        self.frame = 0
        self.preview_bob = 0
        self.preview_scale = 1.0
        
        # Create star-like particles in the background
        self.stars = []
        for _ in range(50):
            self.stars.append({
                'x': random.randrange(0, self.settings.window_width),
                'y': random.randrange(0, self.settings.window_height),
                'size': random.uniform(0.5, 2.0),
                'pulse': random.uniform(0, 6.28)  # Random phase
            })
        
        # Initialize particle system
        self.particles = []
        
        # Initialize customization options
        self.wizard_colors = [
            (180, 30, 30),    # Crimson
            (30, 150, 70),    # Emerald
            (40, 80, 180),    # Sapphire
            (220, 160, 40),   # Amber
            (130, 60, 180),   # Violet
            (40, 160, 160),   # Teal
            (180, 140, 220),  # Lavender
            (200, 100, 100)   # Rose
        ]
        
        self.wizard_hats = [
            'pointed',
            'wide',
            'tall'
        ]
        
        self.wizard_staffs = [
            'wooden',
            'crystal', 
            'bone'
        ]
        
        # Default selections
        self.selected_color = 0
        self.selected_hat = 0
        self.selected_staff = 0
        
        # Create UI elements
        self.create_buttons()
    
    def create_stars(self):
        # Create background stars for the mystical sky
        for _ in range(50):
            self.stars.append({
                'x': random.randrange(0, self.settings.window_width),
                'y': random.randrange(0, self.settings.window_height),
                'size': random.uniform(0.5, 2.0),
                'pulse': random.uniform(0, 6.28)  # Random phase
            })
    
    def create_buttons(self):
        # Define panel dimensions
        panel_width = 600
        panel_height = 400
        
        # Define button dimensions
        button_width = 120
        button_height = 40
        navigation_button_width = 180
        navigation_button_height = 50
        arrow_button_width = 50
        arrow_button_height = 40
        margin = 20
        
        # Calculate panel position
        panel_x = self.settings.window_width//2 - panel_width//2
        panel_y = self.settings.window_height//2 - panel_height//2 + 50  # Move down a bit from center
        
        # Store panel rect for reference
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Navigation buttons (at bottom of screen)
        self.back_button = pygame.Rect(
            self.settings.window_width//2 - navigation_button_width - margin,
            self.settings.window_height - navigation_button_height - margin*2,
            navigation_button_width,
            navigation_button_height
        )
        
        self.start_button = pygame.Rect(
            self.settings.window_width//2 + margin,
            self.settings.window_height - navigation_button_height - margin*2,
            navigation_button_width,
            navigation_button_height
        )
        
        # Customization section positions
        color_section_x = panel_x + margin
        hat_section_x = panel_x + panel_width//3 + margin//2
        staff_section_x = panel_x + 2*panel_width//3 + margin//2
        options_y = panel_y + panel_height - button_height - margin
        
        # Arrow buttons for each customization option
        # Color selection
        self.color_left = pygame.Rect(
            color_section_x,
            options_y,
            arrow_button_width,
            arrow_button_height
        )
        
        self.color_right = pygame.Rect(
            color_section_x + arrow_button_width + margin,
            options_y,
            arrow_button_width,
            arrow_button_height
        )
        
        # Hat selection
        self.hat_left = pygame.Rect(
            hat_section_x,
            options_y,
            arrow_button_width,
            arrow_button_height
        )
        
        self.hat_right = pygame.Rect(
            hat_section_x + arrow_button_width + margin,
            options_y,
            arrow_button_width,
            arrow_button_height
        )
        
        # Staff selection
        self.staff_left = pygame.Rect(
            staff_section_x,
            options_y,
            arrow_button_width,
            arrow_button_height
        )
        
        self.staff_right = pygame.Rect(
            staff_section_x + arrow_button_width + margin,
            options_y,
            arrow_button_width,
            arrow_button_height
        )
    
    def run(self):
        self.running = True
        
        # Main loop
        while self.running:
            # Handle events
            self.check_events()
            
            # Update particles
            self.update_particles()
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            pygame.time.Clock().tick(60)
        
        # Return the next screen to navigate to (None or 'game')
        return self.next_screen
    
    def create_button_particles(self, x, y):
        # Get gold color for button particles
        gold_color = self.assets.get_color('magic_gold')
        # Ensure it's a tuple
        if not isinstance(gold_color, tuple):
            gold_color = (255, 215, 0)  # Default gold if invalid
        
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
    
    def create_magic_particles(self):
        """Create magic particles for wizard effects"""
        # Get random position near the wizard for the particle
        center_x = self.settings.window_width // 2
        center_y = self.settings.window_height - 250
        
        # Create particles around the wizard
        radius = random.randint(30, 80)
        angle = random.uniform(0, math.pi * 2)
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # Generate a gold/magical particle
        particle = {
            'x': x,
            'y': y,
            'vx': random.uniform(-0.5, 0.5),
            'vy': random.uniform(-1.5, -0.5),
            'radius': random.uniform(2, 4),
            'life': 60,
            'max_life': 60,
            'type': 'magic'
        }
        
        self.particles.append(particle)
    
    def update_particles(self):
        # Update all particles
        for particle in self.particles[:]:
            # Move particles
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Apply gravity/float effect to magic particles
            if particle.get('type') == 'magic':
                particle['vy'] -= 0.03  # Make particles float upward
            
            # Decrease lifetime
            particle['life'] -= 1
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def update_stars(self):
        for star in self.stars:
            star['pulse'] += star['pulse_speed']
            if star['pulse'] > 6.28:
                star['pulse'] = 0
    
    def draw(self):
        # Draw background
        background = self.assets.get_image('background')
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.assets.get_color('background'))
            
            # Draw stars
            for star in self.stars:
                size = star['size'] * (0.7 + 0.3 * math.sin(star['pulse']))
                brightness = 150 + int(105 * math.sin(star['pulse']))
                color = (brightness, brightness, brightness)
                pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), size)
        
        # Draw title with animated glow
        title_text = "Customize Your Wizard"
        title_y = 50
        title_offset = math.sin(self.frame * 0.05) * 3
        
        # Draw glow
        for offset in range(3, 0, -1):
            title_shadow = self.assets.get_font('title').render(title_text, True, self.assets.get_color('magic_purple'))
            shadow_rect = title_shadow.get_rect(center=(self.settings.window_width//2 + offset, title_y + offset + title_offset))
            alpha = 80 - offset * 20
            title_shadow.set_alpha(alpha)
            self.screen.blit(title_shadow, shadow_rect)
        
        # Main title
        title = self.assets.get_font('title').render(title_text, True, self.assets.get_color('magic_gold'))
        title_rect = title.get_rect(center=(self.settings.window_width//2, title_y + title_offset))
        self.screen.blit(title, title_rect)
        
        # Draw wooden panel for customization area
        panel_image = self.assets.get_image('panel_wood')
        if panel_image:
            # Scale panel image to fit customization area
            scaled_panel = pygame.transform.scale(panel_image, (self.panel_rect.width, self.panel_rect.height))
            self.screen.blit(scaled_panel, self.panel_rect)
        else:
            pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), self.panel_rect)
            pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), self.panel_rect, 4)
        
        # Draw section dividers
        section_width = self.panel_rect.width // 3
        for i in range(1, 3):
            x = self.panel_rect.left + section_width * i
            pygame.draw.line(
                self.screen, 
                self.assets.get_color('wood_accent'), 
                (x, self.panel_rect.top + 10),
                (x, self.panel_rect.bottom - 10),
                2
            )
        
        # Draw section headers
        section_headers = ["Robe Color", "Wizard Hat", "Magic Staff"]
        header_y = self.panel_rect.top + 30
        
        for i, header in enumerate(section_headers):
            x = self.panel_rect.left + section_width * i + section_width // 2
            # Draw header shadow
            header_shadow = self.assets.get_font('button').render(header, True, (50, 30, 10))
            shadow_rect = header_shadow.get_rect(center=(x + 2, header_y + 2))
            self.screen.blit(header_shadow, shadow_rect)
            
            # Draw header text
            header_text = self.assets.get_font('button').render(header, True, self.assets.get_color('text_light'))
            header_rect = header_text.get_rect(center=(x, header_y))
            self.screen.blit(header_text, header_rect)
        
        # Draw wizard preview
        self.draw_wizard_preview()
        
        # Draw customization options
        self.draw_customization_options()
        
        # Draw buttons
        self.draw_buttons()
        
        # Draw particles
        self.draw_particles()
    
    def draw_wizard_preview(self):
        # Calculate center position for the preview - centered in the panel
        preview_y = self.panel_rect.top + 120
        
        # Section width for each customization area
        section_width = self.panel_rect.width // 3
        
        # Draw each customization preview in its respective section
        
        # 1. Draw robe color preview (left section)
        color_x = self.panel_rect.left + section_width // 2
        self.draw_robe_preview(color_x, preview_y)
        
        # 2. Draw hat preview (middle section)
        hat_x = self.panel_rect.left + section_width + section_width // 2
        self.draw_hat_preview(hat_x, preview_y)
        
        # 3. Draw staff preview (right section)
        staff_x = self.panel_rect.left + 2 * section_width + section_width // 2
        self.draw_staff_preview(staff_x, preview_y)
        
        # Draw full wizard preview at bottom center of screen
        wizard_x = self.settings.window_width // 2
        wizard_y = self.settings.window_height - 250
        self.draw_full_wizard(wizard_x, wizard_y)

    def draw_robe_preview(self, x, y):
        # Apply animation to the preview
        y_offset = self.preview_bob
        
        # Draw color sample
        color_sample_width = 80
        color_sample_height = 120
        
        color_rect = pygame.Rect(
            x - color_sample_width // 2,
            y - color_sample_height // 2 + y_offset,
            color_sample_width,
            color_sample_height
        )
        
        # Draw robe shape
        pygame.draw.rect(self.screen, self.wizard_colors[self.selected_color], color_rect)
        
        # Add robe details
        pygame.draw.rect(self.screen, (0, 0, 0), color_rect, 2)
        
        # Add some robe decorations
        # Collar
        pygame.draw.rect(
            self.screen, 
            (min(255, self.wizard_colors[self.selected_color][0] + 30),
             min(255, self.wizard_colors[self.selected_color][1] + 30),
             min(255, self.wizard_colors[self.selected_color][2] + 30)), 
            (color_rect.left, color_rect.top, color_rect.width, 15)
        )
        
        # Belt
        pygame.draw.rect(
            self.screen, 
            (min(255, self.wizard_colors[self.selected_color][0] - 50),
             min(255, self.wizard_colors[self.selected_color][1] - 50),
             min(255, self.wizard_colors[self.selected_color][2] - 50)), 
            (color_rect.left, color_rect.top + color_rect.height // 2, color_rect.width, 10)
        )
        
        # Magic symbols
        symbol_positions = [
            (color_rect.centerx, color_rect.top + 40),
            (color_rect.left + 20, color_rect.centery + 20),
            (color_rect.right - 20, color_rect.centery + 20)
        ]
        
        for pos in symbol_positions:
            # Draw a small magic symbol
            pygame.draw.circle(self.screen, self.assets.get_color('magic_gold'), pos, 5)
            # Add a glow
            glow_size = 3 + math.sin(self.frame * 0.1) * 2
            pygame.draw.circle(self.screen, self.assets.get_color('magic_purple'), pos, glow_size, 1)
        
        # Label for current color
        color_names = ["Crimson", "Emerald", "Sapphire", "Amber", "Violet", "Teal", "Lavender", "Rose"]
        current_color = color_names[self.selected_color % len(color_names)]
        
        color_label = self.assets.get_font('text').render(current_color, True, self.assets.get_color('text_light'))
        self.screen.blit(color_label, (x - color_label.get_width() // 2, color_rect.bottom + 10))

    def draw_hat_preview(self, x, y):
        # Apply animation to the preview
        y_offset = self.preview_bob
        
        hat_image = self.assets.get_image('wizard_hat')
        if hat_image:
            # Scale hat image
            hat_width = 100
            hat_height = 80
            
            # Adjust based on hat type
            if self.wizard_hats[self.selected_hat] == 'tall':
                hat_height = 100
            elif self.wizard_hats[self.selected_hat] == 'wide':
                hat_width = 120
            
            scaled_hat = pygame.transform.scale(hat_image, (hat_width, hat_height))
            
            # Draw hat
            hat_x = x - scaled_hat.get_width() // 2
            hat_y = y - scaled_hat.get_height() // 2 + y_offset
            self.screen.blit(scaled_hat, (hat_x, hat_y))
        else:
            # Fallback to polygon hat
            hat_color = self.assets.get_color('wood_dark')
            
            if self.wizard_hats[self.selected_hat] == 'pointed':
                hat_points = [
                    (x, y - 40 + y_offset),
                    (x - 40, y + y_offset),
                    (x + 40, y + y_offset)
                ]
            elif self.wizard_hats[self.selected_hat] == 'wide':
                hat_points = [
                    (x, y - 30 + y_offset),
                    (x - 50, y + y_offset),
                    (x + 50, y + y_offset)
                ]
            else:  # tall
                hat_points = [
                    (x, y - 50 + y_offset),
                    (x - 30, y + y_offset),
                    (x + 30, y + y_offset)
                ]
            
            pygame.draw.polygon(self.screen, hat_color, hat_points)
            
            # Add hat band
            band_y = y - 5 + y_offset
            pygame.draw.line(self.screen, self.assets.get_color('magic_gold'), 
                          (hat_points[1][0], band_y), 
                          (hat_points[2][0], band_y), 
                          3)
        
        # Label for current hat
        hat_label = self.assets.get_font('text').render(
            self.wizard_hats[self.selected_hat].title(), 
            True, 
            self.assets.get_color('text_light')
        )
        self.screen.blit(hat_label, (x - hat_label.get_width() // 2, y + 60))

    def draw_staff_preview(self, x, y):
        # Apply animation to the preview
        y_offset = self.preview_bob
        
        staff_image = self.assets.get_image('wizard_staff')
        if staff_image:
            # Scale staff image
            staff_width = 30
            staff_height = 150
            
            scaled_staff = pygame.transform.scale(staff_image, (staff_width, staff_height))
            
            # Apply rotation for visual interest
            rotation = math.sin(self.frame * 0.03) * 5
            rotated_staff = pygame.transform.rotate(scaled_staff, rotation)
            
            # Draw staff
            staff_x = x - rotated_staff.get_width() // 2
            staff_y = y - rotated_staff.get_height() // 2 + y_offset
            self.screen.blit(rotated_staff, (staff_x, staff_y))
        else:
            # Fallback to rectangle staff
            staff_width = 15
            staff_height = 120
            
            staff_rect = pygame.Rect(
                x - staff_width // 2,
                y - staff_height // 2 + y_offset,
                staff_width,
                staff_height
            )
            
            # Draw staff based on type
            if self.wizard_staffs[self.selected_staff] == 'wooden':
                # Wooden staff
                pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), staff_rect)
                # Add grain
                for i in range(0, staff_height, 15):
                    line_y = staff_rect.top + i
                    pygame.draw.line(
                        self.screen, 
                        self.assets.get_color('wood_dark'), 
                        (staff_rect.left, line_y), 
                        (staff_rect.right, line_y), 
                        1
                    )
                    
            elif self.wizard_staffs[self.selected_staff] == 'crystal':
                # Crystal staff
                pygame.draw.rect(self.screen, (70, 70, 90), staff_rect)
                # Add crystal top
                crystal_rect = pygame.Rect(
                    x - 12,
                    staff_rect.top - 15,
                    24,
                    30
                )
                pygame.draw.rect(self.screen, self.assets.get_color('magic_blue'), crystal_rect)
                
                # Add glow
                glow_size = 5 + math.sin(self.frame * 0.1) * 2
                pygame.draw.circle(
                    self.screen, 
                    self.assets.get_color('magic_purple'), 
                    (x, staff_rect.top), 
                    glow_size
                )
                
            else:  # bone
                # Bone staff
                pygame.draw.rect(self.screen, (220, 220, 200), staff_rect)
                # Add bone details
                for i in range(0, staff_height, 20):
                    joint_y = staff_rect.top + i
                    pygame.draw.ellipse(
                        self.screen, 
                        (240, 240, 220), 
                        (staff_rect.left - 5, joint_y, staff_width + 10, 10)
                    )
        
        # Label for current staff
        staff_label = self.assets.get_font('text').render(
            self.wizard_staffs[self.selected_staff].title(), 
            True, 
            self.assets.get_color('text_light')
        )
        self.screen.blit(staff_label, (x - staff_label.get_width() // 2, y + 80))

    def draw_full_wizard(self, x, y):
        # Apply animation to the full preview
        y_offset = self.preview_bob * 1.5
        
        # Draw a magical circle under the wizard
        radius = 50 + math.sin(self.frame * 0.1) * 5
        for r in range(int(radius), int(radius - 10), -1):
            alpha = int(150 * (r - (radius - 10)) / 10)
            color = list(self.assets.get_color('magic_blue'))
            color.append(alpha)
            pygame.draw.circle(self.screen, color, (x, y + 75), r)
        
        # Draw wizard body with selected color
        wizard_width = 60
        wizard_height = 120
        
        # Apply scale effect
        wizard_width = int(wizard_width * self.preview_scale)
        wizard_height = int(wizard_height * self.preview_scale)
        
        wizard_rect = pygame.Rect(
            x - wizard_width // 2,
            y - wizard_height // 2 + y_offset,
            wizard_width,
            wizard_height
        )
        
        # Draw robe
        pygame.draw.rect(self.screen, self.wizard_colors[self.selected_color], wizard_rect)
        
        # Draw arms
        arm_width = 15
        arm_length = 50
        # Left arm
        pygame.draw.rect(
            self.screen,
            self.wizard_colors[self.selected_color], 
            (wizard_rect.left - arm_width, 
             wizard_rect.top + 20 + y_offset // 2, 
             arm_width, 
             arm_length)
        )
        # Right arm
        pygame.draw.rect(
            self.screen,
            self.wizard_colors[self.selected_color], 
            (wizard_rect.right, 
             wizard_rect.top + 20 + y_offset // 2, 
             arm_width, 
             arm_length)
        )
        
        # Add robe details
        pygame.draw.rect(self.screen, (0, 0, 0), wizard_rect, 2)
        # Collar
        pygame.draw.rect(
            self.screen, 
            (min(255, self.wizard_colors[self.selected_color][0] + 30),
             min(255, self.wizard_colors[self.selected_color][1] + 30),
             min(255, self.wizard_colors[self.selected_color][2] + 30)), 
            (wizard_rect.left, wizard_rect.top, wizard_rect.width, 15)
        )
        # Belt
        pygame.draw.rect(
            self.screen, 
            (min(255, self.wizard_colors[self.selected_color][0] - 50),
             min(255, self.wizard_colors[self.selected_color][1] - 50),
             min(255, self.wizard_colors[self.selected_color][2] - 50)), 
            (wizard_rect.left, wizard_rect.top + wizard_rect.height // 2, wizard_rect.width, 10)
        )
        
        # Magic symbols
        symbol_positions = [
            (wizard_rect.centerx, wizard_rect.top + 40),
            (wizard_rect.left + 15, wizard_rect.centery + 30),
            (wizard_rect.right - 15, wizard_rect.centery + 30)
        ]
        
        for pos in symbol_positions:
            # Draw a small magic symbol
            pygame.draw.circle(self.screen, self.assets.get_color('magic_gold'), pos, 4)
            # Add a glow
            glow_size = 2 + math.sin(self.frame * 0.1) * 1.5
            pygame.draw.circle(self.screen, self.assets.get_color('magic_purple'), pos, glow_size, 1)
        
        # Draw wizard's face
        face_y = wizard_rect.top + 7
        face_width = 20
        face_color = (240, 220, 190)  # Skin tone
        
        # Face
        pygame.draw.ellipse(
            self.screen,
            face_color,
            (x - face_width // 2, face_y, face_width, 25)
        )
        
        # Eyes
        eye_color = (30, 30, 60)
        eye_spacing = 8
        
        pygame.draw.circle(self.screen, eye_color, (x - eye_spacing // 2, face_y + 10), 2)
        pygame.draw.circle(self.screen, eye_color, (x + eye_spacing // 2, face_y + 10), 2)
        
        # Beard
        beard_color = (200, 200, 200)
        pygame.draw.polygon(
            self.screen,
            beard_color,
            [(x - 10, face_y + 18), (x, face_y + 35), (x + 10, face_y + 18)]
        )
        
        # Draw hat based on selection
        hat_y = wizard_rect.top - 25 + y_offset
        hat_image = self.assets.get_image('wizard_hat')
        if hat_image:
            # Scale hat based on animation and type
            hat_width = 100 * self.preview_scale
            hat_height = 80 * self.preview_scale
            
            # Adjust based on hat type
            if self.wizard_hats[self.selected_hat] == 'tall':
                hat_height = 100 * self.preview_scale
            elif self.wizard_hats[self.selected_hat] == 'wide':
                hat_width = 120 * self.preview_scale
            
            scaled_hat = pygame.transform.scale(hat_image, (int(hat_width), int(hat_height)))
            
            hat_x = x - scaled_hat.get_width() // 2
            self.screen.blit(scaled_hat, (hat_x, hat_y - scaled_hat.get_height() + 15))
        else:
            # Fallback to polygon hat
            hat_color = self.assets.get_color('wood_dark')
            
            if self.wizard_hats[self.selected_hat] == 'pointed':
                hat_points = [
                    (x, hat_y - 40),
                    (x - 40, hat_y),
                    (x + 40, hat_y)
                ]
            elif self.wizard_hats[self.selected_hat] == 'wide':
                hat_points = [
                    (x, hat_y - 30),
                    (x - 50, hat_y),
                    (x + 50, hat_y)
                ]
            else:  # tall
                hat_points = [
                    (x, hat_y - 50),
                    (x - 30, hat_y),
                    (x + 30, hat_y)
                ]
            
            pygame.draw.polygon(self.screen, hat_color, hat_points)
            
            # Add hat band
            band_y = hat_y - 5
            pygame.draw.line(self.screen, self.assets.get_color('magic_gold'), 
                          (hat_points[1][0], band_y), 
                          (hat_points[2][0], band_y), 
                          3)
        
        # Draw staff based on selection
        staff_image = self.assets.get_image('wizard_staff')
        if staff_image:
            # Scale staff based on animation
            staff_width = int(30 * self.preview_scale)
            staff_height = int(150 * self.preview_scale)
            scaled_staff = pygame.transform.scale(staff_image, (staff_width, staff_height))
            
            staff_x = wizard_rect.right + arm_width - 5
            staff_y = wizard_rect.top + 20 + y_offset // 2
            self.screen.blit(scaled_staff, (staff_x, staff_y))
            
            # Add staff glow effect
            if self.wizard_staffs[self.selected_staff] == 'crystal':
                glow_size = 10 + math.sin(self.frame * 0.1) * 3
                glow_pos = (staff_x + staff_width // 2, staff_y + 15)
                pygame.draw.circle(
                    self.screen, 
                    self.assets.get_color('magic_blue'), 
                    glow_pos, 
                    glow_size, 
                    3
                )
        else:
            # Fallback to rectangle staff
            staff_width = 15
            staff_height = 150
            
            staff_rect = pygame.Rect(
                wizard_rect.right + arm_width - 5,
                wizard_rect.top + 20 + y_offset // 2,
                staff_width,
                staff_height
            )
            
            # Draw staff based on type
            if self.wizard_staffs[self.selected_staff] == 'wooden':
                # Wooden staff
                pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), staff_rect)
                # Add grain
                for i in range(0, staff_height, 15):
                    line_y = staff_rect.top + i
                    pygame.draw.line(
                        self.screen, 
                        self.assets.get_color('wood_dark'), 
                        (staff_rect.left, line_y), 
                        (staff_rect.right, line_y), 
                        1
                    )
                    
            elif self.wizard_staffs[self.selected_staff] == 'crystal':
                # Crystal staff
                pygame.draw.rect(self.screen, (70, 70, 90), staff_rect)
                # Add crystal top
                crystal_rect = pygame.Rect(
                    staff_rect.left - 7,
                    staff_rect.top - 15,
                    staff_width + 14,
                    30
                )
                pygame.draw.rect(self.screen, self.assets.get_color('magic_blue'), crystal_rect)
                
                # Add glow
                glow_size = 10 + math.sin(self.frame * 0.1) * 3
                pygame.draw.circle(
                    self.screen, 
                    self.assets.get_color('magic_purple'), 
                    (staff_rect.left + staff_width // 2, staff_rect.top), 
                    glow_size, 
                    3
                )
                
            else:  # bone
                # Bone staff
                pygame.draw.rect(self.screen, (220, 220, 200), staff_rect)
                # Add bone details
                for i in range(0, staff_height, 20):
                    joint_y = staff_rect.top + i
                    pygame.draw.ellipse(
                        self.screen, 
                        (240, 240, 220), 
                        (staff_rect.left - 5, joint_y, staff_width + 10, 10)
                    )
        
        # Add occasional magic particles around the wizard
        if random.random() < 0.1:
            self.create_magic_particles()
    
    def draw_customization_options(self):
        # Draw color selection label with animated glow
        color_text = "Robe Color"
        color_x = self.settings.window_width//4
        color_y = self.settings.window_height//2 - 70
        
        # Add slight animation to the labels
        glow = math.sin(self.frame * 0.1) * 10 + 10
        
        color_shadow = self.assets.get_font('button').render(color_text, True, (int(glow), int(glow), int(glow)))
        color_shadow_rect = color_shadow.get_rect(center=(color_x + 2, color_y + 2))
        self.screen.blit(color_shadow, color_shadow_rect)
        
        color_label = self.assets.get_font('button').render(color_text, True, self.assets.get_color('text_light'))
        color_label_rect = color_label.get_rect(center=(color_x, color_y))
        self.screen.blit(color_label, color_label_rect)
        
        # Draw hat selection
        hat_text = f"Hat: {self.wizard_hats[self.selected_hat].title()}"
        hat_x = self.settings.window_width//2
        hat_y = self.settings.window_height//2 - 70
        
        hat_shadow = self.assets.get_font('button').render(hat_text, True, (int(glow), int(glow), int(glow)))
        hat_shadow_rect = hat_shadow.get_rect(center=(hat_x + 2, hat_y + 2))
        self.screen.blit(hat_shadow, hat_shadow_rect)
        
        hat_label = self.assets.get_font('button').render(hat_text, True, self.assets.get_color('text_light'))
        hat_label_rect = hat_label.get_rect(center=(hat_x, hat_y))
        self.screen.blit(hat_label, hat_label_rect)
        
        # Draw staff selection
        staff_text = f"Staff: {self.wizard_staffs[self.selected_staff].title()}"
        staff_x = 3 * self.settings.window_width//4
        staff_y = self.settings.window_height//2 - 70
        
        staff_shadow = self.assets.get_font('button').render(staff_text, True, (int(glow), int(glow), int(glow)))
        staff_shadow_rect = staff_shadow.get_rect(center=(staff_x + 2, staff_y + 2))
        self.screen.blit(staff_shadow, staff_shadow_rect)
        
        staff_label = self.assets.get_font('button').render(staff_text, True, self.assets.get_color('text_light'))
        staff_label_rect = staff_label.get_rect(center=(staff_x, staff_y))
        self.screen.blit(staff_label, staff_label_rect)
        
        # Draw current color preview
        color_preview = pygame.Rect(
            color_x - 15,
            color_y + 20,
            30,
            30
        )
        pygame.draw.rect(self.screen, self.wizard_colors[self.selected_color], color_preview)
        pygame.draw.rect(self.screen, self.assets.get_color('text_light'), color_preview, 2)
    
    def draw_buttons(self):
        # Draw navigation buttons
        button_color = self.assets.get_color('button_dark')
        hover_color = self.assets.get_color('button_hover')
        
        # Back button
        if self.back_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, hover_color, self.back_button, border_radius=5)
        else:
            pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=5)
        pygame.draw.rect(self.screen, self.assets.get_color('button_border'), self.back_button, 2, border_radius=5)
        
        back_text = self.assets.get_font('button').render("Back", True, self.assets.get_color('text_light'))
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Start button
        if self.start_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, hover_color, self.start_button, border_radius=5)
        else:
            pygame.draw.rect(self.screen, button_color, self.start_button, border_radius=5)
        pygame.draw.rect(self.screen, self.assets.get_color('button_border'), self.start_button, 2, border_radius=5)
        
        start_text = self.assets.get_font('button').render("Start Game", True, self.assets.get_color('text_light'))
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)
        
        # Draw customization buttons (arrows)
        self.draw_customization_buttons()

    def draw_customization_buttons(self):
        # Get button colors
        button_color = self.assets.get_color('button_dark')
        hover_color = self.assets.get_color('button_hover')
        text_color = self.assets.get_color('text_light')
        
        # Button pairs for each customization option
        button_pairs = [
            (self.color_left, self.color_right, "Robe Color"),
            (self.hat_left, self.hat_right, "Hat Style"),
            (self.staff_left, self.staff_right, "Staff Type")
        ]
        
        # Mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()
        
        for left_btn, right_btn, label in button_pairs:
            # Left button (previous)
            if left_btn.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, hover_color, left_btn, border_radius=5)
            else:
                pygame.draw.rect(self.screen, button_color, left_btn, border_radius=5)
            pygame.draw.rect(self.screen, self.assets.get_color('button_border'), left_btn, 2, border_radius=5)
            
            # Draw left arrow
            left_arrow_points = [
                (left_btn.centerx + 8, left_btn.top + 10),
                (left_btn.centerx - 8, left_btn.centery),
                (left_btn.centerx + 8, left_btn.bottom - 10)
            ]
            pygame.draw.polygon(self.screen, text_color, left_arrow_points)
            
            # Right button (next)
            if right_btn.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, hover_color, right_btn, border_radius=5)
            else:
                pygame.draw.rect(self.screen, button_color, right_btn, border_radius=5)
            pygame.draw.rect(self.screen, self.assets.get_color('button_border'), right_btn, 2, border_radius=5)
            
            # Draw right arrow
            right_arrow_points = [
                (right_btn.centerx - 8, right_btn.top + 10),
                (right_btn.centerx + 8, right_btn.centery),
                (right_btn.centerx - 8, right_btn.bottom - 10)
            ]
            pygame.draw.polygon(self.screen, text_color, right_arrow_points)

    def draw_particles(self):
        # Draw all particles
        for particle in self.particles:
            # Get particle properties
            x, y = particle['x'], particle['y']
            
            if particle.get('type') == 'magic':
                # For magic particles, fade from gold to purple as they age
                life_ratio = particle['life'] / particle['max_life']
                
                if life_ratio > 0.7:  # New particles: gold
                    color = self.assets.get_color('magic_gold')
                elif life_ratio > 0.4:  # Middle-aged particles: orange
                    color = (230, 120, 60)
                else:  # Old particles: purple/fading
                    color = self.assets.get_color('magic_purple')
                    
                # Size fades out
                radius = particle['radius'] * life_ratio
                
                # Draw the particle
                pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)
                
                # Add a glow for magical effect
                if life_ratio > 0.3:
                    glow_radius = radius * 1.5
                    pygame.draw.circle(self.screen, color, (int(x), int(y)), glow_radius, 1)

    def get_customization(self):
        return {
            'color': self.wizard_colors[self.selected_color],
            'hat': self.wizard_hats[self.selected_hat],
            'staff': self.wizard_staffs[self.selected_staff]
        }

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            
        # Update animations
        self.frame += 1
        self.preview_bob = math.sin(self.frame * 0.05) * 3
        self.preview_scale = 1.0 + math.sin(self.frame * 0.03) * 0.05

    def handle_click(self, pos):
        # Handle navigation buttons
        if self.back_button.collidepoint(pos):
            self.running = False
            return
        
        if self.start_button.collidepoint(pos):
            self.save_customization()
            self.running = False
            self.next_screen = 'game'
            return
        
        # Handle customization buttons
        # Color buttons
        if self.color_left.collidepoint(pos):
            self.selected_color = (self.selected_color - 1) % len(self.wizard_colors)
            self.create_color_change_particles()
        elif self.color_right.collidepoint(pos):
            self.selected_color = (self.selected_color + 1) % len(self.wizard_colors)
            self.create_color_change_particles()
        
        # Hat buttons
        elif self.hat_left.collidepoint(pos):
            self.selected_hat = (self.selected_hat - 1) % len(self.wizard_hats)
            self.create_hat_change_particles()
        elif self.hat_right.collidepoint(pos):
            self.selected_hat = (self.selected_hat + 1) % len(self.wizard_hats)
            self.create_hat_change_particles()
        
        # Staff buttons
        elif self.staff_left.collidepoint(pos):
            self.selected_staff = (self.selected_staff - 1) % len(self.wizard_staffs)
            self.create_staff_change_particles()
        elif self.staff_right.collidepoint(pos):
            self.selected_staff = (self.selected_staff + 1) % len(self.wizard_staffs)
            self.create_staff_change_particles()

    def create_color_change_particles(self):
        """Create particles when changing robe color"""
        center_x = self.settings.window_width // 2
        center_y = self.settings.window_height - 250
        
        # Position around the wizard's body
        for _ in range(10):
            x = center_x + random.uniform(-30, 30)
            y = center_y + random.uniform(-50, 50)
            
            # Use the selected color for particles
            color = self.wizard_colors[self.selected_color]
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, 0),
                'radius': random.uniform(2, 4),
                'life': random.randint(30, 60),
                'max_life': 60,
                'type': 'magic',
                'color': color
            })

    def create_hat_change_particles(self):
        """Create particles when changing hat style"""
        center_x = self.settings.window_width // 2
        center_y = self.settings.window_height - 250
        
        # Position around the wizard's hat
        for _ in range(10):
            x = center_x + random.uniform(-30, 30)
            y = center_y - 80 + random.uniform(-20, 20)
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, 0),
                'radius': random.uniform(2, 4),
                'life': random.randint(30, 60),
                'max_life': 60,
                'type': 'magic'
            })

    def create_staff_change_particles(self):
        """Create particles when changing staff type"""
        center_x = self.settings.window_width // 2
        center_y = self.settings.window_height - 250
        
        # Position around the wizard's staff
        for _ in range(10):
            x = center_x + 50 + random.uniform(-10, 10)
            y = center_y - 20 + random.uniform(-40, 40)
            
            # Add special colors for crystal staff
            if self.wizard_staffs[self.selected_staff] == 'crystal':
                color = self.assets.get_color('magic_blue')
            else:
                color = self.assets.get_color('magic_gold')
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, 0),
                'radius': random.uniform(2, 4),
                'life': random.randint(30, 60),
                'max_life': 60,
                'type': 'magic'
            })

    def save_customization(self):
        """Save the selected customization options"""
        # Get color name for display
        color_names = ["Crimson", "Emerald", "Sapphire", "Amber", "Violet", "Teal", "Lavender", "Rose"]
        selected_color_name = color_names[self.selected_color % len(color_names)]
        
        # Create wizard customization data structure
        wizard_data = {
            'color': self.wizard_colors[self.selected_color],
            'color_name': selected_color_name,
            'hat': self.wizard_hats[self.selected_hat],
            'staff': self.wizard_staffs[self.selected_staff]
        }
        
        # Add magic effects based on staff type
        if self.wizard_staffs[self.selected_staff] == 'crystal':
            wizard_data['magic_color'] = self.assets.get_color('magic_blue')
            wizard_data['magic_power'] = 1.5  # Crystal staff has more power
        elif self.wizard_staffs[self.selected_staff] == 'wooden':
            wizard_data['magic_color'] = self.assets.get_color('magic_gold')
            wizard_data['magic_power'] = 1.0  # Standard power
        else:  # Bone staff
            wizard_data['magic_color'] = self.assets.get_color('magic_purple')
            wizard_data['magic_power'] = 1.2  # Bone staff has special power
        
        # Save to the settings
        self.settings.wizard_customization = wizard_data
        print(f"Wizard customized with {selected_color_name} robes, {self.wizard_hats[self.selected_hat]} hat, and {self.wizard_staffs[self.selected_staff]} staff!") 