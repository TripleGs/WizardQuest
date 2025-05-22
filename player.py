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
        
        # Attack properties
        self.attack_cooldown = 0
        self.attack_cooldown_time = 30
        self.attacks = []
        
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
            
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Update invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.damage_flash = 0
        
        # Update damage flash
        if self.damage_flash > 0:
            self.damage_flash -= 1
        
        # Update attacks
        for attack in self.attacks[:]:
            # Check if attack has homing capability
            if attack.get('homing', False) and 'target' in attack:
                target = attack['target']
                
                # Only home in if target is still active
                if target.active and target.death_timer == 0:
                    # Get target's current position
                    target_x = target.x + target.width//2
                    target_y = target.y + target.height//2
                    
                    # Calculate angle to target
                    attack_center_x = attack['x'] + attack['width']//2
                    attack_center_y = attack['y'] + attack['height']//2
                    dx = target_x - attack_center_x
                    dy = target_y - attack_center_y
                    angle = math.atan2(dy, dx)
                    
                    # Calculate distance to target for debugging
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    # Update attack angle with some lerping for smoother turning
                    current_angle = attack.get('angle', angle)
                    # Adjust angle towards target (homing effect)
                    angle_diff = angle - current_angle
                    # Normalize angle difference to -pi to pi
                    while angle_diff > math.pi:
                        angle_diff -= 2 * math.pi
                    while angle_diff < -math.pi:
                        angle_diff += 2 * math.pi
                    # Apply gradual turning - increase turning speed for better tracking
                    new_angle = current_angle + angle_diff * 0.3  # Increased turning speed
                    attack['angle'] = new_angle
                    
                    # Print tracking info for debugging
                    print(f"Tracking: dist={distance:.1f}, angle={math.degrees(new_angle):.1f}°")
                    
                    # Move attack based on angle
                    move_speed = attack['speed']
                    attack['x'] += math.cos(new_angle) * move_speed
                    attack['y'] += math.sin(new_angle) * move_speed
                    
                    # Update attack rect after moving for collision detection
                    attack_rect = pygame.Rect(attack['x'], attack['y'], attack['width'], attack['height'])
                    attack['rect'] = attack_rect
                    
                    # Check for collision with target
                    if attack_rect.colliderect(target.rect):
                        # Kill the enemy
                        target.kill()
                        print(f"Enemy hit and killed!")
                        
                        # Create explosion at enemy position
                        if 'color' in attack and isinstance(attack['color'], tuple) and len(attack['color']) >= 3:
                            explosion_color = attack['color'][:3]
                        else:
                            explosion_color = (150, 100, 250)
                            
                        self.assets.create_particles(
                            target.rect.centerx,
                            target.rect.centery,
                            explosion_color,
                            count=50,
                            speed=6,
                            size=5,
                            lifetime=30
                        )
                        
                        # Remove the attack
                        self.attacks.remove(attack)
                        continue
                else:
                    # Target is no longer active, convert to standard attack
                    print("Target lost - converting to standard attack")
                    attack['homing'] = False
                    
                    # Set direction based on last known angle
                    if 'angle' in attack:
                        angle_degrees = math.degrees(attack['angle']) % 360
                        if angle_degrees < 90 or angle_degrees > 270:
                            attack['direction'] = 'right'
                        else:
                            attack['direction'] = 'left'
                    
                    # Move in that direction
                    attack['x'] += attack['speed'] * (-1 if attack['direction'] == 'left' else 1)
            else:
                # Standard non-homing movement
                attack['x'] += attack['speed'] * (-1 if attack['direction'] == 'left' else 1)
            
            attack['lifetime'] -= 1
            
            # Ensure attack color is valid
            if 'color' in attack and isinstance(attack['color'], tuple) and len(attack['color']) >= 3:
                attack_color = attack['color'][:3]  # Use only RGB components
            else:
                attack_color = (150, 100, 250)  # Default purple if invalid
            
            # Create trail particles
            if random.random() < 0.3:
                self.assets.create_particles(
                    attack['x'] + attack['width']//2, 
                    attack['y'] + attack['height']//2, 
                    attack_color, 
                    count=3,
                    speed=1, 
                    size=2, 
                    lifetime=10
                )
            
            # Remove if out of screen or lifetime ended
            if (attack['x'] < -40 or 
                attack['x'] > self.settings.window_width + 40 or 
                attack['y'] < -40 or
                attack['y'] > self.settings.window_height + 40 or
                attack['lifetime'] <= 0):
                self.attacks.remove(attack)
                
                # Create explosion particles when attack expires
                self.assets.create_particles(
                    attack['x'] + attack['width']//2, 
                    attack['y'] + attack['height']//2, 
                    attack_color, 
                    count=15,
                    speed=3,
                    size=3, 
                    lifetime=20
                )
        
        # Update spells
        for spell in self.spells[:]:
            spell['x'] += spell['speed'] * (-1 if spell['direction'] == 'left' else 1)
            spell['y'] += math.sin(spell['angle']) * 2
            spell['angle'] += 0.1
            spell['lifetime'] -= 1
            
            # Ensure spell color is valid
            if 'color' in spell and isinstance(spell['color'], tuple) and len(spell['color']) >= 3:
                spell_color = spell['color'][:3]  # Use only RGB components
            else:
                spell_color = (150, 100, 250)  # Default purple if invalid
            
            spell_power = spell.get('power', 1.0)
            
            # Create trail particles
            if random.random() < 0.3:
                self.assets.create_particles(
                    spell['x'] + 10, 
                    spell['y'] + 10, 
                    spell_color, 
                    count=int(2 * spell_power),  # More particles for powerful spells
                    speed=1, 
                    size=2, 
                    lifetime=10
                )
            
            # Remove if out of screen or lifetime ended
            if (spell['x'] < -40 or 
                spell['x'] > self.settings.window_width + 40 or 
                spell['lifetime'] <= 0):
                self.spells.remove(spell)
                
                # Create explosion particles when spell expires
                self.assets.create_particles(
                    spell['x'] + 10, 
                    spell['y'] + 10, 
                    spell_color, 
                    count=int(20 * spell_power),  # More explosion for powerful spells
                    speed=4 * spell_power,  # Faster particles for powerful spells
                    size=3, 
                    lifetime=20
                )
    
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
    
    def draw(self, surface):
        # Draw spells
        for spell in self.spells:
            if spell['image']:
                # Scale the effect based on power
                scale_factor = spell.get('power', 1.0)
                scaled_image = pygame.transform.scale(
                    spell['image'], 
                    (int(spell['image'].get_width() * scale_factor), 
                    int(spell['image'].get_height() * scale_factor))
                )
                surface.blit(scaled_image, (spell['x'], spell['y']))
            else:
                # Ensure we have a valid color for the spell
                if 'color' in spell and isinstance(spell['color'], tuple) and len(spell['color']) >= 3:
                    spell_color = spell['color'][:3]  # Use only RGB components
                else:
                    # Default to purple if no valid color
                    spell_color = (150, 100, 250)
                    
                # Scale size based on power
                size = int(20 * spell.get('power', 1.0))
                
                pygame.draw.rect(surface, spell_color, 
                              pygame.Rect(spell['x'], spell['y'], size, size))
                pygame.draw.rect(surface, (100, 50, 200), 
                              pygame.Rect(spell['x'], spell['y'], size, size), 2)
        
        # Draw attacks (directed bolts)
        for attack in self.attacks:
            # Ensure we have a valid color
            if 'color' in attack and isinstance(attack['color'], tuple) and len(attack['color']) >= 3:
                attack_color = attack['color'][:3]  # Use only RGB components
            else:
                # Default to blue if no valid color
                attack_color = (100, 150, 250)
            
            # Create attack bolt shape
            bolt_rect = pygame.Rect(attack['x'], attack['y'], attack['width'], attack['height'])
            
            # Check if this is a homing attack
            if attack.get('homing', False) and 'angle' in attack:
                # For homing attacks, rotate the bolt to match its trajectory
                angle_degrees = math.degrees(attack['angle'])
                
                # Create a surface for the rotated bolt
                bolt_surf = pygame.Surface((attack['width'], attack['height']), pygame.SRCALPHA)
                
                # Draw the bolt on the surface
                pygame.draw.rect(bolt_surf, attack_color, 
                              pygame.Rect(0, 0, attack['width'], attack['height']), 
                              border_radius=5)
                pygame.draw.rect(bolt_surf, (255, 255, 255), 
                              pygame.Rect(0, 0, attack['width'], attack['height']), 
                              2, border_radius=5)
                
                # Add directional effect at front of bolt (pointy end in direction of travel)
                points = [
                    (attack['width'] - 5, attack['height'] // 2),  # tip
                    (attack['width'] - 15, attack['height'] // 4),  # top back
                    (attack['width'] - 15, 3 * attack['height'] // 4)  # bottom back
                ]
                pygame.draw.polygon(bolt_surf, attack_color, points)
                
                # Rotate the bolt to match its trajectory
                rotated_bolt = pygame.transform.rotate(bolt_surf, -angle_degrees)
                
                # Get the center of the bolt for positioning
                bolt_center = bolt_rect.center
                rotated_rect = rotated_bolt.get_rect(center=bolt_center)
                
                # Draw the rotated bolt
                surface.blit(rotated_bolt, rotated_rect.topleft)
                
                # Update rect for collision detection
                attack['rect'] = rotated_rect
                
                # Add glowing trail effect
                trail_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
                for i in range(3):
                    radius = 8 - i*2
                    alpha = 150 - i*40
                    pygame.draw.circle(trail_surf, (*attack_color, alpha), (10, 10), radius)
                
                # Position the trail based on angle
                trail_x = attack['x'] + attack['width']//2 - math.cos(attack['angle']) * attack['width']/2
                trail_y = attack['y'] + attack['height']//2 - math.sin(attack['angle']) * attack['height']/2
                surface.blit(trail_surf, (trail_x-10, trail_y-10))
                
            else:
                # For standard non-homing attacks
                # Draw main bolt with glow effect
                pygame.draw.rect(surface, attack_color, bolt_rect, border_radius=5)
                pygame.draw.rect(surface, (255, 255, 255), bolt_rect, 2, border_radius=5)
                
                # Add directional effect (pointed end)
                if attack['direction'] == 'right':
                    points = [
                        (bolt_rect.right, bolt_rect.centery),
                        (bolt_rect.right - 10, bolt_rect.top),
                        (bolt_rect.right - 10, bolt_rect.bottom)
                    ]
                else:
                    points = [
                        (bolt_rect.left, bolt_rect.centery),
                        (bolt_rect.left + 10, bolt_rect.top),
                        (bolt_rect.left + 10, bolt_rect.bottom)
                    ]
                pygame.draw.polygon(surface, attack_color, points)
                
                # Update rect for collision detection
                attack['rect'] = bolt_rect
                
                # Add a glowing trail effect
                trail_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
                for i in range(3):
                    radius = 8 - i*2
                    alpha = 150 - i*40
                    pygame.draw.circle(trail_surf, (*attack_color, alpha), (10, 10), radius)
                
                # Position the trail based on direction
                offset = 10 if attack['direction'] == 'right' else -10
                trail_x = attack['x'] + (0 if attack['direction'] == 'left' else attack['width']) - offset
                trail_y = attack['y'] + attack['height']//2
                surface.blit(trail_surf, (trail_x-10, trail_y-10))
        
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
    
    def cast_attack(self, enemies):
        """Cast a directed attack that auto-targets the closest enemy"""
        if self.attack_cooldown <= 0:
            # Get magic color and power from customization, ensuring valid color format
            if 'magic_color' in self.customization and isinstance(self.customization['magic_color'], tuple):
                magic_color = self.customization['magic_color'][:3]  # Ensure only RGB components
            else:
                # Default blue magic if no valid color is found
                magic_color = (100, 150, 250)
            
            # Get magic power or use default
            magic_power = self.customization.get('magic_power', 1.0)
            
            # Create attack from hand
            hand_x = self.x + (self.width if self.facing_right else 0)
            hand_y = self.y + 20
            player_center_x = self.x + self.width // 2
            player_center_y = self.y + self.height // 2
            
            # Create a larger, faster attack bolt
            attack_width = 30
            attack_height = 15
            
            # Only look for enemies if there are any
            if enemies and len(enemies) > 0:
                # Find the closest active enemy
                closest_enemy = None
                min_distance = float('inf')
                
                for enemy in enemies:
                    if enemy.active and enemy.death_timer == 0:  # Only target active enemies not in death animation
                        enemy_center_x = enemy.x + enemy.width // 2
                        enemy_center_y = enemy.y + enemy.height // 2
                        
                        # Calculate distance to this enemy
                        dx = enemy_center_x - player_center_x
                        dy = enemy_center_y - player_center_y
                        distance = math.sqrt(dx * dx + dy * dy)  # Actual distance for accuracy
                        
                        if distance < min_distance:
                            min_distance = distance
                            closest_enemy = enemy
                
                # If found a target, determine direction and adjust facing
                if closest_enemy:
                    # Get enemy center position
                    enemy_center_x = closest_enemy.x + closest_enemy.width // 2
                    enemy_center_y = closest_enemy.y + closest_enemy.height // 2
                    
                    # Determine direction to enemy
                    to_right = enemy_center_x > player_center_x
                    self.facing_right = to_right  # Update facing direction to face the enemy
                    
                    # Calculate angle to enemy for homing effect
                    dx = enemy_center_x - player_center_x
                    dy = enemy_center_y - player_center_y
                    angle = math.atan2(dy, dx)
                    
                    # Print debugging info
                    print(f"Targeting enemy at ({enemy_center_x}, {enemy_center_y}) from ({player_center_x}, {player_center_y})")
                    print(f"Angle: {math.degrees(angle):.1f} degrees, Distance: {min_distance:.1f}")
                    
                    # Adjust start position to be in front of the player
                    start_x = player_center_x + (15 if to_right else -15) - attack_width//2
                    start_y = player_center_y - attack_height//2
                    
                    # Create attack object with homing info
                    attack = {
                        'x': start_x,
                        'y': start_y,
                        'width': attack_width,
                        'height': attack_height,
                        'rect': pygame.Rect(start_x, start_y, attack_width, attack_height),
                        'speed': 10 * magic_power,  # Slightly slower for better tracking
                        'direction': 'right' if to_right else 'left',
                        'lifetime': 60,
                        'color': magic_color,
                        'power': magic_power,
                        'homing': True,
                        'target': closest_enemy,
                        'angle': angle
                    }
                    
                    # Check for immediate hit if enemy is very close
                    if min_distance < 80:  # Close range instant hit
                        closest_enemy.kill()
                        
                        # Create explosion at enemy position
                        self.assets.create_particles(
                            closest_enemy.rect.centerx,
                            closest_enemy.rect.centery,
                            magic_color,
                            count=50,
                            speed=6,
                            size=5,
                            lifetime=30
                        )
                        
                        # Don't add the attack to the list if we already hit the enemy
                        self.attack_cooldown = self.attack_cooldown_time
                        return
                else:
                    # No target found, shoot in current facing direction
                    print("No active enemies found to target")
                    attack = self._create_standard_attack(player_center_x, player_center_y, hand_y, attack_width, attack_height, magic_color, magic_power)
            else:
                # No enemies at all, shoot in current facing direction
                print("No enemies to target")
                attack = self._create_standard_attack(player_center_x, player_center_y, hand_y, attack_width, attack_height, magic_color, magic_power)
            
            # Create initial burst particles
            self.assets.create_particles(
                hand_x, 
                hand_y, 
                magic_color, 
                count=int(30 * magic_power),
                speed=5 * magic_power,
                size=4 * magic_power,
                lifetime=15
            )
            
            self.attacks.append(attack)
            self.attack_cooldown = self.attack_cooldown_time
    
    def _create_standard_attack(self, player_center_x, player_center_y, hand_y, attack_width, attack_height, magic_color, magic_power):
        """Helper method to create a standard non-homing attack"""
        # Adjust start position to be in front of the player
        start_x = player_center_x + (15 if self.facing_right else -15) - attack_width//2
        start_y = hand_y - attack_height//2
        
        return {
            'x': start_x,
            'y': start_y,
            'width': attack_width,
            'height': attack_height,
            'rect': pygame.Rect(start_x, start_y, attack_width, attack_height),
            'speed': 15 * magic_power,
            'direction': 'right' if self.facing_right else 'left',
            'lifetime': 60,
            'color': magic_color,
            'power': magic_power,
            'homing': False
        }
    
    def take_damage(self, amount=20):
        """Take damage from enemies"""
        if not self.invulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable = True
            self.invulnerable_timer = 60  # 1 second at 60 fps
            self.damage_flash = 10  # Flash red for 10 frames
            
            # Create damage particles
            self.assets.create_particles(
                self.rect.centerx,
                self.rect.centery,
                (200, 50, 50),  # Red particles
                count=30,
                speed=4,
                size=4,
                lifetime=20
            ) 