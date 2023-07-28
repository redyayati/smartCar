import pygame as pg 
from pygame.math import Vector2
from particle import Particle
from walls import Wall
import numpy as np 
import random
from perlin_noise import PerlinNoise 
pg.init()
width = 900 
height = 700
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock() 
pg.display.set_caption('Self driving vehicles')
noise = PerlinNoise(octaves=1 , seed = random.randint(0,30))

walls = []
inside = []
outside = []
checkpoints = []

def scale(val , startX , endX , startY , endY) : 
    x1 , y1 = startX , startY
    x2 , y2 = endX , endY
    return y2 - (y2-y1)*(x2-val)/(x2-x1)
def nextGeneration() :
    calculateFitness()
    for i in range(total) :
        newParticle = pickOne()
        population.append(newParticle)
    # group.add(cars)
    del savedPopulation[:]
def pickOne(): 
    index = 0 
    r = random.random()
    while r > 0 :
        r = r - savedPopulation[index].fitness
        index += 1
    index -= 1 
    theChoosenOne = savedPopulation[index]
    child = Particle(start.x,start.y,theChoosenOne.brain)
    child.mutate()
    return child
def calculateFitness() : 
    for particle in savedPopulation : 
        particle.calculateFitness()
    sum = 0
    for particle in savedPopulation : 
        sum += particle.fitness
    for particle in savedPopulation : 
        particle.fitness = particle.fitness / sum
pathWidth = 50
pathComplexity = 2
def makeWalls():
    global start , end
    numCheckpoints = 25
    for theta in np.linspace(0,2*np.pi , numCheckpoints) : 
        xoff = scale(np.cos(theta) , -1,1 , 0,pathComplexity)  
        yoff = scale(np.sin(theta) , -1,1 , 0,pathComplexity) 
        r = scale(noise([xoff , yoff]) , 0,1,225,375)
        # x = int((width/2) + ((r+50) * np.cos(theta)))
        # y = int((height/2) + ((r+50) * np.sin(theta)))
        x1 = int((width/2) + ((r*1.3-pathWidth) * np.cos(theta)))
        y1 = int((height/2) + (((r-pathWidth)) * np.sin(theta)))
        x2 = int((width/2) + ((r*1.3+pathWidth) * np.cos(theta)))
        y2 = int((height/2) + ((r+pathWidth) * np.sin(theta)))
        # checkpoints.append(Vector2(x,y))
        checkpoints.append(Wall(x1,y1,x2,y2))
        inside.append(Vector2(x1,y1))
        outside.append(Vector2(x2,y2))
    for i in range(len(checkpoints)) : 
        a1 = inside[i]
        b1 = inside[(i+1)%len(checkpoints)]
        walls.append(Wall(a1.x,a1.y,b1.x,b1.y))
        a2 = outside[i]
        b2 = outside[(i+1)%len(checkpoints)]
        walls.append    (Wall(a2.x,a2.y,b2.x,b2.y))
    # partIn = inside[numCheckpoints-2]
    # partOut = outside[numCheckpoints-2]
    # partitionWall = Wall(partIn.x,partIn.y,partOut.x,partOut.y)
    # walls.append(partitionWall)
    walls.append(Wall(0,0,width,0))
    walls.append(Wall(width,0,width,height))
    walls.append(Wall(width,height, 0,height))
    walls.append(Wall(0,height,0,0))
    start = checkpoints[0].midPoint()
    end = checkpoints[len(checkpoints)-3].midPoint()
def resetWalls(): 
    global noise , start , end
    noise = PerlinNoise(octaves=1 , seed = random.randint(0,30))
    del inside[:]
    del outside[:]
    del checkpoints[:]
    del walls[:]
    makeWalls()
    start = checkpoints[0].midPoint()
    end = checkpoints[len(checkpoints)-3].midPoint()
# group.add(cars)
running = True
bgcol = 10
# p = Particle(start.x,start.y)
total = 50
population = []
savedPopulation = []
makeWalls()

for  i in range(total) : 
    population.append(Particle(start.x,start.y))
n = 1
points = []
showRays = False
while running : 
    screen.fill((bgcol,bgcol,bgcol))
    for i in range(n) : 
        for particle in population : 
            particle.showRays = showRays
            particle.update()
            particle.check(checkpoints,screen)
            # particle.show(screen)
            particle.lookWalls(walls , screen)
        # for particle in population : 
        #     if particle.isDead or particle.finished : 
        #         if not particle.added : 
        #             if particle.index > 2 : print(particle.index)
        #             savedPopulation.append(particle)
        #             particle.added = True
        for i in range(len(population)-1 ,-1 , -1) : 
            if population[i].isDead or population[i].finished : 
                savedPopulation.append(population.pop(i))
    if len(population) == 0 : 
        population = []
        resetWalls()
        screen.fill((bgcol,bgcol,bgcol))
        
        nextGeneration()

    for wall in walls : wall.show(screen)
    # for ck in checkpoints : ck.show(screen)
    for particle in population : particle.show(screen)
    # pg.draw.circle(screen , (180,80,80), (start.x,start.y),10)
    # pg.draw.circle(screen , (180,80,80), (end.x,end.y),10)
    for event in pg.event.get() : 
        if event.type == pg.QUIT :  
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_ESCAPE : 
                running = False 
            if event.key == pg.K_UP : 
                n += 2
                if n >= 30 : n = 30
                print(n)
            if event.key == pg.K_DOWN : 
                n -= 2
                if  n <= 0 : n = 1
                print(n)
            if event.key == pg.K_SPACE : showRays = not showRays
            if event.key == pg.K_r : 
                for i in range(len(population)-1 ,-1 , -1) :   
                    savedPopulation.append(population.pop(i))
    
    # group.draw(screen)
    # group.update()
    pg.display.flip()
    clock.tick(30)
pg.quit()
