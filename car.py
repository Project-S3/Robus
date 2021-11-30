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

    car.mef_control.update()


class Car(framer.Entity):
    def __init__(self, blender_object_name, color_sensor, distance_sensor):
        super().__init__(blender_object_name)
        self.update_callback = obj_update
        self.color_sensor = color_sensor
        self.distance_sensor = distance_sensor
        self.mef_control = MefControl(self)
        self.wheel_angle = 0

    def get_speed(self):
        return np.linalg.norm(self.velocity)

    def set_speed(self, speed):
        if self.get_speed() == 0:
            self.velocity = [speed, 0, 0]
        else:
            self.velocity = utils.set_module_vector(self.velocity, speed)
        self._update_angular_speed()

    def set_front_wheel_angle(self, angle):
        self.wheel_angle = angle
        self._update_angular_speed()

    def _update_angular_speed(self):
        distance_GO = np.sqrt(np.power(140*np.tan(np.deg2rad(90-self.wheel_angle)) + 135/2, 2) + np.power(140/2, 2))
        #print(f"distance_GO : {distance_GO}")
        angular_speed = self.get_speed() / distance_GO
        if self.wheel_angle < 0:
            angular_speed = angular_speed * -1
        #print(f"angular_speed : {angular_speed}")
        self.angular_velocity = [0, 0, angular_speed]

