import numpy as np

from ball import *
from car import *
from framer import *


def main():
    print("hello world")

    car = Car("Car")
    car.set_location([0, 0, 0])
    car.set_rotation([np.pi/2, 0, 0])
    car.velocity = [0, 0, 0]
    car.acceleration = [0, 20, 0]
    car.angular_velocity = [0, 0, 3.14/1000]

    ball = Ball("Ball", car)
    ball.set_location([0, 30, 45])
    # ball.velocity = [-1, 4, 2]
    # ball.acceleration = [0.4, 2, 6]

    f = Framer()
    f.entities = {
        "car": car,
        "ball": ball
    }
    f.clear_animation()
    f.play_animation(second=10)

