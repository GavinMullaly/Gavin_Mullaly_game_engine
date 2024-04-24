# This was created by: Gavin Mullaly
# My game was created with the Help of Mr. Cozort and AI
# 3 goals are, 
# Health Bar 
# Timer system
# Speed Boost
# My beta goal is to add 2 more levels with a boss and end screenx
import pygame as pg 
import sys
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep
# How does def_load_data work and why do we need it in out code?

# Five things that make a game Good is, 1# its enjoyable and fun 2# its not to easy, 
# 3# its not to hard 4# There is a pourpose to the game and lastly 5# Everything works 


# I imported PyGame to my Game same with my other files that include Settings and Sprites

# data types; int, string, loat, boolean

    # This is my class game, def __init__(self): it intializes the game when it stars
class Game:
    def __init__(self):  
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # self.screen displays the width and height of the game 
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock() # Creates a clock that the game uses to count the frames per secound
        pg.key.set_repeat(500, 100)
        self.load_data() 
        self.last_coin_time = 0
        self.speed_boost_duration = 5000  # 5 seconds in milliseconds
        self.speed_boost_active = False # makes sure that the speed boost ins't active at the start
        self.speed_boost_start_time = 0
        self.current_map = "map_1.txt"
    
    
    def activate_speed_boost(self):
        # Activate speed boost
        self.speed_boost_active = True
        self.speed_boost_start_time = pg.time.get_ticks()
        
    
    def load_data(self): # this loads the game and the map
        game_folder = path.dirname(__file__) 
        self.map_data = []
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        with open(path.join(game_folder,  'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
                print(self.map_data)
                print(enumerate(self.map_data)) #this creates the map

    def new(self):
        # initiats all variables, setup groups, instantiate class
        self.all_sprites = pg.sprite.Group() #this group creates all sprite groups
        self.walls = pg.sprite.Group() # these are all my sprite groups
        self.mobs = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.finishes=pg.sprite.Group()
        self.speedboosts = pg.sprite.Group()
        self.player_speed = PLAYER_SPEED # this line creates the players speed attribute
        for row, tiles in enumerate(self.map_data): # this code creates corresponding tiles from the map text
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                     Mob(self, col, row)
                if tile == 'C':
                     Coin(self, col, row)
                if tile == 'S':
                    SpeedBoost(self, col, row)
                if tile == 'F':
                    Finish(self,col, row)
    
    # In the Map.txt 1 = wall P= player and M = Mob
            
            self.timer_start = pg.time.get_ticks() 
        self.timer_duration = 60000  # 1/2 minute in milliseconds
        # this is the amount of time I have to complete the game 30 secs
    
    def run(self): # this makes the game continue to run
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            # when I press the quit button the game ends
    def quit(self): 
        pg.quit()
        sys.exit()
# When I press the quit button the game ends
    
    def update(self): # def update, updates the all the games sprites 
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.speedboosts, True)
        # I created my timer system and speed boost using AI 
        if hits:
            for speedboost in hits:
                speedboost.apply_effect(self.player)
        if hits:
            self.activate_speed_boost()
        if self.speed_boost_active:
            self.player_speed = PLAYER_SPEED * 2  # Double player speed
        else:
            self.player_speed = PLAYER_SPEED
        finish_hits = pg.sprite.spritecollide(self.player, self.finishes, False)
        for finish in finish_hits:
            finish.Collide_With_Finish(self, "map_2.txt")
        
        
        
       # thise code draws the x axis and y axis 
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        if pg.time.get_ticks() - self.timer_start >= self.timer_duration:
            self.playing = False
        if pg.time.get_ticks() - self.last_coin_time >= 10000: 
            self.timer_duration += 10
    # this adds 10 secs to the timer when a coin is collected

             # this adds 10 secs to the timer when a coin is collected
            
        # this code creates the arial font for my text
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)
        
        # this displays the color and spirtes on the map
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, ORANGE, 1,  1) #this is where it displays my coin collector
        self.player.draw_health_bar()
        self.draw_text(self.screen, str((self.timer_duration - (pg.time.get_ticks() - self.timer_start)) // 1000), 64, ORANGE, 29, 1) #This is where it displays my time text
    
        pg.display.flip()   

    # this makes sure events occur 
    def events(self):
        coin_hits = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit() 
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    coin_hits = pg.sprite.spritecollide(self.player, self.coins, True)
                if coin_hits:  
                    for coin in coin_hits:
                        self.collect_coin(coin)
                    else:
                         speedboost_hits = pg.sprite.spritecollide(self.player, self.speedboosts, True)
                    if speedboost_hits:
                            self.activate_speed_boost()
                  # when player hits coin and speedboost it activtes the functions
       # when i collect coins it adds to the coin counter
    def activate_speed_boost(self):
        # when the speed boost is active it runs the function
        self.speed_boost_active = True
        self.speed_boost_start_time = pg.time.get_ticks()
    
    def show_start_screen(self):
     pass

    def show_go_screen(self):
     pass
    

# I have instantiated the Game
def load_next_map(self, map_2):
        # Load the next map from the specified filename
        self.current_map =  map.txt
        with open(map.txt, 'rt') as f:
            self.map_data = []
            for line in f:
                self.map_data.append(line.strip())

        # Clear existing sprite groups
        self.all_sprites.empty()
        self.walls.empty()
        self.mobs.empty()
        self.coins.empty()
        self.speedboosts.empty()
        self.finishes.empty()


        # Create new sprites based on the loaded map data
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)
                elif tile == 'C':
                    Coin(self, col, row)
                elif tile == 'S':
                    SpeedBoost(self, col, row)
                elif tile == 'F':
                    Finish(self, col, row)







g = Game()
while True:
    g.new()
    g.run()
    # g.show_go_screen
     
# I told the game to run
 
 
