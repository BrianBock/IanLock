import RPi.GPIO as GPIO
import time


# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

class Ultrasound:
    def __init__(self, trig, echo):
        GPIO.setmode(GPIO.BCM)
        self.trig = trig
        self.echo = echo

        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, False)
        print("Waiting For Sensor To Settle")

        time.sleep(2)

    def get_distance(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        GPIO.output(self.trig, False)
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start

        distance = round(pulse_duration * 17150, 2)

        print("Distance:", distance, "cm")
        return distance
