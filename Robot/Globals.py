from enum import Enum,IntEnum

class Direction(IntEnum):
    FRONT = 0,
    BACK  = 180

class GripperState(Enum):
    Closed = 0,
    Open  = 1

class GamepieceMode(Enum):
    Cube = 0,
    Cone  = 1

class Globals:
    class Robot:
        turret_side = Direction.FRONT
        gripper_state = GripperState.Open
        gamepice_mode =  GamepieceMode.Cube