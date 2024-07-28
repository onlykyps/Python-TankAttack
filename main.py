import arcade
from constants import *
from objects import *
from utility import *

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.setup()
       
    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player = Player("images/tank.png", TANK_SCALE)
        self.player.center_x = 100
        self.player.center_y = HEIGHT/2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        
        self.player_bullets = arcade.SpriteList()
        self.player.bullets = self.player_bullets

        self.enemy_list = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()

        self.boss_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()


        self.brick_list = arcade.SpriteList()
        self.populate_bricks()
        
        self.view_left = 0
        self.view_bottom = 0
        self.frame_count = 0
        self.game_stage = GAME_INTRO
        
        self.explosion_texture_list = []
        for i in range(50,80):
            # Files from http://www.explosiongenerator.com are numbered sequentially.
            texture_name = f"explosion/explosion{i:04d}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))
        

        arcade.set_viewport(self.view_left,
                                self.view_left + WIDTH,
                                self.view_bottom,
                                self.view_bottom + HEIGHT)


    def on_draw(self):
        """ Called automatically 60 times a second to draw objects."""
        arcade.start_render()
        if self.game_stage == GAME_INTRO:
            arcade.draw_text("Tank Attacks!", WIDTH/2, HEIGHT/2,
                            arcade.color.RED, 30, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text("Press SPACE to continue!", WIDTH/2, HEIGHT/2-100,
                            arcade.color.RED, 30, align="center", anchor_x="center", anchor_y="center")
        elif self.game_stage == GAME_PLAY:
            self.draw_everything()
            arcade.draw_text(f"Lives:{self.player.lives}", self.view_left+100, self.view_bottom+100,
                            arcade.color.RED, 30, align="center", anchor_x="center", anchor_y="center")
        elif self.game_stage == GAME_OVER:
            self.draw_everything()
            result = "You lose!" if self.player.lives == 0 else "You win!"
            arcade.draw_text(f"{result}", self.view_left+WIDTH/2, HEIGHT/2,
                            arcade.color.BLUE, 30, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text("Press SPACE to restart.", self.view_left+WIDTH/2, HEIGHT/2-100,
                            arcade.color.BLUE, 30, align="center", anchor_x="center", anchor_y="center")

        
    def draw_everything(self):
        self.player_list.draw()
        self.brick_list.draw()
        self.player_bullets.draw()
        self.enemy_list.draw()
        self.enemy_bullets.draw()
        self.boss_list.draw()
        self.explosion_list.draw()

    
    def on_update(self, delta_time):
        """ Called automatically 60 times a second to update objects.
            delta_time is time since the last time on_update was called."""
        if self.game_stage == GAME_PLAY:
            self.scroll()
            self.resolve_wall_collisions()
            self.player_list.update()
            self.resolve_all_collisions()
            self.player_bullets.update()
            self.enemy_list.update()
            self.enemy_bullets.update()
            self.boss_list.update()

            self.frame_count += 1
            # every 90 frames, create a new enemy
            if self.frame_count % 90 == 0:
                enemy = Enemy("images/enemy.png", TANK_SCALE, self.view_left)
                enemy.bullets = self.enemy_bullets
                self.enemy_list.append(enemy)
            
            # if no lives left or boss dies, game over
            if self.player.lives == 0 or len(self.boss_list) == 0:
                self.game_stage = GAME_OVER

            self.explosion_list.update()

        
    def populate_bricks(self):
        """
        Populate bricks from csv file.
        See Platformer Tutorial for tutorial on creating maps
        with Tiled editor.
        """
        map_array = get_map("maps/map.csv")
        for row_index, row in enumerate(map_array):
            for column_index, item in enumerate(row):
                if item == -1:
                    continue
                elif item == 0:
                    sprite = arcade.Sprite("images/brick.png", BRICK_SCALE)
                    sprite.left = column_index * 50
                    sprite.top = (12 - row_index) * 50
                    self.brick_list.append(sprite)
                elif item == 1:
                    boss = Boss("images/boss.png", TANK_SCALE)
                    boss.left = column_index * 50
                    boss.top = (12 - row_index) * 50
                    boss.bullets = self.enemy_bullets
                    self.boss_list.append(boss)
            
    def resolve_all_collisions(self):
        """
        Resolve all collisions:player bullets with enemies, bricks and boss,
        enemies bullets colliding with player, and player colliding with boss.
        """
        # player's bullets colliding with enemy
        for bullet in self.player_bullets:
            for boss in self.boss_list:
                if arcade.check_for_collision(bullet, boss):
                    boss.lives -= 1
                    bullet.kill() # or remove_from_sprite_lists()
                    if boss.lives == 0:
                        boss.kill() 
                        self.simulate_explosion(boss)
               
            for enemy in self.enemy_list:
                if arcade.check_for_collision(bullet, enemy):
                    bullet.kill()
                    enemy.kill()
                    self.simulate_explosion(enemy)
            # player's bullet with bricks        
            for brick in self.brick_list:
                if arcade.check_for_collision(bullet, brick):
                    bullet.kill()
            
        # enemies's bullets colliding with player and bricks
        # player is vulnerable only if he's not respawning
        if not self.player.spawning:
            for bullet in self.enemy_bullets:
                if arcade.check_for_collision(bullet, self.player):
                    bullet.kill()
                    self.player.lives -= 1
                    self.simulate_explosion(self.player)
                    self.player.respawn(self.view_left + 100, HEIGHT/2)
                for brick in self.brick_list:
                    if arcade.check_for_collision(bullet, brick):
                        bullet.kill()
                if bullet.right < self.view_left:
                    bullet.kill()
            # player colliding with enemies
            for enemy in self.enemy_list:
                if arcade.check_for_collision(enemy, self.player):
                    self.player.lives -= 1
                    self.simulate_explosion(self.player)
                    self.player.respawn(self.view_left + 100, HEIGHT/2)

            # player colliding with boss
            for boss in self.boss_list:
                if arcade.check_for_collision(boss, self.player):
                    self.player.lives -= 1
                    self.simulate_explosion(self.player)
                    self.player.respawn(self.view_left + 100, HEIGHT/2)


    def simulate_explosion(self, sprite):
        """ create Explosion object"""
        explosion = Explosion(self.explosion_texture_list)
        explosion.center_x = sprite.center_x
        explosion.center_y = sprite.center_y
        self.explosion_list.append(explosion)

    def resolve_wall_collisions(self):
        """ Resolve wall collisions. This is done from scratch.
            Or alternatively, create physics engine(PhysicsEngineSimple)
        """

        # first move in the x-direction
        self.player.center_x += self.player.change_x
        # compute collision_list
        collision_list = arcade.check_for_collision_with_list(self.player, self.brick_list)
        # if collision_list not empty:
        if collision_list:
            for brick in collision_list:
                # if moving right, set player's right to minimum of 
                # all bricks' left. 
                if self.player.change_x > 0:
                    self.player.right = min(brick.left,  
                                                self.player.right)
                # if moving left, set player's left to maximum of 
                # all bricks' right. 
                if self.player.change_x < 0:
                    self.player.left = max(brick.right,  
                                                self.player.left)

        # now move in the y-direction
        self.player.center_y += self.player.change_y
        # compute collision_list
        collision_list = arcade.check_for_collision_with_list(self.player, self.brick_list)
        # if collision_list not empty:
        if collision_list:
            for brick in collision_list:
                # if moving up, set player's top to minimum of 
                # all bricks' bottom. 
                if self.player.change_y > 0:
                    self.player.top = min(brick.bottom,  
                                                self.player.top)
                # if moving down, set player's bottom to maximum of 
                # all bricks' top. 
                if self.player.change_y < 0:
                    self.player.bottom = max(brick.top,  
                                                self.player.bottom) 
                          

    def scroll(self):
        """Scrolling"""
        changed = False
        # Scroll left
        left_bndry = self.view_left + LEFT_MARGIN
        if self.player.left < left_bndry:
            self.view_left -= left_bndry - self.player.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + WIDTH - RIGHT_MARGIN
        if self.player.right > right_bndry:
            self.view_left += self.player.right - right_bndry
            changed = True

        # If we need to scroll, go ahead and do it.
        if changed:
            arcade.set_viewport(self.view_left,
                                self.view_left + WIDTH,
                                self.view_bottom,
                                self.view_bottom + HEIGHT) 
                    
    
    def on_key_press(self, key, modifiers):
        """ Called automatically whenever a key is pressed. """
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
        elif key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        if key == arcade.key.A:
            self.player.shoot()
        if key == arcade.key.SPACE:
            if self.game_stage == GAME_INTRO:
                self.setup()
                self.game_stage = GAME_PLAY
            if self.game_stage == GAME_OVER:
                self.setup()

        
    def on_key_release(self, key, modifiers):
        """ Called automatically whenever a key is released. """    
        if key == arcade.key.LEFT:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP:
            self.player.change_y = 0
        elif key == arcade.key.DOWN:
            self.player.change_y = 0
    
def main():
    """ Main method """
    window = GameWindow(WIDTH, HEIGHT, "Tank Attacks!")
    arcade.run()


if __name__ == "__main__":
    main()




