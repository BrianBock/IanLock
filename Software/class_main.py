import qwiic_serlcd
import qwiic_keypad
import time
from motor import StepperMotor
from ultrasound import Ultrasound
# import sys
import RPi.GPIO as GPIO
import threading


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
            raise RuntimeError("The LCD is not connected")
        self.LCD.clearScreen()
        self.LCD.setFastBacklight(255, 255, 255)  # turn the back light on full white

        # Set up Keypad
        self.keypad = qwiic_keypad.QwiicKeypad()
        if not self.keypad.connected:
            print("The Qwiic Keypad isn't connected to the system. Please check your connection")
            raise RuntimeError("The Keypad is not connected")
        self.keypad.begin()

        self.lock_status = "UNLOCKED"
        self.door_status = "UNKNOWN"
        self.update_door_status()
        self.last_nearby = None
        self.nearby = True
        self.scan = True
        self.can_sleep = False

    def update_door_status(self):
        """Queries door switch to see if door is open or closed"""
        reed_switch = GPIO.input(self.door_switch_pin)
        door_switch = {0: "OPEN", 1: "CLOSED"}
        self.door_status = door_switch[reed_switch]

    def LCDclearprint(self, msg):
        """Clear the LCD and print the message to the screen"""
        self.LCD.clearScreen()
        self.LCD.print(msg)

    def update_screen_status(self):
        """Update the information on screen to reflect the current door and lock status"""
        msg = "Door: +" + self.door_status + "\nLock: +" + self.lock_status
        self.LCDclearprint(msg)

    def lock(self):
        """Lock the door"""
        if self.door_status is "OPEN":
            print("Door is open. You cannot lock an open door. Please close the door and try again.")
            self.lock_status = "UNLOCKED"
        if self.lock_status is "UNLOCKED":
            self.motor.rotate(self.motor.ccw, 360)
            print("Door is locked")
            self.lock_status = "LOCKED"
            self.update_screen_status()
        else:
            print("The door is already locked")

    def unlock(self):
        """Unlock the door"""
        if self.lock_status is "LOCKED":
            self.motor.rotate(self.motor.cw, 360)
            print("Door is unlocked")
            self.lock_status = "UNLOCKED"
            self.update_screen_status()
        else:
            print("The door is already unlocked")

    def sleep(self):
        """Turn off the display"""
        self.LCDclearprint("Goodbye")
        time.sleep(1)
        self.LCD.noDisplay()

    def wakeup(self):
        """Turn on the display"""
        self.LCD.display()
        self.LCD.setFastBacklight(255, 255, 255)
        self.LCDclearprint("Hello!")
        time.sleep(.5)
        self.update_screen_status()

    def check_nearby(self):
        """Determine if someone is nearby (closer than a threshold)"""
        max_dist = 20  # cm
        dist = self.ultrasound.get_distance()
        self.nearby = (dist < max_dist)
        if self.nearby:
            self.last_nearby = time.time()

    def keep_checking_nearby(self):
        """Call "check_nearby' all the time. If not nearby for at least timeout, go to sleep"""
        timeout = 20  # seconds
        while self.scan:
            self.check_nearby()
            time.sleep(.1)
            if not self.nearby and self.last_nearby - time.time() > timeout:
                self.sleep()

    def thread_nearby(self):
        self.montior_thread = threading.Thread(target=keep_checking_nearby)
        self.monitor_thread.start()

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
