import numpy as np


def rotate_vector(vec, rotation):
    v = np.array(vec)
    rx = np.array([[1, 0, 0],
                   [0, np.cos(rotation[0]), -np.sin(rotation[0])],
                   [0, np.sin(rotation[0]), np.cos(rotation[0])]])
    ry = np.array([[np.cos(rotation[1]), 0, np.sin(rotation[1])],
                   [0, 1, 0],
                   [-np.sin(rotation[1]), 0, np.cos(rotation[1])]])
    rz = np.array([[np.cos(rotation[2]), -np.sin(rotation[2]), 0],
                   [np.sin(rotation[2]), np.cos(rotation[2]), 0],
                   [0, 0, 1]])
    v = rx @ v
    v = ry @ v
    v = rz @ v
    return v.tolist()


def set_module_vector(vec, new_module):
    if new_module == 0: return [0, 0, 0]
    factor = np.linalg.norm(vec) / new_module
    return np.divide(vec, factor)
