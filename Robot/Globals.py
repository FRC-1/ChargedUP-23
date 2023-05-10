from enum import IntEnum

class Direction(IntEnum):
    FRONT = 0,
    BACK  = 180

class Globals:
    class Robot:
        turret_side = Direction.FRONT