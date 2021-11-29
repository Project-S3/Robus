import bpy
from mathutils import Vector
import numpy as np
from utils import rotate_vector

car = bpy.data.objects["Car"]

#sensor_corners = [distanceSensor.matrix_world @ Vector(corner) for corner in distanceSensor.bound_box]
class DistanceSensor:
    def __init__(self):
        distanceSensor = bpy.data.objects["DistSensor"]
        self.position_offsets = [distanceSensor.matrix_world @ Vector(corner) for corner in distanceSensor.bound_box]

    def distance_vec(self, point1: Vector, point2: Vector) -> float:
        """Calculate distance between two points."""
        return (point2 - point1).length

    def IsInBoundingVectors(self, vector_check, vector1, vector2, vector3, vector4, vector5, vector6, vector7, vector8):
        for i in range(0, 3):
            if (vector_check[i] < vector1[i] and vector_check[i] < vector2[i] and vector_check[i] < vector3[i] and vector_check[i] < vector4[i] and vector_check[i] < vector5[i] and vector_check[i] < vector6[i] and vector_check[i] < vector7[i] and vector_check[i] < vector8[i]
                    or vector_check[i] > vector1[i] and vector_check[i] > vector2[i] and vector_check[i] > vector3[i] and vector_check[i] > vector4[i] and vector_check[i] > vector5[i] and vector_check[i] > vector6[i] and vector_check[i] > vector7[i] and vector_check[i] > vector8[i]):
                return False
        return True

    def SelectObjectsInBound(self, vector1, vector2, vector3, vector4, vector5, vector6, vector7, vector8):

        for obj in bpy.context.scene.objects:
            #print(obj.matrix_world.to_translation())
            #print(vector1)
            if obj.name == "Obstacle2":
                print(obj.name)
                print(obj.matrix_world.to_translation())
                print("vec1: ", vector1)
                print("vec2: ", vector2)
                print("vec3: ", vector3)
                print("vec4: ", vector4)
                print("vec5: ", vector5)
                print("vec6: ", vector6)
                print("vec7: ", vector7)
                print("vec8: ", vector8)


            if (self.IsInBoundingVectors(obj.matrix_world.to_translation(), vector1, vector2, vector3, vector4, vector5, vector6, vector7, vector8) and obj.name != 'DistSensor'):
                obj.select_set(True)
                print("OPOPOPOPOPOPOP")
                print(obj.name)
                print(obj.matrix_world.to_translation())
                print(car.location)
            else:
                obj.select_set(False)

    def read(self, car_position, car_rotation_z):
        #car = (car_position[0], car_position[1], car_position[2])
        car = Vector((car_position[0], car_position[1], car_position[2]))
        print("car pos:", car_position)
        p0 = np.add(car, rotate_vector(self.position_offsets[0], [0, 0, car_rotation_z])[0:3])
        p1 = np.add(car, rotate_vector(self.position_offsets[1], [0, 0, car_rotation_z])[0:3])
        p2 = np.add(car, rotate_vector(self.position_offsets[2], [0, 0, car_rotation_z])[0:3])
        p3 = np.add(car, rotate_vector(self.position_offsets[3], [0, 0, car_rotation_z])[0:3])
        p4 = np.add(car, rotate_vector(self.position_offsets[4], [0, 0, car_rotation_z])[0:3])
        p5 = np.add(car, rotate_vector(self.position_offsets[5], [0, 0, car_rotation_z])[0:3])
        p6 = np.add(car, rotate_vector(self.position_offsets[6], [0, 0, car_rotation_z])[0:3])
        p7 = np.add(car, rotate_vector(self.position_offsets[7], [0, 0, car_rotation_z])[0:3])

        v0 = Vector((p0[0], p0[1], p0[2]))
        v1 = Vector((p1[0], p1[1], p1[2]))
        v2 = Vector((p2[0], p2[1], p2[2]))
        v3 = Vector((p3[0], p3[1], p3[2]))
        v4 = Vector((p4[0], p4[1], p4[2]))
        v5 = Vector((p5[0], p5[1], p5[2]))
        v6 = Vector((p6[0], p6[1], p6[2]))
        v7 = Vector((p7[0], p7[1], p7[2]))

        #print(self.position_offsets[0])
        #bpy.data.objects["Test"].location = [p2[0], p2[1], 20]
        self.SelectObjectsInBound(v0, v1, v2, v3, v4, v5, v6, v7)
        return "allo"