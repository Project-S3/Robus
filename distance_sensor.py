import time

import numpy as np
import RPi.GPIO as GPIO


class DistanceSensor:
    def __init__(self, channel=20):
        self.channel = channel
        GPIO.setmode(GPIO.BCM)

    def read(self, n = 16):
        distances = np.array([self._read_distance() for _ in range(n)])
        distances_no_err = [e for e in distances if e > 0]
        return np.average(distances_no_err)

    def read_from_file(self):
        try:
            with open("/tmp/robus/dist", "r") as f:
                while True:
                    dist = f.read()
                    if dist:
                        return float(dist)
        except FileNotFoundError:
            return 1000

    def _read_distance(self, timeout=15e-3):
        GPIO.setup(self.channel, GPIO.OUT)
        # Reset
        GPIO.output(self.channel, 0)
        time.sleep(50e-6)
        # Pulse
        GPIO.output(self.channel, 1)
        time.sleep(10e-6)
        GPIO.output(self.channel, 0)
        # Read Echo Lengh
        GPIO.setup(self.channel, GPIO.IN)
        timeout_time = time.time()
        # Pulse Start Time
        pulse_start_time = time.time()
        while GPIO.input(self.channel) == 0:
            if pulse_start_time - timeout_time > timeout: return -1
            pulse_start_time = time.time()
        # Pulse Start Time
        pulse_end_time = time.time()
        while GPIO.input(self.channel) == 1:
            if pulse_end_time - timeout_time > timeout: return -1
            pulse_end_time = time.time()
        # Claculate Distance
        duration = pulse_end_time - pulse_start_time
        distance = duration * 343e2 / 2
        return distance