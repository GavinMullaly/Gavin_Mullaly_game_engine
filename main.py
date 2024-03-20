# This was created by: Gavin Mullaly
# my first source control edit 
# import necessary modules
# 3 goals are, 
# Large Maze 
# Mob thats bounces of the wall
# coin system
import pygame as pg 
import sys
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep
# I imported PyGame to my Game 

# data types; int, string, loat, boolean
# Making my Class Game, Creating the game and displaying the map on PyGame 
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        
# this is my first class which is Game, It loads the Map and sets up the game         
     # load save game data etc...   
        # Does slef.run start the game?
     # Load_Data runs the map 
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder,  'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
                print(self.map_data)
                print(enumerate(self.map_data))

    def new(self):
        # initiats all variables, setup groups, instantiate class
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.coins = pg.sprite.Group()
     # these are all my classes 
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                  #print(row)
                  #print(tiles)
                  # Map system
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
    # In the Map.txt 1 = wall P= player and M = Mob
    
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
            

    def quit(self):
        pg.quit()
        sys.exit()
# When I press the quit button the game ends
    def update(self):
        self.all_sprites.update()
      # System that defins the height and width of the map
    def draw_grid(self):
            for x in range(0, WIDTH, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
            for y in range(0, WIDTH, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
   
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)
        

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, ORANGE, 1,  1)
    
    

        
    
        
        pg.display.flip()   

    # fills the screen with the correct colors
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit() 
    
    def show_start_screen(self):
     pass

    def show_go_screen(self):
     pass
    

# I have instantiated the Game
g = Game()
while True:
    g.new()
    g.run()
    # g.show_go_screen
     
# I told the game to run
 
 
