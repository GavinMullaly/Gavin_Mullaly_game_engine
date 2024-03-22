# This was created by: Gavin Mullaly
# My game was created with the Help of Mr. Cozort and AI
# 3 goals are, 
# Health Bar 
# Timer system
# Speed Boost
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


# Initialize screen, clock, player, etc.


    # this is my first class which is Game, It loads the Map and sets up the game         
     # load save game data etc...   
        # Does slef.run start the game?
     # Load_Data runs the map 
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.last_coin_time = 0
        self.speed_boost_duration = 5000  # 5 seconds in milliseconds
        self.speed_boost_active = False
        self.speed_boost_start_time = 0
        
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
        self.speedboosts = pg.sprite.Group()
        self.player_speed = PLAYER_SPEED
        for row, tiles in enumerate(self.map_data):
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
    
    # In the Map.txt 1 = wall P= player and M = Mob
            
            self.timer_start = pg.time.get_ticks()
        self.timer_duration = 30000  # 1/2 minute in milliseconds

    
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
        if pg.time.get_ticks() - self.timer_start >= self.timer_duration:
            self.playing = False
        if pg.time.get_ticks() - self.last_coin_time >= 10000:  # 10 seconds in milliseconds
        # Update the timer by adding 10 seconds
         self.timer_duration += 10000
        # Update the last coin time
        self.last_coin_time = pg.time.get_ticks()  # Move this line here
        if  self.speed_boost_active:
            if pg.time.get_ticks() - self.speed_boost_start_time >= self.speed_boost_duration:
            # Speed boost expired, reset player speed
                self.player_speed = PLAYER_SPEED
            self.speed_boost_active = False
        else:
            self.player_speed = PLAYER_SPEED * 2  # Double the player speed
        hits = pg.sprite.spritecollide(self.player, self.speedboosts, True)
        for speedboost in hits:
            speedboost.apply_effect(self.player)
        hits = pg.sprite.spritecollide(self.player, self.speedboosts, True)

        if self.timer_duration > MAX_TIMER_DURATION:
            self.timer_duration = MAX_TIMER_DURATION
       
    def draw_grid(self):
            for x in range(0, WIDTH, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
            for y in range(0, WIDTH, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            if pg.time.get_ticks() - self.timer_start >= self.timer_duration:
                self.playing = False
            if pg.time.get_ticks() - self.last_coin_time >= 10:  # 10 seconds in milliseconds
            # Update the timer by adding 10 seconds
             self.timer_duration += 10
            # Update the last coin time
            
            
   
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
        self.player.draw_health_bar()
        self.draw_text(self.screen, str((self.timer_duration - (pg.time.get_ticks() - self.timer_start)) // 1000), 64, ORANGE, 29, 1)
    
        pg.display.flip()   

    # fills the screen with the correct colors
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit() 
            if event.type == pg.sprite.spritecollideany and event.sprite == self.player:
                        if isinstance(event.sprite, SpeedBoost):
                            self.activate_speed_boost()

    def collect_coin(self, coin):
        self.coins.remove(coin)  # Remove the collected coin from the group
        self.player.moneybag += 1  # Increment the player's moneybag
        self.last_coin_time = pg.time.get_ticks()  # Update the last coin time
        print("Collected a coin")
    
    def activate_speed_boost(self):
        # Activate speed boost
        self.speed_boost_active = True
        self.speed_boost_start_time = pg.time.get_ticks()
    
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
 
 
