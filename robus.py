from main import PROJECT_BASE_PATH
import pathlib
import os
from ball import *
from car import *
from color_sensor import *
from distance_sensor import *
from framer import *


def get_car_color_sensor():
    absolute_image_path = os.path.join(PROJECT_BASE_PATH, pathlib.Path('path.png'))
    floor_matrix = np.asarray(Image.open(absolute_image_path).convert('L'))
    floor = Floor(floor_matrix)

    blender_img = bpy.data.objects["Image"]
    blender_img.scale = floor.get_scale()
    blender_img.rotation_euler = [0, 0, np.pi / 2]
    blender_img.location = [0, 0, -37]

    return ColorSensor(position_offsets=[
        [-40, 97, 0],
        [-20, 97, 0],
        [0, 97, 0],
        [20, 97, 0],
        [40, 97, 0]
    ], floor=floor)

    ds = DistanceSensor()

def main():
    car = Car("Car", get_car_color_sensor(),ds)
    car.set_location([0, 0, 0])
    car.set_rotation([np.pi/2, 0, 0])
    car.velocity = [0, 150, 0]
    car.acceleration = [0, 0, 0]
    car.angular_velocity = [0, 0, 3.14/10]

    ball = Ball("Ball", car)
    ball.set_location([0, 30, 45])
    ball.velocity = [-1, 4, 2]
    ball.acceleration = [0.4, 2, 6]

    f = Framer()
    f.entities = {
        "car": car,
        "ball": ball,
        "test": Entity(blender_object_name="Test")
    }
    f.clear_animation()
    f.play_animation(second=30)

