import pygame as pg 
from pygame.math import Vector2
from particle import Particle
from walls import Wall
import random
pg.init()
width = 900 
height = 600
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock() 
pg.display.set_caption('Self driving vehicles')

walls = []
walls.append(Wall(0,0,width,0))
walls.append(Wall(width,0,width,height))
walls.append(Wall(width,height, 0,height))
walls.append(Wall(0,height,0,0))

walls.append(Wall(200, 600 , 200,300))
walls.append(Wall(200,300 , 350 , 150))
walls.append(Wall(350,150, 900 , 150))
walls.append(Wall(300 , 600 , 300 , 300))
walls.append(Wall(300,300 , 350 , 250))
walls.append(Wall(350,250 , 900 , 250))



def nextGeneration() :
    calculateFitness(end)
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
def calculateFitness(target) : 
    for particle in savedPopulation : 
        particle.calculateFitness(target)
    sum = 0
    for particle in savedPopulation : 
        sum += particle.fitness
    for particle in savedPopulation : 
        particle.fitness = particle.fitness / sum

# group.add(cars)
running = True
bgcol = 10
start = Vector2(250 , 550)
end = Vector2(750 , 200)
# p = Particle(start.x,start.y)

total = 100
population = []
savedPopulation = []

for  i in range(total) : 
    population.append(Particle(start.x,start.y))

n = 1
while running : 
    screen.fill((bgcol,bgcol,bgcol))
    for i in range(n) : 
        for particle in population : 
            particle.update()
            # particle.show(screen)
            particle.check(end)
            particle.lookWalls(walls , screen)
    
    for wall in walls : wall.show(screen)
    for particle in population : particle.show(screen)
    pg.draw.circle(screen ,(255,255,255) , (start.x,start.y),10)
    pg.draw.circle(screen ,(255,255,255) , (end.x,end.y),10)

    # for i in range(len(population)-1 , -1 , -1) : 
    #     if population[i].isDead or population[i].finished : 
    #         savedPopulation.append(population[i])
    for particle in population : 
        if particle.isDead or particle.finished : 
            if not particle.added : 
                savedPopulation.append(particle)
                particle.added = True
    if len(savedPopulation) == len(population) : 
        population = []
        nextGeneration()
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
    
    # group.draw(screen)
    # group.update()
    pg.display.flip()
    clock.tick(60)
pg.quit()
