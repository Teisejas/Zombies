import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from Individ import individual
import matplotlib.patches as mpatches

#size of grid space
boundy = 100
boundx = 100

radius = .05 # infection transmission radius
probability = .1 # infection probability
newborn_chance = 0.001 #chance of newborn
zombie_chance = 0.005 #chance for zombie

henergy = 200 # human lives for 200 steps
zenergy = 99999 # while infected - immortal


nhumans = 200 # initial human population
steps = 500 # random walk steps

zombie = "zombie"
human = "human"

hspeed = 0.5 #humans are slower
zspeed = 0.5*hspeed

#newborns to be born in human population A
boundsx = np.arange(32,42)
boundsy = np.arange(32,42)
coords = np.transpose([np.tile(boundsx, len(boundsy)), np.repeat(boundsy, len(boundsx))])

#zombies to turn up in Population B
zboundsx = np.arange(20,30)
zboundsy = np.arange(20,30)
zcoords = np.transpose([np.tile(zboundsx, len(zboundsy)), np.repeat(zboundsy, len(zboundsx))])

#Energy steps until humans die naturally

#collect everyone's coordinates 
everyone = []

#initiate human Population A
for n in range(int(nhumans/2)):
    everyone.append(individual(np.random.randint(32,42),np.random.randint(32,42),
                               0,boundx,boundy, henergy, human, hspeed))

#initiate human Population B
for n in range(int(nhumans/2)):
    everyone.append(individual(np.random.randint(20,30),np.random.randint(20,30),
                               0,boundx,boundy, henergy, human, hspeed))
   

fig = plt.figure(figsize=(5,5))
plt.xlim(0,100)
plt.ylim(0,100)
ax=plt.axes()

ims=[]

for n in range(steps):
    
    #Make everyone random walk, update location, and check for transmission of zombie infection if zombie nearby
    for i in range(0,len(everyone)):
        everyone[i].transmission(everyone[:i]+everyone[i+1:],radius,probability)
    for i in range(0,len(everyone)):
        everyone[i].Random_Walk()
    
    #generate human new borns based on chance within the population A
    human_is_born_here = np.random.rand(len(coords)) <= newborn_chance
    newhumans = coords[human_is_born_here]
    for (x1, y1) in newhumans:
        everyone.append(individual(x1, y1, 0, boundx,boundy, henergy, human, hspeed))
    
    
    #kill human if human and zombie step on each other (same coordinates)
    for j, everyone1 in enumerate(everyone):
        for everyone2 in everyone[j:]:
            if (everyone1.x == everyone2.x and
                everyone1.y == everyone2.y):
                everyone1.interact(everyone2)
            if (everyone1.x != everyone2.x):
                break
            if (everyone1.y != everyone2.y):
                break
            
    #clean up corpses when human dies from natural death or after getting killed by zombie
    dead_indexes = []
    for j, i in enumerate(everyone):
        if i.isDead:
            dead_indexes.append(j)
    everyone = list(np.delete(everyone, dead_indexes))
    
    #generate zombies based on chance within the population B
    zombie_popA = np.random.rand(len(zcoords)) <= zombie_chance
    newzombies = zcoords[zombie_popA]
    for (x1, y1) in newzombies:
        everyone.append(individual(x1, y1, 1, boundx, boundy, zenergy, zombie, zspeed))
    
    #No we need to track everyone's coordinates
    coordx = []
    coordy = []
    status = []
    for person in everyone:
        coordx.append(person.x)
        coordy.append(person.y)
        status.append(person.status)
    #preferably as numpy arrays
    status = np.array(status)
    coordx = np.array(coordx)
    coordy = np.array(coordy)
    colormap = np.array(['#0b559f', '#CD3333', '#89bedc'])
    #Which we can easily index for a scatter plot on one line
    im=[ax.scatter(coordx, coordy,c=colormap[status])]
    
    pop_a = mpatches.Patch(color='#0b559f', label='Humans')
    pop_b = mpatches.Patch(color='#CD3333', label='Zombies')
    pop_c = mpatches.Patch(color='#89bedc', label='Recoverd (immune)')
    plt.legend(handles=[pop_a,pop_b,pop_c])
    
    #Add this artis object to our list
    ims.append(im)

#create animation
        
ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,repeat_delay=1000)

plt.show()

#save as a gif

f = r"c://Users/e10240/.spyder-py3/anim.gif" 
writergif = animation.PillowWriter(fps=30) 
ani.save(f, writer=writergif)