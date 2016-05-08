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
    theta = theta * (2 * math.pi / 360)
    v = ((-g * (x**2) * (math.tan(theta)**2 + 1)) / (2*y - 2*x*math.tan(theta)))**.5
    return v

def calcFireRange(v, g, theta, y):
    theta = theta * (2 * math.pi / 360)
    r = (-2 * v**2 * math.tan(theta) - ((2 * v**2 * math.tan(theta))**2 - 4 * (-g*(math.tan(theta)**2 + 1) * -2 * y * v**2))**.5) / (-2 * g * (math.tan(theta)**2 + 1))
    return r

def calcTheta(v, g, x, y):
    angles = {}
    angles["high"] = math.atan((v**2 + (v**4 - g*(g*x**2 + 2*y*v**2))**.5) / (g*x))
    angles["low"] = math.atan((v**2 - (v**4 - g*(g*x**2 + 2*y*v**2))**.5) / (g*x))
    return angles

def calcEotvos(bearing, velocity, latitude = 35.122002, theta = 45.0): 
    latitude = latitude * (2 * math.pi/360)
    theta = theta * (2 * math.pi/360)
    omega = 7.27 * 10**-5
    earthRadius = 6367444.7 * math.cos(latitude)
    rbearing = bearing * (2 * math.pi / 360) #bearing in radians
    u = (math.sin(rbearing) * velocity) * math.cos(theta) #latitudinal velocity
    v = (math.cos(rbearing) * velocity) * math.cos(theta)  #longitudinal velocity
    a = 2 * omega * u * math.cos(latitude) + (u**2 + v**2)/earthRadius
    return a

#Begin program

weapons = {}
with open('velocities.txt', 'r') as f:
    currentWeapon = ""
    for line in f:
        if line == '\n':
            lastline = line
        elif lastline == '\n':
            #This is a new weapon
            line = line.replace('\n', '')
            weapons[line] = [line]
            currentWeapon = line
            lastline = line
        else:
            line = line.replace('\n', '')
            weapons[currentWeapon].append(line)
            lastline = line
quit = False
while not quit:

    clear()
    print("Artillery Fire Solution Calculator")
    print()
    print("Select an artillery weapon")
    print()

    selection = {}
    index = 1
    for wep in weapons.keys():
        print(str(index) + '. ' + wep)
        selection[index] = wep
        index += 1

    print(str(index) + ". Calibrate a weapon")

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

    try:
        weapon = int(input())
    except:
        print("invalid selection")
        continue

    print()

    battery = numericalInput("Enter your 8 figure battery grid reference \n")
    if len(battery) != 8:
            print("invalid grid reference")
            continue

    if weapon == index:
        #Calibrate a weapon

        name = input("Enter the name of the weapon you wish to calibrate\n")
        if name not in weapons.keys():
            weapons[name] = [name]
            weapons[name].append(input("Enter the number of firing speeds for the " + name + "\n"))
            for i in range(0, int(weapons[name][1])):
                #Create entries to fill in during testing
                weapons[name].append("")
                weapons[name].append("")

        h2 = int(numericalInput("Enter your elevation \n"))
        calibration = {}
        for i in range(0, int(weapons[name][1])):
            clear()
            print("Firing Speed " + str(i))
            target = numericalInput("Please fire at bearing 180 and angle 80, and record the 8-figure grid reference where the shell lands here\n")
            h1 = int(numericalInput("Enter the elevation where the shell landed\n"))
            A = calcA(target, battery)
            B = calcB(target, battery)
            q = calcQ(target, battery)
            x = calcRange(A, B)
            y = h1 - h2
            g = 9.80665
            v = calcMuzzleVelocity(g, x, 80, y)
            muzzleVelocity = round(v, 2)
            minRange = int(x)
            maxRange = int(calcFireRange(v, g, 45, y))
            weapons[name][2 + i] = str(minRange) + " - " + str(maxRange)
            weapons[name][int(weapons[name][1]) + 2 + i] = str(muzzleVelocity)

        #Write calibration to velocities.txt file
        with open('velocities.txt', 'w') as f:
            for wep in weapons.keys():
                f.write('\n')
                for prop in weapons[wep]:
                    f.write(prop + '\n')

        continue
    else:
        try:
            selected = selection[weapon]
        except:
            print("invalid selection")
            print()
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
            v = 0

            for i in range(0, int(weapons[selected][1])):
                range = weapons[selected][i + 2]
                range = range.split(' - ')
                if x < int(range[0]):
                    print("Target is too close to battery")
                    break
                elif int(range[0]) <= x <= int(range[1]):
                    v = float(weapons[selected][int(weapons[selected][1]) + 2 + i])
                    break

            #Calculate estimate of theta for estimate of Eotvos effect
            thetas = calcTheta(v, g, x, y)
            eotvos = (calcEotvos(bearing, v, theta = thetas["high"]) + calcEotvos(bearing, v, theta = thetas["low"])) / 2.0
            g += eotvos

            angles = calcTheta(v, g, x, y)

            hightime = calcTime(x, v, angles["high"])
            lowtime = calcTime(x, v, angles["low"])

            clear()

            print("FIRING SOLUTION")
            print()
            print("Range:", x)
            print("Bearing:", bearing)
            print("High Angle:", math.degrees(angles["high"]))
            print("ETA:", hightime, "seconds")
            print("Low Angle:", math.degrees(angles["low"]))
            print("ETA:", lowtime, "seconds")
            print()

            more = numericalInput("Enter new target? 1/0 \n")
            if int(more) == 0:
                firing = False
                clear()
