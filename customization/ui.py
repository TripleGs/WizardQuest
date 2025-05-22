import pygame
import math

class CustomizationUI:
    def __init__(self, settings, assets):
        self.settings = settings
        self.assets = assets
        self.screen = pygame.display.get_surface()
        self.frame = 0
        
        # Create UI elements
        self.create_layout()
    
    def create_layout(self):
        """Create the layout for the customization screen"""
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
        
        # Color selection position
        self.color_section_rect = pygame.Rect(
            panel_x + margin,
            panel_y + margin,
            panel_width - margin*2,
            panel_height - margin*2
        )
        
        # Arrows for color selection
        self.color_left = pygame.Rect(
            self.settings.window_width//2 - arrow_button_width - margin,
            panel_y + panel_height - arrow_button_height - margin,
            arrow_button_width,
            arrow_button_height
        )
        
        self.color_right = pygame.Rect(
            self.settings.window_width//2 + margin,
            panel_y + panel_height - arrow_button_height - margin,
            arrow_button_width,
            arrow_button_height
        )
    
    def update_animation(self):
        """Update animation values"""
        self.frame += 1
    
    def draw_background(self):
        """Draw the screen background"""
        # Use background image if available
        background = self.assets.get_image('background')
        if background:
            self.screen.blit(background, (0, 0))
        else:
            # Fallback to color fill
            self.screen.fill(self.assets.get_color('background'))
    
    def draw_title(self):
        """Draw the customization screen title with animation"""
        title_text = "Customize Your Wizard"
        title_y = 50
        title_offset = math.sin(self.frame * 0.05) * 3
        
        # Draw glow effect
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
    
    def draw_panel(self):
        """Draw the main panel for customization"""
        # Draw wooden panel background
        panel_image = self.assets.get_image('panel_wood')
        if panel_image:
            # Scale panel image to fit customization area
            scaled_panel = pygame.transform.scale(panel_image, (self.panel_rect.width, self.panel_rect.height))
            self.screen.blit(scaled_panel, self.panel_rect)
        else:
            # Fallback to simple rect
            pygame.draw.rect(self.screen, self.assets.get_color('wood_dark'), self.panel_rect)
            pygame.draw.rect(self.screen, self.assets.get_color('wood_light'), self.panel_rect, 4)
        
        # Draw section header
        header_text = "Select Robe Color"
        header_y = self.panel_rect.top + 30
        
        # Draw header shadow
        header_shadow = self.assets.get_font('button').render(header_text, True, (50, 30, 10))
        shadow_rect = header_shadow.get_rect(center=(self.settings.window_width//2 + 2, header_y + 2))
        self.screen.blit(header_shadow, shadow_rect)
        
        # Draw header text
        header_text = self.assets.get_font('button').render(header_text, True, self.assets.get_color('text_light'))
        header_rect = header_text.get_rect(center=(self.settings.window_width//2, header_y))
        self.screen.blit(header_text, header_rect)
    
    def draw_buttons(self, selected_color_index, total_colors):
        """Draw all buttons with proper styling"""
        # Get colors for buttons
        button_color = self.assets.get_color('wood_dark')
        hover_color = (175, 95, 30)  # Warmer wood color for hover
        border_color = (255, 215, 0)  # Gold border
        text_color = (255, 250, 230)  # Cream colored text
        
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw navigation buttons
        self._draw_navigation_button(self.back_button, "Back", mouse_pos, button_color, hover_color, text_color, border_color)
        self._draw_navigation_button(self.start_button, "Start Game", mouse_pos, button_color, hover_color, text_color, border_color)
        
        # Draw color selection buttons
        self._draw_arrow_button(self.color_left, "left", mouse_pos, button_color, hover_color, text_color, border_color)
        self._draw_arrow_button(self.color_right, "right", mouse_pos, button_color, hover_color, text_color, border_color)
        
        # Draw color index indicator
        index_text = f"{selected_color_index + 1}/{total_colors}"
        index_font = self.assets.get_font('text')
        index_label = index_font.render(index_text, True, text_color)
        index_rect = index_label.get_rect(center=(self.settings.window_width//2, self.color_left.centery))
        self.screen.blit(index_label, index_rect)
    
    def _draw_navigation_button(self, rect, text, mouse_pos, button_color, hover_color, text_color, border_color):
        """Draw a navigation button with hover effects"""
        # Draw button with wooden texture
        button_image = self.assets.get_image('button_wood')
        if button_image and not rect.collidepoint(mouse_pos):
            # Scale image to button size
            scaled_button = pygame.transform.scale(button_image, (rect.width, rect.height))
            self.screen.blit(scaled_button, rect)
        else:
            # Draw custom background for hover or fallback
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, hover_color, rect, border_radius=5)
            else:
                pygame.draw.rect(self.screen, button_color, rect, border_radius=5)
        
        # Add decorative border
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)
        
        # Add shine effect on hover
        if rect.collidepoint(mouse_pos):
            shine_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            for i in range(5):
                alpha = 50 - i * 10
                y_pos = i * 2
                pygame.draw.line(
                    shine_surface, 
                    (255, 255, 255, alpha), 
                    (0, y_pos), 
                    (rect.width, y_pos), 
                    2
                )
            self.screen.blit(shine_surface, rect)
        
        # Draw button text with shadow
        font = self.assets.get_font('button')
        # Text shadow
        shadow_text = font.render(text, True, (40, 20, 0))
        shadow_rect = shadow_text.get_rect(center=(rect.center[0] + 2, rect.center[1] + 2))
        self.screen.blit(shadow_text, shadow_rect)
        
        # Main text
        button_text = font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)
    
    def _draw_arrow_button(self, rect, direction, mouse_pos, button_color, hover_color, text_color, border_color):
        """Draw an arrow button with hover effects"""
        # Draw circular button with wooden texture
        is_hover = rect.collidepoint(mouse_pos)
        
        # Background
        if is_hover:
            pygame.draw.rect(self.screen, hover_color, rect, border_radius=5)
        else:
            pygame.draw.rect(self.screen, button_color, rect, border_radius=5)
        
            # Add wood grain texture
            for i in range(3):
                line_y = rect.top + 10 + i * 7
                pygame.draw.line(
                    self.screen,
                    (100, 60, 30),
                    (rect.left + 5, line_y),
                    (rect.right - 5, line_y),
                    1
                )
        
        # Add decorative border
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)
        
        # Draw arrow shape based on direction
        if direction == "left":
            arrow_points = [
                (rect.centerx + 8, rect.top + 10),
                (rect.centerx - 8, rect.centery),
                (rect.centerx + 8, rect.bottom - 10)
            ]
        else:  # right
            arrow_points = [
                (rect.centerx - 8, rect.top + 10),
                (rect.centerx + 8, rect.centery),
                (rect.centerx - 8, rect.bottom - 10)
            ]
        
        # Draw arrow with glow effect
        if is_hover:
            # Glow effect
            for i in range(3):
                glow_size = 3 - i
                glow_points = []
                for point in arrow_points:
                    glow_points.append((point[0], point[1]))
                pygame.draw.polygon(self.screen, (255, 230, 150), glow_points, glow_size)
        
        # Main arrow
        pygame.draw.polygon(self.screen, text_color, arrow_points)
    
    def check_button_click(self, pos):
        """Check if a button was clicked and return the action"""
        if self.back_button.collidepoint(pos):
            return "back"
        elif self.start_button.collidepoint(pos):
            return "start"
        elif self.color_left.collidepoint(pos):
            return "color_prev"
        elif self.color_right.collidepoint(pos):
            return "color_next"
        return None 