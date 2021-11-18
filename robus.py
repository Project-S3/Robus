import bpy
from PIL import Image

from main import PROJECT_BASE_PATH
import pathlib
import os
from ball import *
from car import *
from color_sensor import *
from framer import *

def main():
    floor_matrix = np.asarray(Image.open(os.path.join(PROJECT_BASE_PATH, pathlib.Path('path.png'))).convert('L'))
    floor = Floor(floor_matrix)

    blender_img = bpy.data.objects["Image"]

    blender_img.scale = floor.get_scale()
    blender_img.rotation_euler = [0, 0, np.pi/2]
    blender_img.location = [0, 0, -37]

    cs = ColorSensor(position_offsets=[
        [-40, 97, 0],
        [-20, 97, 0],
        [0, 97, 0],
        [20, 97, 0],
        [40, 97, 0]
    ], floor=floor)

    print("hello world")

    car = Car("Car", cs)
    car.set_location([0, 0, 0])
    car.set_rotation([np.pi/2, 0, 0])
    car.velocity = [0, 150, 0]
    car.acceleration = [0, 0, 0]
    # car.angular_velocity = [0, 0, 3.14/1000]

    ball = Ball("Ball", car)
    ball.set_location([0, 30, 45])
    ball.velocity = [-1, 4, 2]
    ball.acceleration = [0.4, 2, 6]

    te = Entity(blender_object_name="Test")

    f = Framer()
    f.entities = {
        "car": car,
        "ball": ball,
        "test": te
    }
    f.clear_animation()
    f.play_animation(second=30)

