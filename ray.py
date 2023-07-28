import pygame as pg
from pygame.math import Vector2
import pygame.gfxdraw

class Ray():
    def __init__(self,pos,deg) : 
        self.pos = pos
        self.dir = Vector2(1,0)
        self.angle = deg
        self.dir.rotate_ip(self.angle)
    def show(self,screen):
        pygame.gfxdraw.line(screen,int(self.pos.x),int(self.pos.y),int(self.pos.x+self.dir.x*10),int(self.pos.y+self.dir.y*10),(255,255,255,255))
    def cast(self,wall) : 
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x 
        y2 = wall.b.y
        
        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if den == 0 : return 
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
        u = -1*((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / den
        if t > 0 and t < 1 and u > 0 : 
            pt = Vector2()
            pt.x = x1 + t * (x2-x1)
            pt.y = y1 + t * (y2-y1)
            return pt
        else : return 
    def rotate(self , offset) : 
        self.dir = Vector2(1,0)
        self.dir.rotate_ip(self.angle)
        self.dir.rotate_ip(offset)