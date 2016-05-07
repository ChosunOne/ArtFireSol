#Created by Josiah Evans 2016

#Import modules
import math
import os
clear = lambda: os.system('cls')

#Function Definitions
def numericalInput(prompt):
    entry = True
    userinput = ''
    while entry:
        userinput = input(prompt)
        try:
            int(userinput)
            entry = False
        except:
            print("invalid input \n")
    return userinput

def calcA(tar, bat):
    x1 = int(tar[0:4])
    x2 = int(bat[0:4])
    result = x1 - x2
    return result

def calcB(tar, bat):
    y1 = int(tar[4:8])
    y2 = int(bat[4:8])
    return  (y1 - y2)

def calcQ(tar, bat):
    x1 = int(tar[0:4])
    x2 = int(bat[0:4])
    if x1 > x2:
        return 90
    else:
        return 270

def calcBearing(q, a, b):
    if a == 0:
        a = 1
    return q - math.degrees(math.atan(b / a))

def calcTime(x, v, theta):
    return x / (v*math.cos(theta))

def calcRange(a, b):
    return 10 * (a**2 + b**2)**.5

def calcMuzzleVelocity(g, x, theta, y):
    v = ((-g * (x**2) * (math.tan(theta)**2 + 1)) / (2*y - 2*x*math.tan(theta)))**.5
    return v

def calcTheta(v, g, x, y):
    angles = {}
    angles["high"] = math.atan((v**2 + (v**4 - g*(g*x**2 + 2*y*v**2))**.5) / (g*x))
    angles["low"] = math.atan((v**2 - (v**4 - g*(g*x**2 + 2*y*v**2))**.5) / (g*x))
    return angles

def calcEotvos(bearing, velocity, latitude = 35.122002): 
    latitude = latitude * (2 * math.pi/360)
    omega = math.cos(latitude) * 1670
    earthRadius = 6367444.7
    rbearing = bearing * (2 * math.pi / 360) #bearing in radians
    u = math.cos(rbearing) * velocity #latitudinal velocity
    v = math.sin(rbearing) * velocity #longitudinal velocity
    a = 2 * omega * u * math.cos(latitude) + (u**2 + v**2)/earthRadius
    return a

#Begin program

quit = False
while not quit:

    clear()
    print("Artillery Fire Solution Calculator")
    print()
    print("Select an artillery weapon")
    print()
    print("1. MK6 Mortar")
    print("2. M4 Scorcher / Sochor")
    print("3. M5 MLRS")
    print()
    v = 0.0
    x = 0.0
    h1 = 0.0
    h2 = 0.0
    y = 0.0
    
    q = 0.0
    theta = 0.0
    battery = 0
    target = 0
    weapon = input()
    print()
    if weapon.lower() != '1' and weapon.lower() != '2' and weapon.lower() != '3':
        print("invalid selection")
        print()
    elif weapon == '1':
        #We are using the MK6 Mortar

        battery = numericalInput("Enter your 8 figure battery grid reference \n")
        
        if len(battery) != 8:
            print("invalid grid reference")
            continue

        h2 = int(numericalInput("Enter your elevation \n"))

        firing = True
        while firing:
            print("FIRING MODE")
            print()
            target = numericalInput("Enter your target's 8 figure grid reference \n")
            h1 = int(numericalInput("Enter your target's elevation \n"))

            A = calcA(target, battery)
            B = calcB(target, battery)
            q = calcQ(target, battery)
            x = calcRange(A, B)
            y = h1 - h2
            bearing = calcBearing(q, A, B)
            g = 9.80665
            g += calcEotvos(bearing, v)

            if x < 34:
                print("Target is too close to battery")
                continue
            elif 34 <= x <= 499:
                v = 70.0
            elif 139 <= x <= 1998:
                v = 140.0
            elif 284 <= x <= 4078:
                v = 200.0
            else:
                print("Target is out of range")
                continue

            angles = calcTheta(v, g, x, y)

            hightime = calcTime(x, v, angles["high"])
            lowtime = calcTime(x, v, angles["low"])

            clear()

            print("FIRING SOLUTION")
            print()
            print("Range:", x)
            print("Bearing:", bearing)
            print("High Elevation:", math.degrees(angles["high"]))
            print("ETA:", hightime, "seconds")
            print("Low Elevation:", math.degrees(angles["low"]))
            print("ETA:", lowtime, "seconds")
            print()

            more = numericalInput("Enter new target? 1/0 \n")
            if int(more) == 0:
                firing = False
                clear()

    elif weapon == '2':
        #We are using the scorcher or the sochor
        
        battery = numericalInput("Enter your 8 figure battery grid reference \n")
        
        if len(battery) != 8:
            print("invalid grid reference")
            continue

        h2 = int(numericalInput("Enter your elevation \n"))

        firing = True
        while firing:
            print("FIRING MODE")
            print()
            target = numericalInput("Enter your target's 8 figure grid reference \n")
            h1 = int(numericalInput("Enter your target's elevation \n"))

            A = calcA(target, battery)
            B = calcB(target, battery)
            q = calcQ(target, battery)
            x = calcRange(A, B)
            y = h1 - h2
            bearing = calcBearing(q, A, B)
            g = 9.80665
            g += calcEotvos(bearing, v)
            if x < 826:
                print("Target is too close to battery")
                continue
            elif 826 <= x <= 2415:
                v = 153.9
            elif 2059 <= x <= 6021:
                v = 243.0
            elif 5271 <= x <= 15414:
                #v = 388.8
                v = 477.6
            elif 14644 <= x <= 42818:
                v = 648.0
            elif 22881 <= x <= 66903:
                v = 810.0
            else:
                print("Target is out of range")
                continue

            angles = calcTheta(v, g, x, y)

            hightime = calcTime(x, v, angles["high"])
            lowtime = calcTime(x, v, angles["low"])

            clear()

            print("FIRING SOLUTION")
            print()
            print("Range:", x)
            print("Bearing:", round(bearing, 2))
            print("High Elevation:", round(math.degrees(angles["high"]), 2))
            print("ETA:", round(hightime, 2), "seconds")
            print("Low Elevation:", round(math.degrees(angles["low"]), 2))
            print("ETA:", round(lowtime, 2), "seconds")
            print()

            more = numericalInput("Enter new target? 1/0 \n")
            if int(more) == 0:
                firing = False
                clear()

    elif weapon == '3':
        #We are using the MLRS
        
        battery = numericalInput("Enter your 8 figure battery grid reference \n")

        if len(battery) != 8:
            print("invalid grid reference")
            continue

        h2 = int(numericalInput("Enter your elevation \n"))

        firing = True
        while firing:
            print("FIRING MODE")
            print()
            target = numericalInput("Enter your target's 8 figure grid reference \n")
            h1 = int(numericalInput("Enter your target's elevation \n"))

            A = calcA(target, battery)
            B = calcB(target, battery)
            q = calcQ(target, battery)
            x = calcRange(A, B)
            y = h1 - h2
            bearing = calcBearing(q, A, B)
            g = 9.80665
            g += calcEotvos(bearing, v)

            if x < 826:
                print("Target is too close to battery")
                continue
            elif 799 <= x <= 4604:
                v = 212.5
            elif 3918 <= x <= 18418:
                v = 425.0
            elif 7196 <= x <= 41442:
                v = 637.5
            elif 12793 <= x <= 73674:
                v = 772.5
            else:
                print("Target is out of range")
                continue

            angles = calcTheta(v, g, x, y)

            hightime = calcTime(x, v, angles["high"])
            lowtime = calcTime(x, v, angles["low"])

            clear()

            print("FIRING SOLUTION")
            print()
            print("Range:", x)
            print("Bearing:", round(bearing, 2))
            print("High Elevation:", round(math.degrees(angles["high"]), 2))
            print("ETA:", round(hightime, 2), "seconds")
            print("Low Elevation:", round(math.degrees(angles["low"]), 2))
            print("ETA:", round(lowtime, 2), "seconds")
            print()

            more = numericalInput("Enter new target? 1/0 \n")
            if int(more) == 0:
                firing = False
                clear()
            




        

 



