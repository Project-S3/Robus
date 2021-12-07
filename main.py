#!/usr/bin/env python3

import traceback

from car import Car
from mef_control import MefControl
import RPi.GPIO as GPIO

RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

if __name__ == "__main__":
    car = Car()
    mef = MefControl(car)
    try:
        finish = False
        while not finish:
            finish = mef.update()
        car.reset()
    except KeyboardInterrupt:
        print("Program manualy terminated")
    except:
        print(RED)
        traceback.print_exc()
        print(ENDC)
        
    finally:
        print(f"{BOLD}Car and GPIO Reset{ENDC}")
        car.reset()
        GPIO.cleanup() 

