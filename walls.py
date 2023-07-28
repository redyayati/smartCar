from pygame.math import Vector2
import pygame as pg


class Wall():
    def __init__(self,x1,y1,x2,y2) : 
        self.a = Vector2(x1,y1)
        self.b = Vector2(x2,y2)
    def midPoint(self) : 
        return Vector2((self.a.x+self.b.x)*.5 , (self.a.y+self.b.y)*.5)
    def show(self,screen) : 
        col = 100,100,100
        pg.draw.line(screen , (col) , (self.a.x,self.a.y),(self.b.x,self.b.y),2)
        
    