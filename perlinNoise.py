import pygame as pg 
import numpy as np 
from perlin_noise import PerlinNoise 
from pygame.math import Vector2

pg.init()
width = 900 
height = 600
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock() 
pg.display.set_caption('Perlin Noise Example')
noise = PerlinNoise(octaves=1 , seed = 10)
bgcol = 80
running = True
loop = True
def scale(val , startX , endX , startY , endY) : 
    x1 , y1 = startX , startY
    x2 , y2 = endX , endY
    return y2 - (y2-y1)*(x2-val)/(x2-x1)
off = 20
t = 0
n=1
dir = 1
phase = 0
zoff = 0
while running : 
    points = []
    if loop :
        screen.fill((bgcol,bgcol,bgcol))
        for theta in np.linspace(0,2*np.pi , 500) : 
            xoff = scale(np.cos(theta + (phase+off*.01)) , -1,1 , 0,off*.1)
            yoff = scale(np.sin(theta + (phase+off*.01)) , -1,1 , 0,off*.1)
            r = scale(noise([xoff , yoff , zoff]) , 0,1,200,300)
            x = int((width/2) + (r * np.cos(theta)))
            y = int((height/2) + (r * np.sin(theta)))
            vec = Vector2(x,y)
            points.append(vec)
            t+=.001
        for i in range(len(points)-1) : 
            x1,y1 = points[i].x , points[i].y
            x2,y2 = points[i+1].x , points[i+1].y
            pg.draw.line(screen , (200,200,200), (x1,y1),(x2,y2),1)
            # if i == len(points)-2 : 
            #     x1,y1 = points[0][0] , points[0][1]
            #     x2,y2 = points[i+1][0] , points[i+1][1]
            #     pg.draw.line(screen , (200,200,200), (x1,y1),(x2,y2),1)
        # loop = False
        zoff += .1
        # off += dir
        if off > 100 : dir *= -1
        if off < 1 : dir *= -1
    for event in pg.event.get() : 
        if event.type == pg.QUIT :  
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_ESCAPE : 
                running = False 
            if event.key == pg.K_SPACE : 
                loop = not loop
            if event.key == pg.K_UP : 
                n += 1
                print(n)
            if event.key == pg.K_DOWN : 
                n -= 1
                if  n <= 0 : n = 1
                print(n)
    pg.display.flip()
    clock.tick(30)
pg.quit()
