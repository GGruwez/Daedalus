import pygame
import sys, os, traceback
import math


"""
Solar system Newtonian gravity simulation using Pygame and RK4. 
I am aware the sun is not a planet :)

https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation
https://en.wikipedia.org/wiki/Solar_System
"""

###########################################################################
# TODO: - Scale issues                                                    #
#       - Experiment with right initial settings of planets               #
#       - Track trajectory of planet                                      #
###########################################################################


pygame.display.init()
pygame.font.init()

size = width, height = 1200,700
pygame.display.set_caption("Project Daedalus - Solar System Simulation - Gilles Gruwez")
surface = pygame.display.set_mode(size)

#units:
#   mass [kg]
#   distance [pixel]
#   time [s]

t=0
dt = 1

planets = []

def getApproximateG(width):
    # Neptune is 4.5 * 10^9 km from the sun
    kmperpixel = 4.5 * 10**9 / width 
    G = 6.67384*(10**(-20)) #km^3 kg^-1 s^-2
    #approxG = G/((kmperpixel)**3)
    approxG = G/((kmperpixel)**3)


    return approxG

G = getApproximateG(width)
density = 0.00001

class State:
    def __init__(self, x, y, velX, velY):
        self.x, self.y = x,y
        self.velX, self.velY = velX, velY

class Derivative:
    def __init__(self, dx, dy, dvelX, dvelY):
        self.dx, self.dy = dx, dy 
        self.dvelX, self.dvelY = dvelX, dvelY

class Planet:
    def __init__(self,name):
        self.name = name
        if name == "Sun":
            self.state = State(600,350,0,0)
            self.mass = 1.989*(10**30)*density
            #self.mass = (4.0/3.0)*math.pi*density*1.5**3*1000
            self.color = (255,128,0)
            self.radius = 40
        if name == "Mercury":
            self.state = State(1000,350,0,10)
            #self.mass = (4.0/3.0)*math.pi*density*1.5**3*1000
            self.mass = 3.285*(10**23)*density
            self.color = (255,255,255)
            self.radius = 3
        if name == "Venus":
            self.state = State(350,500,0,2)
            self.mass = 4.867*(10**24)
            self.color = (153,204,255)
            self.radius = 5
        if name == "Earth":
            self.state = State(350,500,0,2)
            self.mass = 5.972*(10**24)
            self.color = (0,128,255)
            self.radius = 5
        if name == "Mars":
            self.state = State(350,500,0,2)
            self.mass = 6.39*(10**23)
            self.color = (204,0,0)
            self.radius = 4
        if name == "Jupiter":
            self.state = State(350,500,0,2)
            self.mass = 1.898*(10**27)
            self.color = (96,96,96)
            self.radius = 15
        if name == "Saturnus":
            self.state = State(350,500,0,2)
            self.mass = 5.683*(10**26)
            self.color = (153,153,0)
            self.radius = 14
        if name == "Uranus":
            self.state = State(350,500,0,2)
            self.mass = 8.681*(10**25)
            self.color = (204,255,255)
            self.radius = 10
        if name == "Neptunus":
            self.state = State(350,500,0,2)
            self.mass = 1.024*(10**26)
            self.color = (0,0,204)
            self.radius = 10

    def acceleration(self,state,t):
        ax = 0.0
        ay = 0.0
        for p in planets:
            if p is self:
                continue
            dx = p.state.x - state.x
            dy = p.state.y - state.y
            dsq = dx*dx + dy*dy  
            dr = math.sqrt(dsq)
            force = G*self.mass*p.mass/dsq if dsq>1e-5 else 0
            ax += force*dx/dr
            ay += force*dy/dr
        return (ax, ay)

    #RK 4 - step size: dt
    def initial(self,state, t):
        ax, ay = self.acceleration(state,t)
        return Derivative(state.velX, state.velX, ax, ay)

    def next(self, initialState, derivative, t, dt):
        state = State(0., 0., 0., 0.)
        state.x = initialState.x + derivative.dx*dt
        state.y = initialState.y + derivative.dy*dt
        state.velX = initialState.velX + derivative.dvelX*dt
        state.velY = initialState.velY + derivative.dvelY*dt
        ax, ay = self.acceleration(state, t+dt)
        return Derivative(state.velX, state.velY, ax, ay)

    def update(self, t, dt):
        k1 = self.initial(self.state, t)
        k2 = self.next(self.state, k1, t, dt*0.5)
        k3 = self.next(self.state, k2, t, dt*0.5)
        k4 = self.next(self.state, k3, t, dt)
        self.state.x += dt*(1.0/6.0 * (k1.dx + 2.0*k2.dx + 2.0*k3.dx + k4.dx))
        self.state.y += dt*(1.0/6.0 * (k1.dy + 2.0*k2.dy + 2.0*k3.dy + k4.dy))
        self.state.velX += dt*(1.0/6.0 * (k1.dvelX + 2.0*k2.dvelX + 2.0*k3.dvelX + k4.dvelX))
        self.state.velY += dt*(1.0/6.0 * (k1.dvelY + 2.0*k2.dvelY + 2.0*k3.dvelY + k4.dvelY))

    def draw(self, surface):
        x,y = math.floor(self.state.x),math.floor(self.state.y)
        pygame.draw.circle(surface,self.color,(x,y),self.radius,0)

    def trackTrajectory(self):
        pass
    
def setup():
    global planets
   
    planets = [Planet("Sun"),Planet("Mercury")]

def updateAll(t,dt):
    for p in planets:
        if p.name == "Sun":
            continue
        p.update(t, dt)

def draw():
    surface.fill((25,0,0))

    for p in planets:
        p.draw(surface)
        
    pygame.display.flip()

def main():
    setup()
    running = True
    while running:
        updateAll(t,dt)
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                sys.exit()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()