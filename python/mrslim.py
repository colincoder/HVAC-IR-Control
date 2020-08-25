#! /usr/bin/sudo /usr/bin/python
import sys
import time
import datetime
import pickle
import os.path
from hvac_ircontrol.ir_sender import LogLevel
from hvac_ircontrol.mitsubishi import Mitsubishi, ClimateMode, FanMode, VanneVerticalMode, VanneHorizontalMode, ISeeMode, AreaMode, PowerfulMode

def sendCommand(temperature, speed, verticalvane, powerfulmode):
    MRSLIM.send_command(
        climate_mode=ClimateMode.Cold,
        temperature=temperature,
        fan_mode=speed,
        vanne_vertical_mode=verticalvane,
        vanne_horizontal_mode=VanneHorizontalMode.NotSet,
        isee_mode=ISeeMode.ISeeOff,
        area_mode=AreaMode.NotSet,
        powerful=powerfulmode
        )
#  Save the last calls parameters
    print (temperature, speed, verticalvane, powerfulmode)
    # Saving the objects:
    with open(fname, 'wb') as f:
        pickle.dump([temperature,speed,verticalvane,powerfulmode], f)
        

###################################################################################
if __name__ == "__main__":
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)
    #print 'Argument List:', sys.argv[1]
    ver = sys.version_info[0]     
    fname = 'mrslim' + str(ver) + '.vars'
#  Get the previous call's parameters or set defaults if they don't exist
    if os.path.isfile(fname):
        #Getting back the objects:
        with open(fname,"rb") as f:
            temperature,speed,verticalvane,powerfulmode = pickle.load(f)
    else:           #defaults
        temperature = 22
        speed = FanMode.Speed1
        verticalvane = VanneVerticalMode.Swing
        powerfulmode = PowerfulMode.PowerfulOff


    MRSLIM = Mitsubishi(22, LogLevel.ErrorsOnly)  #ErrorsOnly, Minimal, Normal, Verbose
    fanmodes = [FanMode.Speed1,FanMode.Speed2,FanMode.Speed3,FanMode.Auto]
    verticalvanemodes = [VanneVerticalMode.Auto, VanneVerticalMode.Top, VanneVerticalMode.MiddleTop,
        VanneVerticalMode.Middle, VanneVerticalMode.MiddleBottom, VanneVerticalMode.Bottom, VanneVerticalMode.Swing]
    powerfulmodes = [PowerfulMode.PowerfulOff, PowerfulMode.PowerfulOn]

    if len(sys.argv) < 2:
        print ("Usage: mrslim.py <arg1> <arg2>")
        print ("arg1: off | on | temperature | speed | verticalvane | powerfulmode")
        print ("arg2: for temperature 64 to 90")
        print ("arg2: for speed 1 to 4")
        print ("\t1 = Low")
        print ("\t2 = Medium")
        print ("\t3 = High")
        print ("\t4 = Auto")
        print ("arg2: for verticalvane 1 to 7")
        print ("\t1 = Auto")
        print ("\t2 = Top")
        print ("\t3 = MiddleTop")
        print ("\t4 = Middle")
        print ("\t5 = MiddleBottom")
        print ("\t6 = Bottom")
        print ("\t7 = Swing")
        print ("arg2: for powerfulmode 1 or 2")
        print ("\t1 = Off")
        print ("\t2 = On")
        exit()
    if sys.argv[1] == 'off':
        MRSLIM.power_off(ClimateMode.Cold)
        print ("Power Off")
    elif sys.argv[1] == 'on':
        if (len(sys.argv) == 6): #there are initial values on the line
            temperature = int(round((int(sys.argv[2]) - 32) * 5/9,0))
            speed = fanmodes[int(sys.argv[3]) - 1]
            verticalvane = verticalvanemodes[int(sys.argv[4]) - 1]
            powerfulmode = powerfulmodes[int(sys.argv[5]) - 1]
        sendCommand(
            temperature,
            speed,
            verticalvane,
            powerfulmode
            )
    elif sys.argv[1] == 'temperature':
        if len(sys.argv) < 3:
            print ("Temperature value missing")
            exit()
        temperature = int(sys.argv[2])
        if temperature < 64 or temperature > 90:
            print ("Temperature value must be 64F thru 90F")
            exit()
        temperature = int(round((temperature - 32) * 5/9,0))
        sendCommand(
            temperature,
            speed,
            verticalvane,
            powerfulmode
            )
    elif sys.argv[1] == 'speed':
        if len(sys.argv) < 3:
            print ("Speed value missing")
            exit()
        speed = int(sys.argv[2]) - 1
        if speed < 0 or speed > 3:
            print ("Speed value must be 1 thru 4")
            exit()
        sendCommand(
            temperature,
            fanmodes[speed],
            verticalvane,
            powerfulmode
            )
    elif sys.argv[1] == 'verticalvane':
        if len(sys.argv) < 3:
            print ("Vertical fan value missing")
            exit()
        verticalvane = int(sys.argv[2]) - 1
        if verticalvane < 0 or verticalvane > 7:
            print ("Vertical Fan Mode value must be 1 thru 7")
            exit()
        sendCommand(
            temperature,
            speed,
            verticalvanemodes[verticalvane],
            powerfulmode
            )
    elif sys.argv[1] == 'powerfulmode':
        if len(sys.argv) < 3:
            print ("Powerful Fan value missing")
            exit()
        powerfulmode = int(sys.argv[2]) - 1
        if powerfulmode < 0 or powerfulmode > 1:
            print ("Powerful Mode value must be 1 or 2")
            exit()
        sendCommand(
            temperature,
            speed,
            verticalvane,
            powerfulmodes[powerfulmode]
            )
##########################################################################################
