import pygame
import math
import random

class WizardRenderer:
    def __init__(self, settings, assets):
        self.settings = settings
        self.assets = assets
        self.frame = 0
        self.preview_bob = 0
        self.preview_scale = 1.0
        
        # Available colors for wizard robes
        self.robe_colors = [
            (180, 30, 30),    # Crimson
            (30, 150, 70),    # Emerald
            (40, 80, 180),    # Sapphire
            (220, 160, 40),   # Amber
            (130, 60, 180),   # Violet
            (40, 160, 160),   # Teal
            (180, 140, 220),  # Lavender
            (200, 100, 100)   # Rose
        ]
        
        # Color names for display
        self.color_names = ["Crimson", "Emerald", "Sapphire", "Amber", "Violet", "Teal", "Lavender", "Rose"]
        
        # Fixed hat and staff styles
        self.hat_style = 'pointed'
        self.staff_style = 'crystal'
        
        # Magic colors for each robe color
        self.magic_colors = [
            (220, 100, 100),  # Crimson magic
            (100, 220, 100),  # Emerald magic
            (100, 120, 240),  # Sapphire magic
            (240, 200, 80),   # Amber magic
            (180, 100, 240),  # Violet magic
            (80, 220, 220),   # Teal magic
            (200, 180, 240),  # Lavender magic
            (240, 160, 160)   # Rose magic
        ]
    
    def update_animation(self):
        """Update animation values for rendering"""
        self.frame += 1
        self.preview_bob = math.sin(self.frame * 0.05) * 3
        self.preview_scale = 1.0 + math.sin(self.frame * 0.03) * 0.05
    
    def draw_robe_preview(self, screen, x, y, color_index):
        """Draw a preview of the robe color option"""
        # Apply animation
        y_offset = self.preview_bob
        
        # Draw color sample with more interesting shape
        color_sample_width = 80
        color_sample_height = 120
        
        # Main robe shape (tapered at bottom for more natural look)
        points = [
            (x - color_sample_width//2, y - color_sample_height//2 + y_offset),  # top left
            (x + color_sample_width//2, y - color_sample_height//2 + y_offset),  # top right
            (x + color_sample_width//3, y + color_sample_height//2 + y_offset),  # bottom right
            (x - color_sample_width//3, y + color_sample_height//2 + y_offset)   # bottom left
        ]
        
        # Draw robe shape
        pygame.draw.polygon(screen, self.robe_colors[color_index], points)
        pygame.draw.polygon(screen, (40, 40, 40), points, 2)
        
        # Add robe decorations
        # Collar
        collar_points = [
            (x - color_sample_width//2, y - color_sample_height//2 + 15 + y_offset),  # left
            (x + color_sample_width//2, y - color_sample_height//2 + 15 + y_offset),  # right
            (x + color_sample_width//2, y - color_sample_height//2 + y_offset),       # top right
            (x - color_sample_width//2, y - color_sample_height//2 + y_offset)        # top left
        ]
        
        # Lighter shade for collar
        collar_color = self._lighter_shade(self.robe_colors[color_index], 30)
        pygame.draw.polygon(screen, collar_color, collar_points)
        
        # Belt at middle
        belt_y = y - color_sample_height//4 + y_offset
        belt_color = self._darker_shade(self.robe_colors[color_index], 50)
        pygame.draw.line(screen, belt_color, 
                      (x - color_sample_width//2, belt_y), 
                      (x + color_sample_width//2, belt_y), 
                      5)
        
        # Add magical emblem
        emblem_y = y - color_sample_height//4 - 15 + y_offset
        emblem_size = 14
        pygame.draw.circle(screen, (255, 220, 100), (x, emblem_y), emblem_size)
        
        # Add emblem details - magical symbol
        symbol_size = emblem_size - 4
        symbol_points = []
        for i in range(5):  # 5-pointed star
            angle = math.pi/2 + i * 2*math.pi/5
            inner_angle = angle + math.pi/5
            # Outer point
            symbol_points.append((
                x + math.cos(angle) * symbol_size,
                emblem_y + math.sin(angle) * symbol_size
            ))
            # Inner point
            symbol_points.append((
                x + math.cos(inner_angle) * (symbol_size/2.5),
                emblem_y + math.sin(inner_angle) * (symbol_size/2.5)
            ))
        
        pygame.draw.polygon(screen, self.magic_colors[color_index], symbol_points)
        
        # Add magical glow effect around emblem
        glow_size = emblem_size + 2 + math.sin(self.frame * 0.1) * 2
        pygame.draw.circle(screen, self.magic_colors[color_index], (x, emblem_y), glow_size, 1)
        
        # Draw color name label
        color_label = self.assets.get_font('text').render(
            self.color_names[color_index], 
            True, 
            self.assets.get_color('text_light')
        )
        screen.blit(color_label, (x - color_label.get_width() // 2, y + color_sample_height//2 + 15))
    
    def draw_full_wizard(self, screen, x, y, color_index):
        """Draw the full wizard with the selected color"""
        # Apply animation
        y_offset = self.preview_bob * 1.5
        
        # Draw magical aura under the wizard
        self._draw_magical_aura(screen, x, y + 75, color_index)
        
        # Draw full wizard
        wizard_width = 60
        wizard_height = 120
        
        # Apply scale effect
        wizard_width = int(wizard_width * self.preview_scale)
        wizard_height = int(wizard_height * self.preview_scale)
        
        # Robe is tapered at the bottom for a more realistic look
        robe_top_width = wizard_width
        robe_bottom_width = wizard_width * 1.3  # Wider at bottom
        
        # Main robe shape
        robe_points = [
            (x - robe_top_width//2, y - wizard_height//2 + y_offset),                    # top left
            (x + robe_top_width//2, y - wizard_height//2 + y_offset),                    # top right
            (x + robe_bottom_width//2, y + wizard_height//2 + y_offset),                 # bottom right
            (x - robe_bottom_width//2, y + wizard_height//2 + y_offset)                  # bottom left
        ]
        
        # Draw robe
        pygame.draw.polygon(screen, self.robe_colors[color_index], robe_points)
        pygame.draw.polygon(screen, (40, 40, 40), robe_points, 2)
        
        # Draw arms with sleeve details
        self._draw_wizard_arms(screen, x, y, y_offset, color_index)
        
        # Add decorative elements to robe
        self._draw_robe_details(screen, x, y, y_offset, robe_points, color_index)
        
        # Draw wizard's face with more detail
        self._draw_wizard_face(screen, x, y + y_offset)
        
        # Draw wizard's hat
        self._draw_wizard_hat(screen, x, y + y_offset, color_index)
        
        # Draw wizard's staff
        self._draw_wizard_staff(screen, x, y, y_offset, color_index)
    
    def _draw_magical_aura(self, screen, x, y, color_index):
        """Draw magical aura/circle under the wizard"""
        # Base radius with pulsing animation
        radius = 50 + math.sin(self.frame * 0.1) * 5
        
        # Use the magic color associated with the robe color
        magic_color = self.magic_colors[color_index]
        
        # Draw multiple circles with fading opacity for a glow effect
        for r in range(int(radius), int(radius - 15), -1):
            alpha = int(150 * (r - (radius - 15)) / 15)
            # Create a surface for the semi-transparent circle
            circle_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surf, (*magic_color, alpha), (r, r), r)
            screen.blit(circle_surf, (x-r, y-r))
        
        # Add magical symbols within the aura
        self._draw_magical_symbols(screen, x, y, color_index)
    
    def _draw_magical_symbols(self, screen, x, y, color_index):
        """Draw magical symbols within the aura"""
        magic_color = self.magic_colors[color_index]
        
        # Draw a few runes/symbols around the circle
        for i in range(4):
            angle = self.frame * 0.01 + i * math.pi/2
            symbol_x = x + math.cos(angle) * 30
            symbol_y = y + math.sin(angle) * 30
            
            # Draw a magical rune (simple geometric shape)
            if i % 2 == 0:
                # Star
                size = 6
                points = []
                for j in range(5):
                    point_angle = angle + j * 2*math.pi/5
                    points.append((
                        symbol_x + math.cos(point_angle) * size,
                        symbol_y + math.sin(point_angle) * size
                    ))
                pygame.draw.polygon(screen, magic_color, points)
            else:
                # Circle with inner details
                pygame.draw.circle(screen, magic_color, (int(symbol_x), int(symbol_y)), 6)
                pygame.draw.circle(screen, (255, 255, 200), (int(symbol_x), int(symbol_y)), 3)
    
    def _draw_wizard_arms(self, screen, x, y, y_offset, color_index):
        """Draw the wizard's arms with sleeve details"""
        arm_width = 15
        arm_length = 50
        robe_color = self.robe_colors[color_index]
        
        # Left arm/sleeve
        left_sleeve = [
            (x - wizard_width//2 - 5, y - wizard_height//4 + y_offset),            # top connection
            (x - wizard_width//2 - arm_width, y - wizard_height//8 + y_offset),    # outer top
            (x - wizard_width//2 - arm_width, y + arm_length//2 + y_offset),       # outer bottom
            (x - wizard_width//2, y + arm_length//3 + y_offset)                    # inner bottom
        ]
        pygame.draw.polygon(screen, robe_color, left_sleeve)
        pygame.draw.polygon(screen, (40, 40, 40), left_sleeve, 1)
        
        # Right arm/sleeve
        right_sleeve = [
            (x + wizard_width//2 + 5, y - wizard_height//4 + y_offset),            # top connection
            (x + wizard_width//2 + arm_width, y - wizard_height//8 + y_offset),    # outer top
            (x + wizard_width//2 + arm_width, y + arm_length//2 + y_offset),       # outer bottom
            (x + wizard_width//2, y + arm_length//3 + y_offset)                    # inner bottom
        ]
        pygame.draw.polygon(screen, robe_color, right_sleeve)
        pygame.draw.polygon(screen, (40, 40, 40), right_sleeve, 1)
        
        # Draw hands
        hand_color = (240, 220, 190)  # Skin tone
        pygame.draw.circle(screen, hand_color, 
                        (int(right_sleeve[2][0] - 5), int(right_sleeve[2][1] + 5)), 8)
        pygame.draw.circle(screen, hand_color, 
                        (int(left_sleeve[2][0] + 5), int(left_sleeve[2][1] + 5)), 8)
    
    def _draw_robe_details(self, screen, x, y, y_offset, robe_points, color_index):
        """Draw decorative details on the wizard's robe"""
        robe_color = self.robe_colors[color_index]
        
        # Collar (lighter shade)
        collar_height = 15
        collar_points = [
            (robe_points[0][0], robe_points[0][1]),                          # top left
            (robe_points[1][0], robe_points[1][1]),                          # top right
            (robe_points[1][0], robe_points[1][1] + collar_height),          # bottom right
            (robe_points[0][0], robe_points[0][1] + collar_height)           # bottom left
        ]
        collar_color = self._lighter_shade(robe_color, 30)
        pygame.draw.polygon(screen, collar_color, collar_points)
        
        # Belt at middle (darker shade)
        belt_y = y + y_offset
        belt_width = int((robe_points[1][0] - robe_points[0][0]) * 1.1)  # slightly wider than robe
        belt_color = self._darker_shade(robe_color, 50)
        belt_rect = pygame.Rect(
            x - belt_width//2,
            belt_y - 5,
            belt_width,
            10
        )
        pygame.draw.rect(screen, belt_color, belt_rect)
        
        # Belt buckle (gold)
        buckle_size = 14
        pygame.draw.circle(screen, (255, 220, 100), (x, belt_y), buckle_size)
        pygame.draw.circle(screen, (40, 40, 40), (x, belt_y), buckle_size, 1)
        
        # Magical embroidery/symbols on robe
        magic_color = self.magic_colors[color_index]
        symbol_positions = [
            (x, y - wizard_height//4 + y_offset),                     # chest symbol
            (x - wizard_width//3, y + wizard_height//4 + y_offset),   # left side
            (x + wizard_width//3, y + wizard_height//4 + y_offset)    # right side
        ]
        
        for pos in symbol_positions:
            # Draw emblem background
            pygame.draw.circle(screen, (255, 220, 100), pos, 8)
            
            # Draw magical symbol inside
            self._draw_small_magical_symbol(screen, pos[0], pos[1], magic_color)
            
            # Add glow
            glow_size = 8 + math.sin(self.frame * 0.1 + symbol_positions.index(pos)) * 2
            pygame.draw.circle(screen, magic_color, pos, glow_size, 1)
    
    def _draw_small_magical_symbol(self, screen, x, y, color):
        """Draw a small magical symbol/rune"""
        size = 5
        # Simple 5-point star
        points = []
        for i in range(5):
            angle = self.frame * 0.01 + i * 2*math.pi/5
            points.append((
                x + math.cos(angle) * size,
                y + math.sin(angle) * size
            ))
        
        pygame.draw.polygon(screen, color, points)
    
    def _draw_wizard_face(self, screen, x, y):
        """Draw the wizard's face with more details"""
        # Face shape - more oval than circle
        face_width = 24
        face_height = 30
        face_color = (240, 220, 190)  # Skin tone
        
        face_rect = pygame.Rect(
            x - face_width//2,
            y - wizard_height//2 + 10,
            face_width,
            face_height
        )
        pygame.draw.ellipse(screen, face_color, face_rect)
        
        # Add facial features
        eye_y = face_rect.top + face_height//3
        eye_spacing = 8
        
        # Eyes with detail
        # Left eye
        pygame.draw.circle(screen, (250, 250, 250), (x - eye_spacing//2, eye_y), 4)  # Eyeball
        pygame.draw.circle(screen, (30, 30, 60), (x - eye_spacing//2, eye_y), 2)     # Pupil
        # Right eye
        pygame.draw.circle(screen, (250, 250, 250), (x + eye_spacing//2, eye_y), 4)  # Eyeball
        pygame.draw.circle(screen, (30, 30, 60), (x + eye_spacing//2, eye_y), 2)     # Pupil
        
        # Eyebrows
        brow_y = eye_y - 5
        pygame.draw.line(screen, (150, 130, 110), 
                      (x - eye_spacing//2 - 4, brow_y), 
                      (x - eye_spacing//2 + 3, brow_y - 1), 
                      2)
        pygame.draw.line(screen, (150, 130, 110), 
                      (x + eye_spacing//2 - 3, brow_y - 1), 
                      (x + eye_spacing//2 + 4, brow_y), 
                      2)
        
        # Nose
        nose_y = eye_y + 6
        pygame.draw.line(screen, (220, 200, 170), 
                      (x, eye_y + 3), 
                      (x + 2, nose_y), 
                      1)
        
        # Mouth - slight smile
        mouth_y = face_rect.top + face_height * 2//3
        pygame.draw.arc(screen, (180, 120, 120), 
                     pygame.Rect(x - 5, mouth_y - 3, 10, 6),
                     0, math.pi, 1)
        
        # Beard - more detailed and flowing
        beard_top = face_rect.top + face_height * 2//3
        beard_color = (220, 220, 220)  # White/gray beard
        
        # Longer flowing beard points
        beard_points = [
            (x - face_width//2 + 4, beard_top),                        # left top
            (x + face_width//2 - 4, beard_top),                        # right top
            (x + face_width//3, beard_top + face_height//2 + 10),      # right middle
            (x, beard_top + face_height//2 + 15),                      # bottom point
            (x - face_width//3, beard_top + face_height//2 + 10)       # left middle
        ]
        pygame.draw.polygon(screen, beard_color, beard_points)
        
        # Add beard texture with a few lines
        for i in range(3):
            line_x = x - 5 + i * 5
            pygame.draw.line(screen, (200, 200, 200), 
                          (line_x, beard_top + 5), 
                          (line_x - 2, beard_top + face_height//2 + 5), 
                          1)
    
    def _draw_wizard_hat(self, screen, x, y, color_index):
        """Draw a more detailed wizard hat"""
        hat_color = (80, 60, 120)  # Deep purple base for the hat
        magic_color = self.magic_colors[color_index]
        
        # Hat base shape - wider brim
        brim_width = wizard_width * 1.5
        brim_height = 12
        brim_y = y - wizard_height//2
        
        brim_points = [
            (x - brim_width//2, brim_y),                  # left
            (x + brim_width//2, brim_y),                  # right
            (x + wizard_width//2, brim_y - brim_height),  # inner right
            (x - wizard_width//2, brim_y - brim_height)   # inner left
        ]
        pygame.draw.polygon(screen, hat_color, brim_points)
        
        # Hat cone - taller and more curved
        cone_height = 50
        cone_curve = 10  # amount of curve/bend
        
        tip_x = x + cone_curve  # Slight bend to the right
        tip_y = brim_y - brim_height - cone_height
        
        cone_points = [
            (x - wizard_width//2, brim_y - brim_height),   # left
            (x + wizard_width//2, brim_y - brim_height),   # right
            (tip_x, tip_y)                                 # tip
        ]
        pygame.draw.polygon(screen, hat_color, cone_points)
        
        # Hat decoration - band with magical emblem
        band_y = brim_y - brim_height + 5
        pygame.draw.line(screen, (255, 220, 100), 
                      (x - wizard_width//2 - 3, band_y), 
                      (x + wizard_width//2 + 3, band_y), 
                      3)
        
        # Magical emblem on hat
        emblem_x = x + wizard_width//6
        emblem_y = band_y
        pygame.draw.circle(screen, (255, 220, 100), (emblem_x, emblem_y), 7)
        
        # Star symbol in emblem
        star_size = 4
        star_points = []
        for i in range(5):
            angle = self.frame * 0.01 + i * 2*math.pi/5
            star_points.append((
                emblem_x + math.cos(angle) * star_size,
                emblem_y + math.sin(angle) * star_size
            ))
        pygame.draw.polygon(screen, magic_color, star_points)
        
        # Add some stars/sparkles on the hat
        for i in range(3):
            spark_x = x - wizard_width//4 + i * wizard_width//4
            spark_y = brim_y - brim_height - cone_height//2 + i * cone_height//6
            
            # Animate the sparkles
            if (self.frame + i*10) % 60 < 30:
                size = 2
                pygame.draw.circle(screen, (255, 255, 200), (spark_x, spark_y), size)
                pygame.draw.circle(screen, magic_color, (spark_x, spark_y), size+1, 1)
    
    def _draw_wizard_staff(self, screen, x, y, y_offset, color_index):
        """Draw a detailed wizard staff"""
        staff_width = 8
        staff_height = 140
        magic_color = self.magic_colors[color_index]
        
        # Staff base position - held by the right hand
        staff_x = x + wizard_width//2 + 15
        staff_y = y + 10 + y_offset
        
        # Staff body - slightly curved
        staff_curve = 5
        staff_points = [
            (staff_x, staff_y),                                     # top
            (staff_x + staff_width, staff_y),                       # top right
            (staff_x + staff_width + staff_curve, staff_y + staff_height),  # bottom right with curve
            (staff_x + staff_curve, staff_y + staff_height)                 # bottom left with curve
        ]
        
        # Wood grain texture for staff
        wood_color = (120, 80, 40)
        pygame.draw.polygon(screen, wood_color, staff_points)
        pygame.draw.polygon(screen, (60, 40, 20), staff_points, 1)
        
        # Add wood grain lines
        for i in range(0, staff_height, 12):
            line_y = staff_y + i
            curve_offset = staff_curve * i / staff_height
            pygame.draw.line(screen, (100, 60, 30), 
                         (staff_x + curve_offset, line_y), 
                         (staff_x + staff_width + curve_offset, line_y), 
                         1)
        
        # Crystal top for the staff
        crystal_width = 20
        crystal_height = 30
        crystal_x = staff_x - crystal_width//2 + staff_width//2
        crystal_y = staff_y - crystal_height
        
        # Crystal shape - more complex with multiple facets
        crystal_points = [
            (crystal_x, crystal_y + crystal_height),                    # bottom center
            (crystal_x - crystal_width//2, crystal_y + crystal_height*2//3),  # bottom left
            (crystal_x - crystal_width//3, crystal_y + crystal_height//3),    # middle left
            (crystal_x, crystal_y),                                     # top
            (crystal_x + crystal_width//3, crystal_y + crystal_height//3),    # middle right
            (crystal_x + crystal_width//2, crystal_y + crystal_height*2//3)   # bottom right
        ]
        
        # Crystal base color with transparency
        crystal_surface = pygame.Surface((crystal_width*2, crystal_height*2), pygame.SRCALPHA)
        crystal_color = (*magic_color, 180)  # Add alpha channel
        pygame.draw.polygon(crystal_surface, crystal_color, 
                         [(p[0]-crystal_x+crystal_width, p[1]-crystal_y+crystal_height) for p in crystal_points])
        
        # Add highlight to crystal
        highlight_points = [
            crystal_points[3],  # top
            crystal_points[2],  # middle left
            crystal_points[4]   # middle right
        ]
        pygame.draw.polygon(crystal_surface, (255, 255, 255, 100), 
                         [(p[0]-crystal_x+crystal_width, p[1]-crystal_y+crystal_height) for p in highlight_points])
        
        # Add crystal to the screen
        screen.blit(crystal_surface, (crystal_x-crystal_width, crystal_y-crystal_height))
        
        # Add magical glow around crystal
        glow_size = 15 + math.sin(self.frame * 0.1) * 3
        glow_x = crystal_x
        glow_y = crystal_y + crystal_height//2
        
        # Create a surface for the glow with transparency
        glow_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        for i in range(3):
            alpha = 100 - i*30
            pygame.draw.circle(glow_surface, (*magic_color, alpha), (glow_size, glow_size), glow_size-i*3)
        
        screen.blit(glow_surface, (glow_x-glow_size, glow_y-glow_size))
        
        # Add small magical particles around the crystal
        if random.random() < 0.2:  # Occasional particles
            for _ in range(2):
                particle_x = crystal_x + random.uniform(-crystal_width, crystal_width)
                particle_y = crystal_y + random.uniform(0, crystal_height)
                particle_size = random.uniform(1, 3)
                
                pygame.draw.circle(screen, magic_color, (particle_x, particle_y), particle_size)
                # Add glow
                pygame.draw.circle(screen, (255, 255, 200), (particle_x, particle_y), particle_size+1, 1)
    
    def _lighter_shade(self, color, amount):
        """Create a lighter shade of the given color"""
        return (
            min(255, color[0] + amount),
            min(255, color[1] + amount),
            min(255, color[2] + amount)
        )
    
    def _darker_shade(self, color, amount):
        """Create a darker shade of the given color"""
        return (
            max(0, color[0] - amount),
            max(0, color[1] - amount),
            max(0, color[2] - amount)
        )

# Global variables for dimensions
wizard_width = 60
wizard_height = 120 