import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, assets, patrol_min=None, patrol_max=None, speed=1, direction=1):
        self.x = x
        self.y = y
        self.assets = assets
        self.width = 30
        self.height = 40
        self.speed = speed
        self.direction = direction  # 1 = right, -1 = left
        self.active = True
        self.death_timer = 0
        
        # Patrol boundaries
        self.patrol_min = patrol_min if patrol_min is not None else x - 100
        self.patrol_max = patrol_max if patrol_max is not None else x + 100
        
        # Animation properties
        self.frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        
        # Create enemy rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Create enemy surface
        self.create_enemy_surface()
    
    def create_enemy_surface(self):
        """Create the enemy's appearance"""
        # Create a base surface for the enemy
        self.enemy_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Evil dark goblin/imp color
        body_color = (70, 120, 50)  # Dark green
        
        # Enemy body shape
        body_points = [
            (self.width // 2, 0),                     # top
            (self.width, self.height // 3),           # right shoulder
            (self.width, self.height),                # bottom right
            (0, self.height),                         # bottom left
            (0, self.height // 3)                     # left shoulder
        ]
        pygame.draw.polygon(self.enemy_surface, body_color, body_points)
        pygame.draw.polygon(self.enemy_surface, (30, 30, 30), body_points, 1)
        
        # Add eyes (red and glowing)
        eye_y = self.height // 4
        eye_color = (220, 50, 50)  # Red
        # Left eye
        pygame.draw.circle(self.enemy_surface, eye_color, 
                         (self.width // 3, eye_y), 3)
        # Right eye
        pygame.draw.circle(self.enemy_surface, eye_color, 
                         (2 * self.width // 3, eye_y), 3)
        
        # Add glow to eyes
        for eye_x in [self.width // 3, 2 * self.width // 3]:
            glow_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 100, 100, 100), (4, 4), 4)
            self.enemy_surface.blit(glow_surf, (eye_x - 4, eye_y - 4))
        
        # Add teeth/mouth
        teeth_y = self.height // 2
        # Evil smile
        pygame.draw.arc(self.enemy_surface, (200, 200, 200), 
                      (self.width // 4, teeth_y - 3, self.width // 2, 10), 
                      0, 3.14, 2)
        
        # Add pointy teeth
        for i in range(3):
            tooth_x = self.width // 4 + i * self.width // 8
            pygame.draw.line(self.enemy_surface, (200, 200, 200), 
                          (tooth_x, teeth_y), (tooth_x, teeth_y + 5), 2)
        
        # Add spikes on back
        for i in range(3):
            spike_x = self.width // 4 + i * self.width // 4
            spike_height = random.randint(5, 8)
            pygame.draw.line(self.enemy_surface, (30, 80, 30), 
                          (spike_x, 5), (spike_x, 5 - spike_height), 2)
        
        # Create flipped version
        self.enemy_surface_flipped = pygame.transform.flip(self.enemy_surface, True, False)
        
        # Death surface (X eyes)
        self.death_surface = self.enemy_surface.copy()
        # X eyes
        for eye_x in [self.width // 3, 2 * self.width // 3]:
            pygame.draw.line(self.death_surface, (0, 0, 0), 
                          (eye_x - 3, eye_y - 3), (eye_x + 3, eye_y + 3), 2)
            pygame.draw.line(self.death_surface, (0, 0, 0), 
                          (eye_x - 3, eye_y + 3), (eye_x + 3, eye_y - 3), 2)
        
        # Death surface flipped
        self.death_surface_flipped = pygame.transform.flip(self.death_surface, True, False)
    
    def update(self):
        """Update enemy position and animation"""
        if not self.active:
            # Death animation
            self.death_timer += 1
            if self.death_timer > 60:  # 1 second at 60 fps
                # After death timer, remove enemy
                self.active = False
            return
        
        # Move enemy based on direction
        self.x += self.speed * self.direction
        
        # Check patrol boundaries
        if self.x <= self.patrol_min:
            self.x = self.patrol_min
            self.direction = 1  # Switch direction to right
        elif self.x >= self.patrol_max - self.width:
            self.x = self.patrol_max - self.width
            self.direction = -1  # Switch direction to left
        
        # Update rect position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Animation
        self.animation_timer += self.speed * 0.1
        if self.animation_timer >= 1:
            self.frame = (self.frame + 1) % 4
            self.animation_timer = 0
    
    def draw(self, surface):
        """Draw the enemy on the screen"""
        # Apply a "bobbing" effect based on animation frame
        bob_offset = math.sin(self.frame * 0.5) * 2
        
        # Choose surface based on direction and alive/dead state
        if self.death_timer > 0:
            # Death animation - rotate and fade
            if self.direction > 0:
                enemy_surf = self.death_surface
            else:
                enemy_surf = self.death_surface_flipped
                
            # Rotate based on death timer
            angle = min(90, self.death_timer * 3)
            enemy_surf = pygame.transform.rotate(enemy_surf, angle)
            
            # Fade out
            alpha = max(0, 255 - self.death_timer * 4)
            enemy_surf.set_alpha(alpha)
            
            # Calculate new position after rotation
            rot_rect = enemy_surf.get_rect(center=self.rect.center)
            surface.blit(enemy_surf, rot_rect.topleft)
        else:
            # Normal animation
            if self.direction > 0:
                surface.blit(self.enemy_surface, (self.x, self.y + bob_offset))
            else:
                surface.blit(self.enemy_surface_flipped, (self.x, self.y + bob_offset))
    
    def kill(self):
        """Kill the enemy"""
        if self.active and self.death_timer == 0:
            self.death_timer = 1  # Start death animation
            return True
        return False 