import qwiic_serlcd
import qwiic_keypad
import time
from motor import StepperMotor
from ultrasound import Ultrasound
import sys
import RPi.GPIO as GPIO


class ApplePi:
    def __init__(self):
        # Define GPIO Pins
        us_trig_pin = 24
        us_echo_pin = 25
        motor_pins = [14, 15, 18, 23]
        self.motor = StepperMotor(motor_pins)  # set up motor
        self.ultrasound = Ultrasound(us_trig_pin, us_echo_pin)  # set up ultrasound
        self.door_switch_pin = 12
        GPIO.setup(self.door_switch_pin, GPIO.IN)

        # Set up LCD
        self.LCD = qwiic_serlcd.QwiicSerlcd()  # set up the LCD
        if not self.LCD.connected:
            print("The Qwiic SerLCD device isn't connected to the system. Please check your connection")
            sys.exit("The LCD is not connected")
        self.LCD.clearScreen()
        self.LCD.setFastBacklight(255, 255, 255)  # turn the back light on full white

        # Set up Keypad
        self.keypad = qwiic_keypad.QwiicKeypad()
        if not self.keypad.connected:
            print("The Qwiic Keypad isn't connected to the system. Please check your connection")
            sys.exit("The Keypad is not connected")
        self.keypad.begin()

        self.lock_status = "UNLOCKED"
        self.door_status = "UNKNOWN"
        self.update_door_status()

    def update_door_status(self):
        reed_switch = GPIO.input(self.door_switch_pin)
        door_switch = {0: "OPEN", 1: "CLOSED"}
        self.door_status = door_switch[reed_switch]
        return

    def LCDclearprint(self, msg):
        self.LCD.clearScreen()
        self.LCD.print(msg)
        return

    def update_screen_status(self):
        msg = "Door: +" + self.door_status + "\nLock: +" + self.lock_status
        self.LCDclearprint(msg)

    def change_door(self, cmd):
        if self.door_status is "OPEN" and cmd is "LOCK":
            print("Door is open. You cannot lock an open door. Please close the door and try again.")
            self.lock_status = "UNLOCKED"
            return

        if cmd is "LOCK":
            print("Locking the door...")
            self.motor.rotate(self.motor.cw, 360)
            print("Door is locked")
            self.lock_status = "LOCKED"

        elif cmd is "UNLOCK":
            print("Unlocking the door...")
            self.motor.rotate(self.motor.ccw, 360)
            print("Door is unlocked")
            self.lock_status = "UNLOCKED"

        print("Door is " + self.lock_status)
        self.LCDclearprint("Door: " + self.lock_status)



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


# # change_door(command, door_status)
# command = "LOCK"
# door_status = "OPEN"
# lock_status = "LOCKED"
