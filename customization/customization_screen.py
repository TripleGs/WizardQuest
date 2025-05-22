import pygame
import sys
import random
import math

from .wizard_renderer import WizardRenderer
from .particles import ParticleSystem
from .ui import CustomizationUI

class CustomizationScreen:
    def __init__(self, settings, assets):
        self.settings = settings
        self.assets = assets
        self.screen = pygame.display.get_surface()
        self.running = True
        self.next_screen = None
        
        # Initialize components
        self.ui = CustomizationUI(settings, assets)
        self.wizard_renderer = WizardRenderer(settings, assets)
        self.particles = ParticleSystem(assets)
        
        # Track selected color
        self.selected_color = 0
        
        # Create background stars
        self.stars = []
        self.create_stars()
    
    def create_stars(self):
        """Create background stars for a mystical atmosphere"""
        for _ in range(50):
            self.stars.append({
                'x': random.randrange(0, self.settings.window_width),
                'y': random.randrange(0, self.settings.window_height),
                'size': random.uniform(0.5, 2.0),
                'pulse': random.uniform(0, 6.28)  # Random phase
            })
    
    def run(self):
        """Run the customization screen loop"""
        self.running = True
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle events
            self.check_events()
            
            # Update animations
            self.wizard_renderer.update_animation()
            self.ui.update_animation()
            self.particles.update()
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            
            # Cap framerate
            clock.tick(60)
        
        # Return whether to proceed to the game
        return self.next_screen
    
    def check_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
    
    def handle_click(self, pos):
        """Handle mouse click events"""
        # Check which button was clicked
        action = self.ui.check_button_click(pos)
        
        if action == "back":
            # Go back to main menu
            self.running = False
            return
        
        elif action == "start":
            # Save customization and start game
            self.save_customization()
            self.running = False
            self.next_screen = 'game'
            return
        
        elif action == "color_prev":
            # Previous color
            self.selected_color = (self.selected_color - 1) % len(self.wizard_renderer.robe_colors)
            self.create_color_change_particles()
            
        elif action == "color_next":
            # Next color
            self.selected_color = (self.selected_color + 1) % len(self.wizard_renderer.robe_colors)
            self.create_color_change_particles()
    
    def create_color_change_particles(self):
        """Create particles for color change effect"""
        # Center position for the wizard
        center_x = self.settings.window_width // 2
        center_y = self.settings.window_height - 250
        
        # Create particles with the selected color
        color = self.wizard_renderer.robe_colors[self.selected_color]
        self.particles.create_color_change_particles(center_x, center_y, color)
    
    def draw(self):
        """Draw all elements of the customization screen"""
        # Draw background
        self.ui.draw_background()
        
        # Draw stars if no background image
        if not self.assets.get_image('background'):
            self.draw_stars()
        
        # Draw title
        self.ui.draw_title()
        
        # Draw panel
        self.ui.draw_panel()
        
        # Draw preview in the panel
        preview_y = self.ui.panel_rect.top + 120
        self.wizard_renderer.draw_robe_preview(
            self.screen, 
            self.settings.window_width // 2, 
            preview_y, 
            self.selected_color
        )
        
        # Draw full wizard preview at bottom of screen
        wizard_x = self.settings.window_width // 2
        wizard_y = self.settings.window_height - 250
        self.wizard_renderer.draw_full_wizard(
            self.screen,
            wizard_x,
            wizard_y,
            self.selected_color
        )
        
        # Draw UI buttons
        self.ui.draw_buttons(
            self.selected_color, 
            len(self.wizard_renderer.robe_colors)
        )
        
        # Draw particles
        self.particles.draw(self.screen)
    
    def draw_stars(self):
        """Draw animated background stars"""
        for star in self.stars:
            # Animate star size with pulsing effect
            size = star['size'] * (0.7 + 0.3 * math.sin(star['pulse']))
            star['pulse'] += 0.01
            
            # Calculate brightness based on size
            brightness = 150 + int(105 * math.sin(star['pulse']))
            color = (brightness, brightness, brightness)
            
            # Draw the star
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), size)
    
    def save_customization(self):
        """Save the selected customization to game settings"""
        # Get color name
        color_name = self.wizard_renderer.color_names[self.selected_color]
        
        # Get fixed hat and staff styles
        hat_style = self.wizard_renderer.hat_style
        staff_style = self.wizard_renderer.staff_style
        
        # Create customization data
        wizard_data = {
            'color': self.wizard_renderer.robe_colors[self.selected_color],
            'color_name': color_name,
            'hat': hat_style,
            'staff': staff_style,
            'magic_color': self.wizard_renderer.magic_colors[self.selected_color],
            'magic_power': 1.2  # Default power level
        }
        
        # Save to settings
        self.settings.wizard_customization = wizard_data 