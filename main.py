import arcade
import arcade.key

WIDTH = 800
HEIGHT = 600

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)

        self.center_x = width/2
        self.center_y = height/2

        self.change_x = 0
        self.change_y = 0
    
    def on_draw(self):
        """ Called  automatically about 60 times a second to draww objects """
        arcade.start_render()
        arcade.draw_rectangle_filled(self.center_x, self.center_y,  40, 40, arcade.color.BLUE)
        

    def on_update(self, delta_time):
        """ Called  automatically about 60 times a second to update objects """
        self.center_x += self.change_x
        self.center_y += self.change_y

    def on_key_press(self, key, modifiers):
        """ Called automatically whenever a key is pressed """

        if key == arcade.key.LEFT:
            self.change_x = -5
        if key == arcade.key.RIGHT:
            self.change_x = 5
        if key == arcade.key.UP:
            self.change_y = 5
        if key == arcade.key.DOWN:
            self.change_y = -5
    
    def on_key_release(self, key, modifiers):
        """ Called automatically whenever a key is released """

        if key == arcade.key.LEFT:
            self.change_x = 0
        if key == arcade.key.RIGHT:
            self.change_x = 0
        if key == arcade.key.UP:
            self.change_y = 0
        if key == arcade.key.DOWN:
            self.change_y = 0

    # def on_key_press(self, symbol: int, modifiers: int):
    #     """ Called automatically whenever a key is pressed """
    #     return super().on_key_press(symbol, modifiers)
    
    # def on_key_release(self, symbol: int, modifiers: int):
    #     """ Called automatically whenever a key is released """
    #     return super().on_key_release(symbol, modifiers)

def main():
    """ Main method """
    window = GameWindow(WIDTH,HEIGHT,"Basic Animation")
    arcade.run()

if __name__ == "__main__":
    main()