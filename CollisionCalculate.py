import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
class formula:
    def __init__(self, x, y ,speed,angle):
        self.angle = angle
        self.speed = speed
        self.x = x
        self.y = y
    def updateAngle(self, angle):
        self.angle = angle
    def update(self, x, y ,speed):
        self.speed = speed
        self.x = x
        self.y = y
    def calculateNewCoords(self,time):
        # calculate the new coords
        # cos = overstaand /schuine
        # schuine zijde is: s = v*t  
        # cos(90 -angle)
        # dus overstaand is formule
        # + oude coordinaat maakt niewe coordinaat
        dY = 0
        dX = 0 
        if(self.angle <= 90):
            dY = (self.speed*time)*np.cos(np.radians(self.angle))         
            dX = (self.speed*time)*np.sin(np.radians(self.angle))
        elif(self.angle <= 180):
            dY = (self.speed*time)*np.cos(np.radians(180 - self.angle))        
            dX = (self.speed*time)*np.sin(np.radians(180 - self.angle))
            dY = dY *-1
        elif(self.angle < 270):
            dY = (self.speed*time)*np.cos(np.radians(self.angle -180))
            dX =(self.speed*time)*np.sin(np.radians(self.angle -180))
            dX = dX *-1
            dY = dY *-1
        elif(self.angle <= 360):
            dY = (self.speed*time)*np.cos(np.radians(360 - self.angle))        
            dX = (self.speed*time)*np.sin(np.radians(360 - self.angle))   
            dX = dX *-1
        self.y = self.y +dY
        self.x = self.x + dX

def DistanceBetweenPoints(x1,y1,x2,y2):
    return np.sqrt(((x2-x1)**2)+((y2-y1)**2) )

def coordsToMeters(lon,lat):
    try:
        lon = lon.replace(' ','') 
        lat = lat.replace(' ','') 
    except:
        pass
    lon = float(lon)
    lat = float(lat)
    x = 1852 * (60 * (lon - int(lon)))
    y = 1852 * (60 * (lat - int(lat)))
    return x,y

def knotsToMPS(speed):
    speed = speed.replace(' ','')
    speed = float(speed)
    return (speed *1.852)/3.6

# openen en lezen van bestand verander later naar direct uitlezen uit ais
f = open("data.txt", "r")
file = f.read()
file_splitLine = file.splitlines()
f.close()
file_split = list(set(file_splitLine))
ships = []

f2 = open( "data2.txt", "w")
for i in range(len(file_split)):
    file_split[i] = file_split[i].replace('[','')
    file_split[i] = file_split[i].replace(']','')

for i in range(len(file_split)):
    line_split = file_split[i].split(',')
    if not line_split[5] == " null":
        if((int(line_split[5])) == 511):
            pass
        else: 
            ships.append(line_split)      
dangerDistance = 10000
own_x = []
own_y = []
they_x = []
they_y = []
listThey_x = []
listThey_y = []
xoud = []
youd = []
h = 0
ownx,owny = coordsToMeters(4.5,50)
Formula1 = formula(ownx, owny,2,1)         #onze boot
timeInterval = 350
amountOfCoords = 100

for i in range(len(ships)):
    x,y = coordsToMeters(ships[i][1], ships[i][2])
    speed = knotsToMPS(ships[i][3])
    angle = ships[i][5]
    angle = angle.replace(' ','')
    angle = int(angle)
    Formula2 = formula(x,y,speed,angle)        #ander schip
    for j in range(0,amountOfCoords,1):
        Formula2.calculateNewCoords(timeInterval)
        they_x.append(Formula2.x)
        they_y.append(Formula2.y)
    listThey_x.append(they_x)
    listThey_y.append(they_y)
    they_x = []
    they_y = []

for i in range(0,amountOfCoords,1):
        Formula1.calculateNewCoords(timeInterval)
        xoud.append(Formula1.x)
        youd.append(Formula1.y)

def calculatedistances():
    global Formula1
    global own_x
    global own_y
    global listThey_x
    global listThey_y

    Formula1.update(ownx,owny,10)
    for i in range(0,amountOfCoords,1):
        Formula1.calculateNewCoords(timeInterval)
        own_x.append(Formula1.x)
        own_y.append(Formula1.y)
    for j in range(0, len(listThey_x)):
        for k in range(0, len(listThey_x[j])):
            distance = DistanceBetweenPoints(own_x[k], own_y[k], listThey_x[j][k] ,  listThey_y[j][k])
            print("test")
            print(str(distance))
            f2.write(str(distance) + "\n")
            if distance < dangerDistance:
                own_x = []
                own_y = []
                calculateNewHeading()
    return

def calculateNewHeading():
    print("new heading")
    global Formula1
    heading = Formula1.angle
    global h
    if (h % 2) == 0:
        h = h * -1
    heading = heading +h
    h += 5 
    Formula1.updateAngle(heading)
    calculatedistances()
    
calculatedistances()
root = Tk()
root.title('test')
root.geometry("400x200")
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def graph(x1, x2, y1, y2, i):
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.xlim(x1-150000, x1+150000)
    plt.ylim(y1-150000, y1+150000)
    plt.gca().set_aspect('equal', adjustable='box') 
    plt.scatter(x1,y1,c="red",s=3000)
    plt.scatter(x1, y1, c="green", Label = "Eigen boot")
    for ship in range(len(x2)):
        plt.scatter(x2[ship][i], y2[ship][i], c="red", Label = "boot")
        plt.plot(x2[ship],y2[ship], color = "red", Label = "Koers boot", linestyle = '--')
    plt.title('AIS')    
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.plot(own_x, own_y, color = "green", Label = "Koers eigen boot", linestyle = '--')
    plt.plot(xoud,youd,color="blue", Label= "Oude koers eigen boot", linestyle='--')
    plt.legend()
    plt.show(block=False)
    plt.pause(1)
    plt.close()
    
def update():
    for i in range(amountOfCoords):
        graph(own_x[i], listThey_x, own_y[i], listThey_y, i) 

my_button = Button(root, text="graph", command=update)
my_button.pack()

root.mainloop() 
