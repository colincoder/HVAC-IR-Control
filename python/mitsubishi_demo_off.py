#!/bin/python

"""
Demo Mitsubishi HVAC
"""
import time
import datetime
from hvac_ircontrol.ir_sender import LogLevel
from hvac_ircontrol.mitsubishi import Mitsubishi, ClimateMode, FanMode, VanneVerticalMode, VanneHorizontalMode, ISeeMode, AreaMode, PowerfulMode, PowerMode

if __name__ == "__main__":
    while True:
        print("=======================================================")
        print("Power OFF")
        HVAC = Mitsubishi(22, LogLevel.ErrorsOnly)  #Minimal, Normal, Verbose
        HVAC.power_off(ClimateMode.Cold)
        print("Wait 2 secs ...")
        time.sleep(2)
        exit()
        print("It's gonna get cold here !")
        HVAC.send_command(
            climate_mode=ClimateMode.Cold,
            temperature=18,
            fan_mode=FanMode.Auto,
            vanne_vertical_mode=VanneVerticalMode.Auto,
            vanne_horizontal_mode=VanneHorizontalMode.NotSet,
            isee_mode=ISeeMode.ISeeOn,
            area_mode=AreaMode.Full,
            powerful=PowerfulMode.PowerfulOn
            )
        exit()
        print("=======================================================")
        print("Go dormant for 30 secs ...")
        time.sleep(25)

