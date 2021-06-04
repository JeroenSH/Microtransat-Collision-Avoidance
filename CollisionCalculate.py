# TODO
# angle with speed and richting checken

#voor rechte lijnen oplossing verzinnen
#kijken of schip stil ligt
# in lezen van bestand
# met echte waardes doen
# koers bepalen
# meerdere schepen tegelijk

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
        print(self.a)

    def calculateNewCoords(self,time):
        print(self.angle)    
        # calculate the new coords
        # cos = overstaand /schuine
        # schuine zijde is: s = v*t  
        # cos(90 -angle)
        # dus overstaand is formule
        # + oude coordinaat maakt niewe coordinaat
        self.y = self.y + (self.speed*time)*np.cos(90-self.angle)         
        self.x = self.x + (self.speed*time)*np.sin(90-self.angle)
        print("x y")
        print(self.x)
        print(self.y)

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

def coordsToMeters(long,lat):
    print(long)
    print(int(long))
    x = 1852 * (60 * (long - int(long)))
    y = 1852 * (60 * (lat - int(lat)))
    return x,y

def knotsToMPS(speed):
    return (speed *1.852)/3.6

# x,y = coordsToMeters(4.9, 2.32)
# print(x,y)

# speed = knotsToMPS(5)
# print(speed)


Formula1 = formula(0,2,1,300)         #onze boot
Formula2 = formula(0,5,1,170)        #ander schip
print(Formula1.a)
print(Formula2.a)

smallestDistance = 10000

for timeInterval in range(0,20,1):
    Formula1.calculateNewCoords(timeInterval)
    Formula2.calculateNewCoords(timeInterval)
    distance = DistanceBetweenPoints(Formula1.x , Formula1.y, Formula2.x , Formula2.y)
    print("distance")
    print(distance)
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