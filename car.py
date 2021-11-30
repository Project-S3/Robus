import numpy as np
import bpy
import framer
import distance_sensor as ds
from mathutils import Vector
import utils
from mef_control import *


def obj_update(car, time, entities, changes):
    car.velocity = utils.rotate_vector(car.velocity, changes["delta_rotation"])
    car.acceleration = utils.rotate_vector(car.acceleration, changes["delta_rotation"])

    colorSensorValues = car.color_sensor.read(car.get_location(), car.get_rotation()[2])

    car.mef_control.update()


class Car(framer.Entity):
    def __init__(self, blender_object_name, color_sensor, distance_sensor):
        super().__init__(blender_object_name)
        self.update_callback = obj_update
        self.color_sensor = color_sensor
        self.distance_sensor = distance_sensor
        self.mef_control = MefControl(self)

    def get_speed(self):
        return np.linalg.norm(self.velocity)

    def set_speed(self, speed):
        if self.get_speed() == 0:
            self.velocity = [speed, 0, 0]
        else:
            self.velocity = utils.set_module_vector(self.velocity, speed)

    def set_front_wheel_angle(self):
        pass
