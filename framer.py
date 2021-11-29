import bpy
import numpy as np


class Framer:
    def __init__(self):
        self.entities = {}
        bpy.context.scene.render.fps = 60

    def play_animation(self, second):
        time = 0
        current_frame = 1
        max_frame = second * bpy.context.scene.render.fps
        bpy.context.scene.frame_end = max_frame + 15
        while current_frame <= max_frame:
            print(f"### CURRENT FRAME ### -> {current_frame}")
            dt = 1 / bpy.context.scene.render.fps
            for e in list(self.entities.values()):

                dv, dl = e.update_location_frame(dt)
                dr = e.update_rotation_frame(dt)

                if e.update_callback is not None: e.update_callback(e, time, self.entities, {
                    "delta_velocity": dv,
                    "delta_location": dl,
                    "delta_rotation": dr
                })
                e.blender_object.keyframe_insert(data_path="location", frame=current_frame)
                e.blender_object.keyframe_insert(data_path="rotation_euler", frame=current_frame)
            time += dt
            current_frame += 1

    def clear_animation(self):
        for e in list(self.entities.values()):
            obj = e.blender_object
            obj.animation_data_clear()


class Entity:
    def __init__(self, blender_object_name):
        obj = bpy.data.objects[blender_object_name]
        self.name = blender_object_name
        self.blender_object = obj
        self.velocity = [0, 0, 0]
        self.acceleration = [0, 0, 0]
        self.angular_velocity = [0, 0, 0]
        self.update_callback = None

    def update_location_frame(self, dt):
        dv = np.multiply(self.acceleration, dt)
        dl = np.multiply(self.velocity, dt) + np.multiply(self.acceleration, np.power(dt, 2))
        self.velocity = np.add(self.velocity, dv)
        self.blender_object.location = np.add(self.blender_object.location, dl)
        return dv, dl

    def update_rotation_frame(self, dt):
        dr = np.multiply(self.angular_velocity, dt)
        self.blender_object.rotation_euler = np.add(self.blender_object.rotation_euler, dr)
        return dr

    def get_location(self):
        return self.blender_object.location

    def set_location(self, location):
        self.blender_object.location = location

    def get_rotation(self):
        return self.blender_object.rotation_euler

    def set_rotation(self, rotation):
        self.blender_object.rotation_euler = rotation

    def get_direction(self):
        if self.velocity[1] == 0:
            direction = 0
        else:
            direction = np.arctan(self.velocity[0]/self.velocity[1])
        if self.velocity[0] < 0:
            direction += np.pi
        return direction

