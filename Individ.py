import numpy as np

#this funcion calculates the distance between one individual and another
def distance(coord_1,coord_2):
        return np.sqrt((coord_1[0]-coord_2[0])**2 + (coord_1[1]-coord_2[1])**2) 

class individual:
  #each individual is instatiated with location, status, energy, species type, speed and a set of boundaries
    def __init__(self,x,y,status,boundx, boundy, energy, species, speed):
        self.x = x
        self.y = y
        self.status = status
        self.boundx = boundx
        self.boundy = boundy
        self.speed = speed
        self.time = 0
        self.immune = 0 # no initial immunity 
        self.species = species
        self.isDead = False
        self.energy = energy
        
    #Interact with another individual:
    #If they're from the same species, ignore each other.
    #Zombie kills human.
    def interact(self, other):

        if self.species == "human" and other.species == "zombie":
            self.die()

        if self.species == "zombie" and other.species == "human":
            other.die()
    
    #Changing status to dead
    def die(self):
        
        self.isDead = True

   #Every turn of random walk at an individual speed it will update location
   #every step on the gird takes 1 energy; once no energy left an individual proceeds to die  
    def Random_Walk(self):
        boundx = self.boundx
        boundy = self.boundy
        speed = self.speed
        
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3
        STAY = 4
        
        direction = np.random.randint(0, 5)
              
        self.energy -= 1
        
        if direction == LEFT:
           self.x += 1*speed if self.x > 0 else -1   #bounce back from the bounds of the grid
        if direction == RIGHT:
           self.x -= 1*speed  if self.x < boundx-1 else -1
        if direction == UP:
           self.y += 1*speed  if self.y < boundy-1 else -1
        if direction == DOWN:
           self.y -= 1*speed  if self.y > 0 else -1
        if direction == STAY:
            pass
        
        if self.energy <= 0:
            self.die()
            
    #each individual has a certain chance to be infected by others
    #within a certain radius
    def transmission(self,others,radius,probability):
        hspeed = 0.5 #match human speed with one from simulation
      #if they already have immunity (recovered from zombie infection)
        if self.status == 2 and self.immune == 1:
            pass
        #and if they're already infected, they won't get infected again
        elif self.status == 1:
            #but we can track how long they've been infected as zombies
            self.time +=1
            #And put them into the 'immune' human category after they recover from zombie infection
            if self.time == 100:
                self.status =2
                self.immune = 1
                self.energy = 200 #once recovered assign human life span
                self.speed = hspeed #back to human speed
        else:
          #but if they're susceptible, 
            neighbor_count = 0
            for other in others:
            #then every zombie nearby increases the probability of transmission
                if other.immune == 1:
                    pass
                elif other.status == 1:
                    if distance((self.x, self.y),(other.x, other.y)) < radius:
                        neighbor_count +=1
            if sum([1 for x in np.random.random(neighbor_count) if x >probability]) > 0:
                self.status = 1
                self.energy = 99999 #once infected unlimited energy
                self.speed = hspeed*2 #assign zombie speed level