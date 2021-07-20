import qwiic_serlcd
import time
from motor import StepperMotor
from ultrasound import Ultrasound

# Define GPIO Pins
us_trig_pin = 24
us_echo_pin = 25
motor_pins = [14, 15, 18, 23]

####################
# Set up the LCD ###
####################

myLCD = qwiic_serlcd.QwiicSerlcd()  # set up the LCD
myLCD.clearScreen()
myLCD.setFastBacklight(255, 255, 255)  # turn the back light on full white

motor = StepperMotor(motor_pins)  # set up motor
ultrasound = Ultrasound(us_trig_pin, us_echo_pin)  # set up ultrasound

command = "LOCK"
door_status = "OPEN"
distance = ultrasound.get_distance()

def LCDclearprint(msg):
    myLCD.clearScreen()
    myLCD.print(msg)
    return


def change_door(cmd, door_stat):
    if door_stat is "OPEN" and cmd is "LOCK":
        print("Door is open. You cannot lock an open door. Please close the door and try again.")
        lock_status = "UNLOCKED"
        return lock_status

    if cmd is "LOCK":
        print("Locking the door...")
        motor.rotate(motor.cw, 360)
        print("Door is locked")
        lock_status = "LOCKED"

    elif cmd is "UNLOCK":
        print("Unlocking the door...")
        motor.rotate(motor.ccw, 360)
        print("Door is unlocked")
        lock_status = "UNLOCKED"

    print("Door is " + lock_status)
    LCDclearprint("Door: " + lock_status)
    return lock_status

# myLCD.display() #turn on display
# time.sleep(1)
# myLCD.noDisplay() # turn off display

# while True:
#     distance = getDist()
#     if distance > 20:
#         LCDclearprint("Goodbye")
#         time.sleep(1)
#         myLCD.noDisplay()  # turn off display
#
#     else:
#         print("Hello there!")


# change_door(command, door_status)
