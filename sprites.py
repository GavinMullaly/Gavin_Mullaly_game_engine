# This file was created by Gavin Mullaly

import pygame as pg
from pygame.sprite import Group, Sprite
from settings import * 

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
        self.player_speed = INITIAL_PLAYER_SPEED
    
    
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
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                # when a player collides with a coin the add 1 coin to their money bad
    

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
        # this makes sure the game updates when a player collects a coin
        
            

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
         # this makes sure the mobs update when touching a wall
