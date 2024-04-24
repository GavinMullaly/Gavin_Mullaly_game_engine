# This file was created by Gavin Mullaly

import pygame as pg
from pygame.sprite import Group, Sprite
from settings import * 
from os import path

#SPRITESHEET = "theBell.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

class Spritesheet:
    # utility class for loading and parsing spritesheets
   # def __init__(self, filename):
        #self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image


# i imported pygame to the sprites 
# this is my Player class, The player is green he is as big as a tile
class Player(Sprite): # ths player is defined as self 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0 # the Player starts out with 0 coins 
        self.lives = 10 # The player starts out with 10 lives, everytime they player hits a mob they lose a life
   # This is my Healthbar system I created it Using AI
        #self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        #self.load_images()
        #self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0
        self.material = True
        self.jumping = False
        self.walking = False
        self.vx, self.vy = 0, 0
        self.player_speed = INITIAL_PLAYER_SPEED
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0


    
    
    def draw_health_bar(self):
        # The Health bar Calculates the width of health bar based on remaining lives the player has
        health_width = int(BAR_LENGTH * (self.lives / 10))
        #  the bar length is as big as the amount of live dived by 10, so if the player has 8 lives left the health bars size will be 8/10 
        #how big the bar is 
        bg_rect = pg.Rect(10, 10, BAR_LENGTH, BAR_HEIGHT)
        pg.draw.rect(self.game.screen, WHITE, bg_rect)

        # this code Draws remaining health
        health_rect = pg.Rect(10, 10, health_width, BAR_HEIGHT)
        pg.draw.rect(self.game.screen, RED, health_rect)
        # The health bar is red and is at the top of the screen
        
        

    # My Movement system, When pressing arrow keys or wasd the play moves up down left or right
    def get_keys(self): 
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.player_speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.player_speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.player_speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.player_speed
        if  self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    # when the player touches the wall it stops it from going through the wall
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    # My wall stop the player and mobs from going through it
    def collide_with_Mob(self, kill):
        hits = pg.sprite.spritecollide(self, self.game.mobs, kill)
        if hits:
            self.lives -=1
            print(self.lives)
            return True
        
    # when the player collides with a mob they lose 1 life
                
    

 # My Update system 
    def update(self):
        self.get_keys()
        self.draw_health_bar()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        if self.collide_with_Mob(False):
            if self.lives == -1:
                self.game.player.kill()
        # The update system checks for keys being pressed to move the player and it checks for collisions with walls and mobs
        # When the player hits the mob they lose a life
        hits = pg.sprite.spritecollide(self, self.game.coins, True)
        for hit in hits:
            if isinstance(hit, Coin):
                self.moneybag += 1
         #this makes sure the game updates when a player collects a coin
        hits = pg.sprite.spritecollide(self, self.game.coins, True)
        if hits:
                self.timer_duration += 10000  # Add 10 seconds to the timer
                if self.timer_duration > MAX_TIMER_DURATION:
                    self.timer_duration = MAX_TIMER_DURATION
                if pg.time.get_ticks() - self.last_coin_time >= 10000: 
                    self.timer_duration += 10000
            

# when the player hits a coin the Player gets + 1 coins
# Create a wall class
class Wall(Sprite):
    # initalizing class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # this is my wall class its as big as a tile in the map and is yellow
    
# Using the sytem Mr. Cozort made
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE    
    

    # this coin system creates the coin to be a tile long as the coin is orange
# My SpeedBoost class
class SpeedBoost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.speedboosts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE 
        # the speed boost is purple and is also a tile long
    def apply_effect(self, player):
        player.player_speed *= 2  # Double the player's speed
        player.speed_boost_active = True
# My mob class
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx, self.vy = MOB_SPEED, 0 
        self.x = x * TILESIZE
        self.y = y * TILESIZE
    # when the mob Collides with wall it bounces back in the opposite direction
    def collide_with_walls(self): 
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.vx *= -1
            self.rect.x = self. x
     # self.vx = -1 means it goes in the opposite direction when touching a wall
    def update(self):
         self.x += self.vx * self.game.dt
         self.y += self.vy * self.game.dt
         self.rect.x = self.x
         self.collide_with_walls()
         self.rect.y = self.y
      #   self.animate()
        # self.get_keys()
         # this makes sure the mobs update when touching a wall
   # def load_images(self):
      #  self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                              #  self.spritesheet.get_image(32,0, 32, 32)]
        
    #def animate(self):
        #now = pg.time.get_ticks()
        #if now - self.last_update > 350:
           # self.rect = self.image.get_rect()
    
            
class Finish(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.finishes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE 
    
    def Collide_With_Finish(self, next_map):
        # Method implementation...
        # Load the next map using the provided filename
        self.game.load_next_map(next_map)
        finish_hits = pg.sprite.spritecollide(self.player, self.finishes, False)
        for finish in finish_hits:
            finish.Collide_With_Finish("map_2.txt")

        
