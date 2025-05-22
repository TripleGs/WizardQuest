import pygame
import random
import math

class ParticleSystem:
    def __init__(self, assets):
        self.assets = assets
        self.particles = []
    
    def create_magic_particles(self, x, y, color, count=1):
        """Create magical particle effects"""
        for _ in range(count):
            # Random position near the specified point
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            
            # Generate a particle with proper color
            particle = {
                'x': x + offset_x,
                'y': y + offset_y,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-1.5, -0.5),  # Particles float upward
                'radius': random.uniform(2, 4),
                'life': random.randint(40, 80),
                'max_life': 80,
                'color': color
            }
            
            self.particles.append(particle)
    
    def create_color_change_particles(self, x, y, color, count=10):
        """Create particles when changing robe color"""
        for _ in range(count):
            offset_x = random.uniform(-30, 30)
            offset_y = random.uniform(-50, 50)
            
            self.particles.append({
                'x': x + offset_x,
                'y': y + offset_y,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, 0),
                'radius': random.uniform(2, 4),
                'life': random.randint(30, 60),
                'max_life': 60,
                'color': color
            })
    
    def create_selection_particles(self, button_rect, color):
        """Create particles when clicking a button"""
        center_x = button_rect.centerx
        center_y = button_rect.centery
        
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            distance = random.uniform(5, 15)
            
            self.particles.append({
                'x': center_x + math.cos(angle) * distance,
                'y': center_y + math.sin(angle) * distance,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'radius': random.uniform(1, 3),
                'life': random.randint(20, 40),
                'max_life': 40,
                'color': color
            })
    
    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            # Move particles
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Apply slight upward acceleration for floating effect
            particle['vy'] -= 0.03
            
            # Decrease lifetime
            particle['life'] -= 1
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        """Draw all particles with proper blending"""
        for particle in self.particles:
            # Calculate opacity based on remaining life
            life_ratio = particle['life'] / particle['max_life']
            
            # Get base color
            color = particle['color']
            
            if life_ratio > 0.7:
                # New particles: original color
                draw_color = color
            elif life_ratio > 0.4:
                # Middle-aged particles: slightly faded
                draw_color = self._blend_colors(color, (255, 255, 255), 0.3)
            else:
                # Old particles: more transparent and faded
                draw_color = self._blend_colors(color, (255, 255, 255), 0.6)
            
            # Size fades out
            radius = particle['radius'] * life_ratio
            
            # Only draw if radius is visible
            if radius >= 1:
                # Draw the particle
                pygame.draw.circle(screen, draw_color, (int(particle['x']), int(particle['y'])), radius)
                
                # Add a glow for magical effect
                if life_ratio > 0.3:
                    glow_radius = radius * 1.5
                    pygame.draw.circle(screen, draw_color, (int(particle['x']), int(particle['y'])), glow_radius, 1)
    
    def _blend_colors(self, color1, color2, ratio):
        """Blend two colors with a ratio (0-1)"""
        return (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio)
        ) 