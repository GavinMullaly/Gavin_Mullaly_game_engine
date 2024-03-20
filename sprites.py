# This file was created by Gavin Mullaly

import pygame as pg
from pygame.sprite import Sprite
from settings import * 

# Player is capatilized

# create a Player class

# create a Wall class

# Creating a player class
# this is my Player class, The player is green he is as big as a tile
class Player(Sprite):
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
        self.moneybag = 0
        self.lives = 10
   
    def draw_health_bar(self):
        if self.lives < 0:
            self.lives = 10
        bar_width = int(BAR_LENGTH * (self.lives / 10))
        bar_rect = pg.Rect(10, 10, bar_width, BAR_HEIGHT)
        outline_rect = pg.Rect(10, 10, BAR_LENGTH, BAR_HEIGHT)
        pg.draw.rect(self.game.screen, RED, bar_rect)
        pg.draw.rect(self.game.screen, WHITE, outline_rect, 2)
    
    def draw_health_bar(self):
        # Calculate width of health bar based on remaining lives
        health_width = int(BAR_LENGTH * (self.lives / 10))
        
        # Draw background of health bar
        bg_rect = pg.Rect(10, 10, BAR_LENGTH, BAR_HEIGHT)
        pg.draw.rect(self.game.screen, WHITE, bg_rect)

        # Draw remaining health
        health_rect = pg.Rect(10, 10, health_width, BAR_HEIGHT)
        pg.draw.rect(self.game.screen, RED, health_rect)
        
        
        
    # Changed movment 
    # def move(self, dx=0, dy=0):
       #  self.x += dx
        # self.y += dy
    # My Movement system, When pressing arrow keys or wasd the play moves up down left or right
    def get_keys(self): 
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
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
    # My Mob collision is not finished yet, goal is player takes damage when hit a mob
    def collide_with_Mob(self, kill):
        hits = pg.sprite.spritecollide(self, self.game.mobs, kill)
        if hits:
            self.lives -=1
            print(self.lives)
            return True
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
    

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
        
        # When the player hits the mob the game ends
        hits = pg.sprite.spritecollide(self, self.game.coins, True)
        for hit in hits:
            if isinstance(hit, Coin):
                self.moneybag += 1
        
    # When the player hits the mob the game ends
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
        self.collide_with_group(self.game.coins, True)

        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")
# when the player hits a coin the Player gest + 1 coins
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
    
    def update(self):
         self.x += self.vx * self.game.dt
         self.y += self.vy * self.game.dt
         self.rect.x = self.x
         self.collide_with_walls()
         self.rect.y = self.y
