import RPi.GPIO as GPIO
import time


# From Dr. Devoe's ENME489B Mechatronics Course
################################
# Set up the Stepper Motor ###
################################
def delay_us(tus):  # use microseconds to improve time resolution
    end_time = time.time() + float(tus) / 1000000.0
    while time.time() < end_time:
        pass


class StepperMotor:
    def __init__(self, pins):
        GPIO.setmode(GPIO.BCM)
        self.pins = pins  # controller inputs: in1, in2, in3, in4
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT, initial=0)
        # Define the pin sequence for counter-clockwise motion, noting that
        # two adjacent phases must be actuated together before stepping to
        # a new phase so that the rotor is pulled in the right direction:
        self.ccw = [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1],
               [1, 0, 0, 1]]

        # Make a copy of the ccw sequence. This is needed since simply
        # saying cw = ccw would point both variables to the same list object:
        self.cw = self.ccw[:]  # use slicing to copy list (could also use ccw.copy() in Python 3)
        self.cw.reverse()  # reverse the new cw sequence

    def rotate(self, direction, deg):  # rotation direction: dir = cw or ccw
        steps = int(deg*512/360)
        for i in range(steps):  # full revolution (8 cycles/rotation * 64 gear ratio)
            for half_step in range(8):  # 8 half-steps per cycle
                for pin in range(4):
                    GPIO.output(self.pins[pin], direction[half_step][pin])
                delay_us(1000)
