# TODO
# koers bepalen
# meerdere schepen tegelijk
# direct uitlezen uit ais ?

import numpy as np
from fractions import Fraction
class formula:
    def __init__(self, x, y ,speed,angle):
        self.a = 0
        self.angle = angle
        self.speed = speed
        self.KeepAngleInParameters()
        self.x = x
        self.y = y
        self.b = 0
        self.headingToCoefficient()
        self.CalculateB()
        self.changeToInt()
        self.negA = False
    
    def KeepAngleInParameters(self):
        # verander de angle zodat de richtingscoefficient goed werkt.
        if (self.angle <= 90):
            self.negA = False
        elif (self.angle <= 180):
            self.angle = 180 - self.angle
            self.negA = True
        elif (self.angle <= 270):
            self.angle = self.angle - 180
            self.speed = self.speed *-1
            self.negA = False
        elif (self.angle <= 360):
            self.negA = True
            self.speed = self.speed *-1
            self.angle = 360 - self.angle
        # else:
        #     self.negA = True
        #     self.speed = self.speed *-1
        #     self.angle = 270 - self.angle

    def headingToCoefficient(self):
        if(self.angle == 90 or self.angle ==270):
            self.a = 0
            return
        if(self.angle == 0 or self.angle == 180):
            self.angle = self.angle + 0.0001
            
            
        angleB1 = 180 -90 - self.angle
        sideAC = np.sin(np.radians(angleB1)/np.sin(np.radians(90)))
        angleB2 = 90 - angleB1
        sideAD = np.sin(np.radians(angleB2)/np.sin(np.radians(90)))
        y2 = self.y + sideAC
        x2 = self.x + sideAD
        self.a = (y2- self.y)/(x2 -self.x)
        self.a = float(self.a)
        if(self.negA):
            self.a = self.a *-1

    def calculateNewCoords(self,time):
        # calculate the new coords
        # cos = overstaand /schuine
        # schuine zijde is: s = v*t  
        # cos(90 -angle)
        # dus overstaand is formule
        # + oude coordinaat maakt niewe coordinaat
        self.y = self.y + (self.speed*time)*np.cos(90-self.angle)         
        self.x = self.x + (self.speed*time)*np.sin(90-self.angle)
        # print("x y")
        # print(self.x)
        # print(self.y)

    def CalculateB(self):
        self.b = self.y -(self.a*self.x)
        if(self.b / round(self.b) == 1):
            self.b = int(self.b)

    def changeToInt(self):
        if (type(self.a) == float and type(self.b) == float):
            aF = str(Fraction(str(self.a)))
            aS = aF.split('/')
            bF = str(Fraction(str(self.b)))
            bS = bF.split('/')
            lcm = np.lcm(int(aS[1]), int(bS[1]))
        elif (type(self.a) == float):
            aF = str(Fraction(str(self.a)))
            aS = aF.split('/')
            lcm = np.lcm(int(aS[1]), self.b)
        elif (type(self.b) == float):
            bF = str(Fraction(str(self.b)))
            bS = bF.split('/')
            lcm = np.lcm(self.a, int(bS[1]))
        else:
            lcm = np.lcm(self.a,self.b)
        self.a = int(self.a * lcm)
        self.b = int(self.b * lcm)

def DistanceBetweenPoints(x1,y1,x2,y2):
    return np.sqrt(((x2-x1)**2)+((y2-y1)**2) )

def coordsToMeters(lon,lat):
    lon = lon.replace(' ','') 
    lat = lat.replace(' ','') 
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
for i in range(len(file_split)):
    file_split[i] = file_split[i].replace('[','')
    file_split[i] = file_split[i].replace(']','')

for i in range(len(file_split)):
    line_split = file_split[i].split(',')
    if not line_split[5] == " null":
        if((int(line_split[5])) == 511):
            #print("geen heading")
            pass
        else: 
            ships.append(line_split)      
            #print(line_split[0])
# for i in range(len(ships)):
i = 2
x,y = coordsToMeters(ships[i][2], ships[i][1])
speed = knotsToMPS(ships[i][3])
angle = ships[i][5]
angle = angle.replace(' ','')
angle = int(angle)

Formula1 = formula(4.453,52,5,180)         #onze boot
Formula2 = formula(x,y,speed,angle)        #ander schip
# print(Formula1.a)
# print(Formula2.a)

smallestDistance = 1000000000000

for timeInterval in range(0,1000,1):
    Formula1.calculateNewCoords(timeInterval)
    Formula2.calculateNewCoords(timeInterval)
    distance = DistanceBetweenPoints(Formula1.x , Formula1.y, Formula2.x , Formula2.y)
    if(distance < smallestDistance):
        smallestDistance = distance

print("shortest distance is:")
print(smallestDistance)
smallestDistance = 10000



# # ax +1y = b
# k = np.array([[Formula1.a, 1],[Formula2.a,1]]) 
# l = np.array([Formula1.b,Formula2.b])
# m = np.linalg.solve(k,l)
# #print(m)
