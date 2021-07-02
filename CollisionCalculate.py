import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import keyboard

class formula:
    def __init__(self, x, y ,speed,angle):
        self.angle = angle
        self.speed = speed
        self.x = x
        self.y = y
    def updateAngle(self, angle):           #update the angle of the boat
        self.angle = angle
    def update(self, x, y ,speed):          #update all the values of the boat
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

def DistanceBetweenPoints(x1,y1,x2,y2):                 #pythagoras 
    return np.sqrt(((x2-x1)**2)+((y2-y1)**2) )

def coordsToMeters(lon,lat):                    #change the values from longitude/ latitude to meters
    try:
        lon = lon.replace(' ','')               #try to remove empty spaces from string
        lat = lat.replace(' ','') 
    except:
        pass
    lon = float(lon)
    lat = float(lat)
    x = 1852 * (60 * (lon - int(lon)))         #calculate the x and y in meters
    y = 1852 * (60 * (lat - int(lat)))
    return x,y

def knotsToMPS(speed):                          #change the speed to meters per second
    speed = speed.replace(' ','')                #try to remove empty spaces from string
    speed = float(speed)
    return (speed *1.852)/3.6

def calculatedistances():
    global Formula1
    global own_x
    global own_y
    global listThey_x
    global listThey_y

    Formula1.update(ownx,owny,ownSpeed)                        #update to the new x and y coordinates
    for i in range(0,amountOfCoords,1):                        #calculate the new coordinates
        Formula1.calculateNewCoords(timeInterval)
        own_x.append(Formula1.x)
        own_y.append(Formula1.y)
    for j in range(0, len(listThey_x)):
        for k in range(0, len(listThey_x[j])):
            distance = DistanceBetweenPoints(own_x[k], own_y[k], listThey_x[j][k] ,  listThey_y[j][k])      #calculate the distance between our ship and another ship
            if distance < dangerDistance:           # if the distance is too small update the heading
                own_x = []
                own_y = []
                calculateNewHeading()
    return

def calculateNewHeading():                  # update the heading
    #heading is updated in a specific order. 
    # first add 5 to the origal heading
    # then substract 10 from the new heading
    # then add 15 from the new heading
    # then substract 20 from the new heading
    # this will continue untill a heading has been found
    # list of heading is (with start heading 0):
    #print("new heading")
    global Formula1
    heading = Formula1.angle
    global h
    if (h % 2) == 0:
        h = h * -1
    heading = heading +h
    h += 5 
    #print(heading)
    if (heading < 0):
        print(heading)
        heading = 360 + heading
    if (heading > 360):
        print(heading)
        heading = heading - 360
    Formula1.updateAngle(heading)
    calculatedistances()

def graph(x1, x2, y1, y2, i,blockBool):
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.xlim(x1-150000, x1+150000)                                  #set the size of the graph
    plt.ylim(y1-150000, y1+150000)
    plt.gca().set_aspect('equal', adjustable='box') 
    plt.text(1, 1, 'frame ' + str(i), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    plt.scatter(x1,y1,c="red",s=700)                               # circle of minimum distance from the ship
    plt.scatter(x1, y1, c="green", Label = "Eigen boot")            # display our own ship 

    plt.plot(own_x, own_y, color = "green", Label = "Koers eigen boot", linestyle = '--')       #display our heading
    plt.plot(xoud,youd,color="blue", Label= "Oude koers eigen boot", linestyle='--')            #display old heading before calculations

    for ship in range(len(x2)):                                             # go trough all the ships and display the ships and the heading
        plt.scatter(x2[ship][i], y2[ship][i], c="red", Label = "boot")
        plt.plot(x2[ship],y2[ship], color = "red", Label = "Koers boot", linestyle = '--')
    
    plt.title('AIS')    
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.legend()
    plt.show(block=blockBool)           #decides if the next frame is displayed False is same frame , True is next Frame
    plt.pause(0.001)
    plt.close()
    
def update():
    i = 0
    update = False
    while i < amountOfCoords:
        if keyboard.is_pressed('left arrow'):                               # if the left arrow is pressed go one frame back
            if i == 0:                                                      # prevent list index out of range
                i = 0
            else:
                i -= 1
            graph(own_x[i], listThey_x, own_y[i], listThey_y, i, update) 
        elif keyboard.is_pressed('right arrow'):                            # if the right arrow is pressed go one frame forward
            if i == amountOfCoords-1:                                      # prevent list index out of range
                i = amountOfCoords-1
            else:
                i += 1
            graph(own_x[i], listThey_x, own_y[i], listThey_y, i, update) 

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
ownSpeed = 2
Formula1 = formula(ownx, owny,ownSpeed,1)         #onze boot
timeInterval = 350
amountOfCoords = 100

#open the file with the ais data in it. 
#this can be changed later to directly reading from the ais module.
f = open("data2.txt", "r")
file = f.read()
file_splitLine = file.splitlines()
f.close()
file_split = list(set(file_splitLine))
ships = []

for i in range(len(file_split)):                                                    #remove the brackets for all entries
    file_split[i] = file_split[i].replace('[','')
    file_split[i] = file_split[i].replace(']','')

for i in range(len(file_split)):                            #split the line on every ',' and put it in a list
    line_split = file_split[i].split(',')
    if not line_split[5] == " null":
        if((int(line_split[5])) == 511):                    # if the heading is 511 do not append to the list. (ship is stationary)
            pass
        else: 
            ships.append(line_split)      


def calculateOtherCoords():
    global listThey_x
    global listThey_y
    global they_x
    global they_y
    for i in range(len(ships)):                             # go through list of all ships from ais data
        x,y = coordsToMeters(ships[i][1], ships[i][2])      #change to meters
        speed = knotsToMPS(ships[i][3])                     # change to meters per second
        angle = ships[i][5]
        angle = angle.replace(' ','')                       
        angle = int(angle)
        Formula2 = formula(x,y,speed,angle)                 #set all the data in the formula
        for j in range(0,amountOfCoords,1):                 #calculate the new coordinates and put it in a list.
            Formula2.calculateNewCoords(timeInterval)
            they_x.append(Formula2.x)
            they_y.append(Formula2.y)
        listThey_x.append(they_x)                           #list of coordinates list per ship     
        listThey_y.append(they_y)
        they_x = []
        they_y = []

def originalListOfCoords():
    for i in range(0,amountOfCoords,1):                     #calculate the original coordinates of our own ship to display it later       
        Formula1.calculateNewCoords(timeInterval)
        xoud.append(Formula1.x)
        youd.append(Formula1.y)

calculateOtherCoords()
originalListOfCoords()
calculatedistances()

root = Tk()
root.title('test')
root.geometry("400x200")
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


my_button = Button(root, text="graph", command=update)
my_button.pack()
root.mainloop() 
