from pygame.math import Vector2
import pygame.gfxdraw
from nn import NeuralNetwork
import numpy as np
import pygame as pg
from ray import Ray

def scale(val , startX , endX , startY , endY) : 
    x1 , y1 = startX , startY
    x2 , y2 = endX , endY
    return y2 - (y2-y1)*(x2-val)/(x2-x1)
def ptDist(p1,p2,x,y) : 
    num = abs((p2.x - p1.x)*(p1.y-y) - (p1.x-x)*(p2.y-p1.y))
    den = ((p2.x-p1.x)**2 + (p2.y - p1.y)**2)**.5
    return num/den
lifespan = 30
class Particle(): 
    def __init__(self , xpos,ypos, brain = None) :
        self.pos = Vector2(xpos,ypos)
        self.vel = Vector2()
        self.acc = Vector2()
        self.maxspeed = 10
        self.rays = []
        for i in range(-90,92,45) : 
            ray = Ray(self.pos , i)
            self.rays.append(ray)
        self.sight = 10
        self.isDead = False
        self.finished = False
        self.added = False
        self.score = 0
        self.fitness = 0
        self.round = 0
        self.showRays = True
        self.sight = 200
        self.index = 0
        self.counter = 0
        self.goal = None
        if brain : self.brain = brain.copy()
        else : self.brain = NeuralNetwork(len(self.rays),len(self.rays),1)
    def check(self,checkpoints,screen): 
        if not self.finished : 
            self.goal = checkpoints[self.index]
            d = ptDist(self.goal.a , self.goal.b , self.pos.x,self.pos.y)
        
        # d = self.pos.distance_to(goal)
            if d < 5 : 
                self.index = (self.index + 1) % len(checkpoints)
                self.counter = 0
                self.fitness += 1
                # if self.index == len(checkpoints)-1 : self.finished = True
        # for i in range(self.index) : 
            # checkpoints[self.index-1].show(screen)

    def calculateFitness(self) : 
        self.fitness = self.fitness**2
        # if self.finished : self.fitness = 100 
        # else : 
        #     d = self.pos.distance_to(target)
        #     self.fitness = 1/d

    def lookWalls(self,walls, screen): 
        inputs = []
        for ray in self.rays : 
            record = self.sight
            closest = None
            for wall in walls : 
                pt = ray.cast(wall)
                if pt : 
                    dist = self.pos.distance_to(pt)
                    if dist < record  and dist < self.sight : 
                        record = dist
                        closest = pt
            if record < 5 : self.isDead = True
            inputs.append(scale(record , 0,self.sight,1,0))
           
            if self.showRays : 
                if closest : 
                    self.showRay(self.pos , closest , screen)

        # vel = self.vel.copy()
        # if vel.magnitude() > 0 : vel.normalize_ip()
        # inputs.append(vel.x)
        # inputs.append(vel.y)
        output = self.brain.predict(inputs)
        angle = scale(output[0] , 0,1,-180, 180)
        angle += Vector2(2,0).angle_to(self.vel)
        steeringVec = Vector2(4,0)
        steeringVec.rotate_ip(angle)
        self.applyForce(steeringVec - self.vel)
        

    def applyForce(self, force) : 
        self.acc += force 
    def update(self) : 
        if not self.isDead and not self.finished: 
            self.pos += self.vel 
            self.vel += self.acc 
            # if self.vel.magnitude() > 0 : self.vel.clamp_magnitude_ip(0,self.maxspeed)
            self.acc *= 0 
            self.counter += 1
            if self.counter > lifespan : self.isDead = True
            for ray in self.rays : ray.rotate(Vector2(2,0).angle_to(self.vel))
    def show(self , screen) : 
        theta = Vector2(1,0).angle_to(self.vel)
        theta = np.pi * theta / 180
        self.drawRect(self.pos.x , self.pos.y,theta,5,screen)
        # if self.goal : self.goal.show(screen)
    def showRay(self,pt1,pt2 , screen) :
        x1,y1 = pt1.x,pt1.y
        x2,y2 = pt2.x,pt2.y
        pygame.gfxdraw.line(screen,int(x1),int(y1),int(x2),int(y2),(255,255,255,25))
        # pg.draw.circle(screen,(180,10,10),(int(x2),int(y2)),3)
    def run(self) : 
        if not self.isDead : 
            self.pos += self.vel
            self.vel += self.accel 
            self.accel *= 0 
            for ray in self.rays : 
                ray.rotate(self.turnAngle)

    def mutate(self) : 
        self.brain.mutate(.05)

    # def boundary(self) : 
    #     margin = 3
    #     if self.pos.x > width - margin : self.pos.x = width-margin 
    #     if self.pos.x < margin : self.pos.x = margin 
    #     if self.pos.y > height-margin : self.pos.y = height-margin
    #     if self.pos.y < margin : self.pos.y = margin 
    # def show(self) : 
    #     theta = Vector2(1,0).angle_to(self.vel)
        # theta = self.vel.angle_to(Vector2(2,0))
        # theta = np.pi * theta / 180
        # self.drawVehicle(self.pos.x , self.pos.y,theta,20)
        # pg.draw.circle(screen,(150,150,150) , (int(self.pos.x),int(self.pos.y)),10)
        # pg.draw.line(screen, (255,255,255), (int(self.pos.x),int(self.pos.y)), (int(self.pos.x+self.vel.x*20), int(self.pos.y+self.vel.y*20)),2)
        # for ray in self.rays : 
        #     ray.show()

    def drawVehicle(self,xpos,ypos,theta,l,screen) : 
        x1,y1 = xpos+(5*l/4)*np.cos(theta), ypos+(5*l/4)*np.sin(theta)
        x2,y2 = xpos+l*np.cos(theta-(3.2*np.pi/4)), ypos+l*np.sin(theta-(3.2*np.pi/4))
        xt,yt = xpos+(l/2)*np.cos(theta+(-np.pi)), ypos+(l/2)*np.sin(theta+(-np.pi))
        x3,y3 = xpos+l*np.cos(theta+(3.2*np.pi/4)), ypos+l*np.sin(theta+(3.2*np.pi/4))
        pygame.gfxdraw.filled_polygon(screen, ((x1,y1), (x2,y2),(xt,yt),(x3,y3)), (255,255,255,100))
        pygame.gfxdraw.polygon(screen, ((x1,y1), (x2,y2),(xt,yt),(x3,y3)), (255,255,255,250))

    def drawRect(self,xpos,ypos,theta,l,screen) : 
        offTheta = np.pi/7
        x1,y1 = xpos+(1.5*l)*np.cos(theta+offTheta), ypos+(1.5*l)*np.sin(theta+offTheta)
        x2,y2 = xpos+(1.5*l)*np.cos(theta+(np.pi-offTheta)), ypos+(1.5*l)*np.sin(theta+(np.pi-offTheta))
        x3,y3 = xpos+(1.5*l)*np.cos(theta-(np.pi-offTheta)), ypos+(1.5*l)*np.sin(theta-(np.pi-offTheta))
        x4,y4 = xpos+(1.5*l)*np.cos(theta-offTheta), ypos+(1.5*l)*np.sin(theta-offTheta)
        pygame.gfxdraw.filled_polygon(screen, ((x1,y1), (x2,y2),(x3,y3),(x4,y4)), (255,255,255,50))
        pygame.gfxdraw.polygon(screen, ((x1,y1), (x2,y2),(x3,y3),(x4,y4)), (255,255,255,250))