from color_sensor import ColorSensor
from distance_sensor import DistanceSensor
from wheels import Wheels

class Car:
    def __init__(self):
        self.wheels = Wheels()
        self._color_sensor = ColorSensor()
        self._distance_sensor = DistanceSensor()
    
    def read_colors(self):
        return self._color_sensor.read()

    def read_distance(self):
        # return self._distance_sensor.read()
        return self._distance_sensor.read_from_file()
            
    def reset(self):
        self.wheels.set_speed(0, acceleration_dt=None)
        self.wheels.set_angle(0, acceleration_dt=None)


