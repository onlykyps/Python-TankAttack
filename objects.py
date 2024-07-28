import arcade
from constants import *
import random
import math

class Player(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.lives = 3
        self.bullets = None
        self.spawning = 0
    def shoot(self):
        bullet = arcade.Sprite("images/bullet_blue.png", BULLET_SCALE)
        bullet.change_x = BULLET_SPEED
        bullet.center_y = self.center_y
        bullet.left = self.right
        self.bullets.append(bullet)
    def respawn(self, x_pos, y_pos):
        """ 
        While respawning, player is not vulnerable to attack
        """
        self.spawning = 1
        self.center_x = x_pos
        self.center_y = y_pos
    def update(self):
        if self.spawning != 0:
            self.spawning += 2
            self.alpha = self.spawning # alpha is transparency(0 is invisible, 255 completely opaque)
            if self.spawning > 250:
                self.spawning = 0
                self.alpha = 255

class Enemy(arcade.Sprite):
    def __init__(self, filename, scale, view_left):
        super().__init__(filename, scale)
        self.center_x = view_left + WIDTH + 100
        self.center_y = random.randrange(100, HEIGHT - 100)
        self.angle = 180
        self.bullets = None
        self.change_x = ENEMY_SPEED
    def shoot(self):
        """Shoots randomly, returns True if character did shoot."""
        # shoots at random intervals(on average every 1.5 seconds)
        if random.randrange(90) == 0:
            bullet = arcade.Sprite("images/bullet_dark.png", BULLET_SCALE)
            bullet.change_x = ENEMY_BULLET_SPEED
            bullet.center_y = self.center_y
            bullet.right = self.left
            bullet.angle = self.angle
            self.bullets.append(bullet)
            return True
        return False


class Boss(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.bullets = None
        self.lives = 6
        self.change_y = 3
    def update(self):
        super().update()
        if self.center_y<100 or self.center_y>(HEIGHT-100):
            self.change_y *= -1
    def aim(self, target):
        # sets angle to be in direction of target
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        self.angle = math.degrees(math.atan2(dy, dx))
    def shoot(self, target):
        self.aim(target)
        # shoots at random intervals(on average every 2 seconds)
        # bullet faces same direction as Boss
        if random.randrange(120) == 0:
            bullet = arcade.Sprite("images/bullet_dark.png", BULLET_SCALE)
            bullet.angle = self.angle
            bullet.change_x = BOSS_BULLET_SPEED*math.cos(math.radians(self.angle))
            bullet.change_y = BOSS_BULLET_SPEED*math.sin(math.radians(self.angle))
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y
            self.bullets.append(bullet)


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """
    def __init__(self, texture_list):
        super().__init__("explosion/explosion0050.png")
        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list
    def update(self):
        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()
        
