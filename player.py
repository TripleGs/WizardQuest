import pygame
import random
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.assets = game.assets
        
        # Player properties
        self.width = 40
        self.height = 60
        self.x = self.settings.window_width // 2
        self.y = self.settings.window_height // 2
        self.speed = 5
        self.jump_power = -15
        self.velocity_y = 0
        self.velocity_x = 0
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        
        # Health and damage
        self.max_health = 100
        self.health = self.max_health
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.damage_flash = 0
        
        # Animation properties
        self.frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        
        # Create player rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Spell properties - magic now comes directly from hands
        self.spell_cooldown = 0
        self.spell_cooldown_time = 20  # Faster without staff
        self.spells = []
        
        # Load customization
        self.customization = self.settings.wizard_customization
        
        # Create player surfaces
        self.create_player_surfaces()
    
    def create_player_surfaces(self):
        # Create body surface with the customized color
        self.body_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Make sure we have valid color data
        if isinstance(self.customization['color'], tuple) and len(self.customization['color']) >= 3:
            robe_color = self.customization['color']
        else:
            # Default to crimson if color is invalid
            robe_color = (180, 30, 30)
        
        # Draw the robe with proper shape
        # Tapered bottom for more realistic look
        robe_points = [
            (0, 0),                         # top left
            (self.width, 0),                # top right
            (self.width + 10, self.height),  # bottom right (wider for better drape)
            (-10, self.height)               # bottom left (wider for better drape)
        ]
        
        # Fill the body surface with the robe
        pygame.draw.polygon(self.body_surface, robe_color, robe_points)
        pygame.draw.polygon(self.body_surface, (40, 40, 40), robe_points, 1)
        
        # Add collar (lighter shade)
        collar_color = self._lighter_shade(robe_color, 30)
        collar_points = [
            (0, 0),                  # top left
            (self.width, 0),         # top right
            (self.width, 12),        # bottom right (slightly taller)
            (0, 12)                  # bottom left (slightly taller)
        ]
        pygame.draw.polygon(self.body_surface, collar_color, collar_points)
        
        # Add belt (darker shade)
        belt_y = self.height // 2
        belt_color = self._darker_shade(robe_color, 50)
        pygame.draw.rect(self.body_surface, belt_color, (0, belt_y - 5, self.width, 10))
        
        # Add magical emblem on chest with more detail
        emblem_size = 10
        emblem_center = (self.width // 2, self.height // 4)
        # Gold circle background
        pygame.draw.circle(self.body_surface, (255, 220, 100), emblem_center, emblem_size)
        
        # Add magical symbol inside emblem (small star)
        symbol_points = []
        for i in range(5):  # 5-pointed star
            outer_angle = math.pi/2 + i * 2*math.pi/5
            inner_angle = outer_angle + math.pi/5
            # Outer point
            symbol_points.append((
                emblem_center[0] + math.cos(outer_angle) * (emblem_size-4),
                emblem_center[1] + math.sin(outer_angle) * (emblem_size-4)
            ))
            # Inner point
            symbol_points.append((
                emblem_center[0] + math.cos(inner_angle) * (emblem_size-7),
                emblem_center[1] + math.sin(inner_angle) * (emblem_size-7)
            ))
        
        # Use magic color for the symbol if available
        if 'magic_color' in self.customization and isinstance(self.customization['magic_color'], tuple):
            magic_color = self.customization['magic_color'][:3]
        else:
            magic_color = (150, 100, 250)  # Default purple
            
        pygame.draw.polygon(self.body_surface, magic_color, symbol_points)
        
        # Add robe decoration lines for more detail
        for i in range(2):
            line_y = self.height // 3 + i * 30
            pygame.draw.line(
                self.body_surface, 
                self._darker_shade(robe_color, 30),
                (5, line_y),
                (self.width - 5, line_y),
                1
            )
        
        # Add hands
        hand_color = (240, 220, 190)  # Skin tone
        
        # Left hand
        pygame.draw.circle(self.body_surface, hand_color, (5, self.height // 2), 6)
        
        # Right hand
        pygame.draw.circle(self.body_surface, hand_color, (self.width - 5, self.height // 2), 6)
        
        # Draw face
        face_y = 8  # Position face at top of robe
        self._draw_wizard_face(self.body_surface, self.width // 2, face_y)
        
        # Create hat surface - match customization screen exactly
        hat_color = (80, 60, 120)  # Deep purple base for the hat, matching customization
        
        # Hat dimensions based on body size
        hat_width = int(self.width * 1.5)  # Wide brim like in customization
        hat_height = int(hat_width * 0.6)  # Better height ratio
        
        self.hat_surface = pygame.Surface((hat_width, hat_height), pygame.SRCALPHA)
        
        # Draw hat brim - wider at bottom
        brim_height = hat_height // 4
        brim_points = [
            (0, hat_height - brim_height),                   # bottom left
            (hat_width, hat_height - brim_height),           # bottom right
            (hat_width * 3 // 4, hat_height - brim_height * 2), # inner right
            (hat_width // 4, hat_height - brim_height * 2)      # inner left
        ]
        pygame.draw.polygon(self.hat_surface, hat_color, brim_points)
        
        # Draw hat cone - tall and slightly curved
        cone_curve = hat_width // 10  # slight curve
        tip_x = hat_width // 2 + cone_curve
        
        cone_points = [
            (hat_width // 4, hat_height - brim_height * 2),     # left
            (hat_width * 3 // 4, hat_height - brim_height * 2), # right
            (tip_x, 0)                                          # tip
        ]
        pygame.draw.polygon(self.hat_surface, hat_color, cone_points)
        
        # Add gold band
        band_y = hat_height - brim_height - 2
        pygame.draw.line(self.hat_surface, (255, 220, 100), 
                       (hat_width // 4 - 3, band_y), 
                       (hat_width * 3 // 4 + 3, band_y), 
                       3)
        
        # Add emblem with star
        emblem_x = hat_width // 2 + hat_width // 10  # Slightly to the right
        emblem_y = band_y
        pygame.draw.circle(self.hat_surface, (255, 220, 100), (emblem_x, emblem_y), 6)
        
        # Add star in emblem
        if 'magic_color' in self.customization and isinstance(self.customization['magic_color'], tuple):
            magic_color = self.customization['magic_color'][:3]
        else:
            magic_color = (150, 100, 250)  # Default purple
        
        # Draw star in emblem
        star_size = 3
        star_points = []
        for i in range(5):
            angle = i * 2*math.pi/5
            star_points.append((
                emblem_x + math.cos(angle) * star_size,
                emblem_y + math.sin(angle) * star_size
            ))
        pygame.draw.polygon(self.hat_surface, magic_color, star_points)
        
        # Add sparkles to hat
        for i in range(3):
            spark_x = hat_width // 4 + i * hat_width // 6
            spark_y = hat_height // 3 + i * hat_height // 8
            pygame.draw.circle(self.hat_surface, (255, 255, 200), (spark_x, spark_y), 1)
        
        # Create flipped versions
        self.body_surface_flipped = pygame.transform.flip(self.body_surface, True, False)
        self.hat_surface_flipped = pygame.transform.flip(self.hat_surface, True, False)
    
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
    
    def update(self, platforms):
        # Handle movement
        keys = pygame.key.get_pressed()
        
        # Horizontal movement with smoother acceleration/deceleration
        if keys[pygame.K_LEFT]:
            self.velocity_x = max(self.velocity_x - 1, -self.speed)
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = min(self.velocity_x + 1, self.speed)
            self.facing_right = True
        else:
            # Deceleration when no keys pressed
            if self.velocity_x > 0:
                self.velocity_x = max(0, self.velocity_x - 0.5)
            elif self.velocity_x < 0:
                self.velocity_x = min(0, self.velocity_x + 0.5)
        
        # Store previous position for collision detection
        prev_x = self.x
        prev_y = self.y
        
        # Apply horizontal movement and check for collisions
        self.x += self.velocity_x
        self.rect.x = int(self.x)
        
        # Check for horizontal collisions with platforms
        for platform in platforms:
            platform_rect = platform['rect']
            
            # Check if colliding horizontally
            if self.rect.colliderect(platform_rect):
                # Coming from left
                if prev_x + self.width <= platform_rect.left + 2:
                    self.rect.right = platform_rect.left
                    self.x = self.rect.x
                    self.velocity_x = 0
                # Coming from right
                elif prev_x >= platform_rect.right - 2:
                    self.rect.left = platform_rect.right
                    self.x = self.rect.x
                    self.velocity_x = 0
        
        # Keep player within screen bounds
        if self.x < 0:
            self.x = 0
            self.rect.x = 0
            self.velocity_x = 0
        elif self.x > self.settings.window_width - self.width:
            self.x = self.settings.window_width - self.width
            self.rect.x = int(self.x)
            self.velocity_x = 0
            
        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            # Create jump particles
            self.assets.create_particles(
                self.x + self.width//2, 
                self.y + self.height, 
                self.assets.get_color('wood_light'), 
                count=15, 
                speed=3
            )
        
        # Apply gravity
        self.velocity_y += self.gravity
        
        # Apply vertical movement
        self.y += self.velocity_y
        self.rect.y = int(self.y)
        
        # Check for vertical collisions with platforms
        self.on_ground = False
        for platform in platforms:
            platform_rect = platform['rect']
            
            # Only check for vertical collision if we're within the platform's horizontal bounds
            horizontal_overlap = (
                self.rect.right > platform_rect.left + 5 and 
                self.rect.left < platform_rect.right - 5
            )
            
            if horizontal_overlap:
                # Landing on top of platform
                if (self.rect.bottom >= platform_rect.top and 
                    prev_y + self.height <= platform_rect.top + 5 and  # Was above or just at the top
                    self.velocity_y >= 0):  # Moving downward
                    
                    self.rect.bottom = platform_rect.top
                    self.y = self.rect.y
                    self.velocity_y = 0
                    self.on_ground = True
                    
                    # Create dust particles when landing with significant velocity
                    if abs(self.velocity_y) > 5:
                        self.assets.create_particles(
                            self.x + self.width//2, 
                            self.rect.bottom, 
                            self.assets.get_color('wood_accent'), 
                            count=int(abs(self.velocity_y)), 
                            speed=2
                        )
                
                # Hitting bottom of platform (ceiling collision)
                elif (self.rect.top <= platform_rect.bottom and 
                      prev_y >= platform_rect.bottom - 5 and  # Was below the platform
                      self.velocity_y < 0):  # Moving upward
                    
                    self.rect.top = platform_rect.bottom
                    self.y = self.rect.y
                    self.velocity_y = 0
        
        # Bottom screen boundary check
        if self.y > self.settings.window_height:
            self.y = self.settings.window_height - self.height
            self.rect.y = int(self.y)
            self.velocity_y = 0
            self.on_ground = True
        
        # Animation
        if abs(self.velocity_x) > 0.5 or not self.on_ground:
            self.animation_timer += abs(self.velocity_x) * 0.02
            if self.animation_timer >= 1:
                self.frame = (self.frame + 1) % 4
                self.animation_timer = 0
        
        # Update spell cooldown
        if self.spell_cooldown > 0:
            self.spell_cooldown -= 1
        
        # Update invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.damage_flash = 0
        
        # Update damage flash
        if self.damage_flash > 0:
            self.damage_flash -= 1
        
        # Update spells
        for spell in self.spells[:]:
            # Move spell based on direction
            if spell['direction'] == 'right':
                spell['x'] += spell['speed']
            else:
                spell['x'] -= spell['speed']
            
            # Update lifetime
            spell['lifetime'] -= 1
            
            # Remove if out of screen or lifetime ended
            if (spell['x'] < -40 or 
                spell['x'] > self.settings.window_width + 40 or 
                spell['lifetime'] <= 0):
                self.spells.remove(spell)
                
                # Create explosion particles when spell expires
                if 'color' in spell and isinstance(spell['color'], tuple) and len(spell['color']) >= 3:
                    spell_color = spell['color'][:3]
                else:
                    spell_color = (150, 100, 250)
                    
                self.assets.create_particles(
                    spell['x'], 
                    spell['y'], 
                    spell_color, 
                    count=20, 
                    speed=3, 
                    lifetime=20
                )
    
    def draw(self, surface):
        # Draw spells
        for spell in self.spells:
            # Calculate spell position
            spell_x = spell['x']
            spell_y = spell['y']
            
            # Create magical effect
            if 'image' in spell and spell['image']:
                # Scale effect based on power
                scale = 1.0
                if 'power' in spell:
                    scale = max(0.5, min(2.0, spell['power']))
                
                orig_image = spell['image']
                width = int(orig_image.get_width() * scale)
                height = int(orig_image.get_height() * scale)
                
                image = pygame.transform.scale(orig_image, (width, height))
                
                # Flip based on direction
                if spell['direction'] == 'left':
                    image = pygame.transform.flip(image, True, False)
                
                # Draw at spell position
                surface.blit(image, (spell_x - width // 2, spell_y - height // 2))
            else:
                # Fallback to simple magical effect
                # Get customized magic color
                if 'color' in spell and isinstance(spell['color'], tuple) and len(spell['color']) >= 3:
                    magic_color = spell['color'][:3]
                else:
                    magic_color = (150, 100, 250)
                
                # Create a trail of particles
                for i in range(5):
                    offset_x = -i * 5 if spell['direction'] == 'right' else i * 5
                    pygame.draw.circle(surface, magic_color, 
                                    (int(spell_x + offset_x), int(spell_y)), 
                                    5 - i)
        
        # Apply a "bobbing" effect based on animation frame
        bob_offset = math.sin(self.frame * 0.5) * 2
        
        # Get body surface based on direction
        body_surface = self.body_surface_flipped if not self.facing_right else self.body_surface
        
        # Apply damage flash effect
        if self.damage_flash > 0:
            # Create a red tinted copy of the body surface
            flash_surface = body_surface.copy()
            flash_surface.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(flash_surface, (self.x, self.y + bob_offset))
        # Apply invulnerability blinking effect
        elif self.invulnerable and self.invulnerable_timer % 6 < 3:
            # Draw semi-transparent body for invulnerability blinking
            body_surface.set_alpha(150)
            surface.blit(body_surface, (self.x, self.y + bob_offset))
            body_surface.set_alpha(255)  # Reset alpha
        else:
            # Normal drawing
            surface.blit(body_surface, (self.x, self.y + bob_offset))
        
        # Draw hat with proper positioning to match customization screen
        hat_y = self.y - self.hat_surface.get_height() + 20 + bob_offset  # Better vertical position
        hat_x = self.x + self.width//2 - self.hat_surface.get_width()//2  # Center hat precisely
        
        # Choose hat surface based on direction
        hat_surface = self.hat_surface_flipped if not self.facing_right else self.hat_surface
        
        # Apply hat transparency effect when invulnerable
        if self.invulnerable and self.invulnerable_timer % 6 < 3:
            hat_surface.set_alpha(150)
            surface.blit(hat_surface, (hat_x, hat_y))
            hat_surface.set_alpha(255)  # Reset alpha
        else:
            surface.blit(hat_surface, (hat_x, hat_y))
        
        # Draw magic aura when casting
        if self.spell_cooldown > self.spell_cooldown_time - 10:
            # Get customized magic color with fallback
            if 'magic_color' in self.customization and isinstance(self.customization['magic_color'], tuple):
                magic_color = self.customization['magic_color'][:3]  # Use only RGB components
            else:
                magic_color = (150, 100, 250)  # Default purple if invalid
            
            # Draw magical hand gesture (replacing staff)
            hand_x = self.x + (self.width + 5 if self.facing_right else -5)
            hand_y = self.y + 20 + bob_offset
            
            # Draw magic circle
            circle_radius = 8 + math.sin(self.frame * 0.2) * 2
            pygame.draw.circle(surface, magic_color, (hand_x, hand_y), circle_radius)
            pygame.draw.circle(surface, (255, 255, 255), (hand_x, hand_y), circle_radius - 2, 1)
            
            # Draw radiating particles
            for _ in range(3):
                angle = random.uniform(0, 2 * 3.14159)
                dist = random.uniform(5, 30)
                x = self.x + self.width // 2 + math.cos(angle) * dist
                y = self.y + self.height // 2 + math.sin(angle) * dist
                size = random.randint(1, 3)
                pygame.draw.circle(surface, magic_color, (int(x), int(y)), size)
    
    def _draw_wizard_face(self, surface, x, y):
        """Draw a detailed wizard face matching the customization screen"""
        # Face
        face_width = 20
        face_height = 25
        face_color = (240, 220, 190)  # Skin tone
        
        # Draw face oval
        pygame.draw.ellipse(surface, face_color, 
                         (x - face_width//2, y, face_width, face_height))
        
        # Add eyes
        eye_y = y + face_height//3
        pygame.draw.circle(surface, (50, 50, 50), (x - face_width//4, eye_y), 2)
        pygame.draw.circle(surface, (50, 50, 50), (x + face_width//4, eye_y), 2)
        
        # Add eyebrows
        eyebrow_y = eye_y - 3
        pygame.draw.line(surface, (100, 80, 80), 
                      (x - face_width//4 - 2, eyebrow_y), 
                      (x - face_width//4 + 2, eyebrow_y - 1), 
                      1)
        pygame.draw.line(surface, (100, 80, 80), 
                      (x + face_width//4 - 2, eyebrow_y - 1), 
                      (x + face_width//4 + 2, eyebrow_y), 
                      1)
        
        # Add beard
        beard_top = y + face_height * 2//3
        beard_color = (220, 220, 220)  # White/gray beard
        
        # Flowing beard points
        beard_points = [
            (x - face_width//2 + 2, beard_top),                 # left top
            (x + face_width//2 - 2, beard_top),                 # right top
            (x + face_width//3, beard_top + face_height//2),    # right middle
            (x, beard_top + face_height//2 + 5),                # bottom point
            (x - face_width//3, beard_top + face_height//2)     # left middle
        ]
        pygame.draw.polygon(surface, beard_color, beard_points)
        
        # Add beard texture with a few lines
        for i in range(3):
            line_x = x - 3 + i * 3
            pygame.draw.line(surface, (200, 200, 200), 
                          (line_x, beard_top + 2), 
                          (line_x - 1, beard_top + face_height//2), 
                          1)
    
    def cast_spell(self):
        if self.spell_cooldown <= 0:
            # Get magic color and power from customization, ensuring valid color format
            if 'magic_color' in self.customization and isinstance(self.customization['magic_color'], tuple):
                magic_color = self.customization['magic_color'][:3]  # Ensure only RGB components
            else:
                # Default blue magic if no valid color is found
                magic_color = (100, 150, 250)
            
            # Get magic power or use default
            magic_power = self.customization.get('magic_power', 1.0)
            
            # Create magic particles from hands
            hand_x = self.x + (self.width if self.facing_right else 0)
            hand_y = self.y + 20
            
            # Create magical particles
            particle_count = int(20 * magic_power)
            particle_speed = 4 * magic_power
            particle_size = 3 * magic_power
            
            self.assets.create_particles(
                hand_x, 
                hand_y, 
                magic_color, 
                count=particle_count, 
                speed=particle_speed, 
                size=particle_size, 
                lifetime=20
            )
            
            # Create a spell with magical effect
            magic_effect = self.assets.get_image('magic_effect')
            
            spell = {
                'x': hand_x,
                'y': hand_y,
                'speed': 10 * magic_power,  # Faster without staff
                'direction': 'left' if not self.facing_right else 'right',
                'angle': 0,
                'lifetime': 70,
                'image': magic_effect,
                'color': magic_color,
                'power': magic_power
            }
            self.spells.append(spell)
            self.spell_cooldown = self.spell_cooldown_time
    
    def take_damage(self, amount=10):
        """Take damage and become temporarily invulnerable"""
        if not self.invulnerable:
            self.health -= amount
            self.invulnerable = True
            self.invulnerable_timer = 60  # 1 second at 60 fps
            self.damage_flash = 5  # Flash for 5 frames 