from typing import Tuple, Dict, Any

__glob: Dict[str, Any] = {'MAX_BRIGHTNESS_LEVEL': 7}

def set_var(key, value):
    __glob[key] = value

def get_var(key):
    return __glob[key]

def set_max_brightness_level(value: int):
    set_var('MAX_BRIGHTNESS_LEVEL', value)

def get_max_brightness_level() -> int:
    return get_var('MAX_BRIGHTNESS_LEVEL')


import numpy as np
from warnings import warn
RIGHT_HAND_COORDINATE: bool = True
COORDINATOR: Tuple[str, str, str] = ("x+", "y+", "z+")
COORDINATE_MAP: np.ndarray = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

def set_control_coordinator(x: str = "x+", y: str = "y+", z: str = "z+", camera=None):
    global RIGHT_HAND_COORDINATE, COORDINATOR, COORDINATE_MAP
    def get_vec(s: str) -> np.ndarray:
        if s == "x+":
            return np.array([1, 0, 0])
        if s == "x-":
            return np.array([-1, 0, 0])
        if s == "y+":
            return np.array([0, 1, 0])
        if s == "y-":
            return np.array([0, -1, 0])
        if s == "z+":
            return np.array([0, 0, 1])
        if s == "z-":
            return np.array([0, 0, -1])
        raise ValueError("Invalid direction")
    mat = np.array([get_vec(x), get_vec(y), get_vec(z)])
    RIGHT_HAND_COORDINATE = int(np.linalg.det(mat)) > 0
    COORDINATOR = (x, y, z)
    COORDINATE_MAP = mat
    if camera is not None:
        camera.glu_look_at(up=tuple(mat[2].tolist()))
        camera.calc_sight()

def get_control_coordinator():
    return RIGHT_HAND_COORDINATE, COORDINATOR, COORDINATE_MAP