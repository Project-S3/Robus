import numpy as np

import framer
import utils


def obj_update(car, time, entities, changes):
    car.velocity = utils.rotate_vector(car.velocity, changes["delta_rotation"])
    car.acceleration = utils.rotate_vector(car.acceleration, changes["delta_rotation"])

    lines = car.color_sensor.read(car.get_location(), car.get_rotation()[2])

    print(lines)

    if len(list(filter(lambda x: x < 50, lines))) == 5:
        # car.set_speed(0)
        print("Finish Line")

    if len(list(filter(lambda x: x > 240, lines))) == 5:
        # car.set_speed(0)
        print("Line Lost")


class Car(framer.Entity):
    def __init__(self, blender_object_name, color_sensor):
        super().__init__(blender_object_name)
        self.update_callback = obj_update
        self.color_sensor = color_sensor

    def get_speed(self):
        return np.linalg.norm(self.velocity)

    def set_speed(self, speed):
        if self.get_speed() == 0:
            self.velocity = [speed, 0, 0]
        else:
            self.velocity = utils.set_module_vector(self.velocity, speed)

    def set_front_wheel_angle(self):
        pass

