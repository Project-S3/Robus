import bpy
from mathutils import Vector
import numpy as np
from utils import rotate_vector


class DistanceSensor:
    def __init__(self):
        # obj = bpy.data.objects["DistSensor"]
        # code for generation offsets
        # for i, v in enumerate([obj.matrix_world @ Vector(corner) for corner in obj.bound_box]):
        #     print(f"\t[{round(v[0])}, {round(v[1])}, {round(v[2])}]")
        self.position_offsets = [[-89, 108, -1],
                                 [-89, 108, 31],
                                 [-89, 1108, 31],
                                 [-89, 1108, -1],
                                 [89, 108, -1],
                                 [89, 108, 31],
                                 [89, 1108, 31],
                                 [89, 1108, -1]]

    def distance_vec(self, p1, p2):
        return np.linalg.norm(np.subtract(p1, p2))

    def is_in_bounding_vectors(self, vector_check, sensor_points):
        for i in range(0, 3):
            if (vector_check[i] < sensor_points[0][i]
                    and vector_check[i] < sensor_points[1][i]
                    and vector_check[i] < sensor_points[2][i]
                    and vector_check[i] < sensor_points[3][i]
                    and vector_check[i] < sensor_points[4][i]
                    and vector_check[i] < sensor_points[5][i]
                    and vector_check[i] < sensor_points[6][i]
                    and vector_check[i] < sensor_points[7][i]
                    or vector_check[i] > sensor_points[0][i]
                    and vector_check[i] > sensor_points[1][i]
                    and vector_check[i] > sensor_points[2][i]
                    and vector_check[i] > sensor_points[3][i]
                    and vector_check[i] > sensor_points[4][i]
                    and vector_check[i] > sensor_points[5][i]
                    and vector_check[i] > sensor_points[6][i]
                    and vector_check[i] > sensor_points[7][i]):
                return False
        return True

    def select_objects_in_bound(self, sensor_points, car_location):
        """
        :return: object distance in cm or -1 if nothing found
        """
        distances = []
        for obj in bpy.context.scene.objects:
            if self.is_in_bounding_vectors(obj.matrix_world.to_translation(), sensor_points) \
                    and not (obj.name == 'DistSensor' or obj.name == 'Car'):
                dist = self.distance_vec(obj.location, car_location)
                dist = int(dist - 113)
                dist = int(dist / 10)
                print(f"OBJECT DETECTED -> {obj.name} : distance={dist}")
                distances.append(dist)
        return min(distances) if len(distances) > 0 else -1

    def read(self, car_position, car_rotation_z):
        p0 = np.add(car_position, rotate_vector(self.position_offsets[0], [0, 0, car_rotation_z])[0:3])
        p1 = np.add(car_position, rotate_vector(self.position_offsets[1], [0, 0, car_rotation_z])[0:3])
        p2 = np.add(car_position, rotate_vector(self.position_offsets[2], [0, 0, car_rotation_z])[0:3])
        p3 = np.add(car_position, rotate_vector(self.position_offsets[3], [0, 0, car_rotation_z])[0:3])
        p4 = np.add(car_position, rotate_vector(self.position_offsets[4], [0, 0, car_rotation_z])[0:3])
        p5 = np.add(car_position, rotate_vector(self.position_offsets[5], [0, 0, car_rotation_z])[0:3])
        p6 = np.add(car_position, rotate_vector(self.position_offsets[6], [0, 0, car_rotation_z])[0:3])
        p7 = np.add(car_position, rotate_vector(self.position_offsets[7], [0, 0, car_rotation_z])[0:3])

        return self.select_objects_in_bound([p0, p1, p2, p3, p4, p5, p6, p7], car_position)
