from typing import Awaitable
from Subsystems.GripperSubsystem import GripperSubsystem
from Commands.base.CommandBase import CommandBase, CommandPhase
from Constants import Constants
GripperConstants = Constants.Robot.GripperSubsystem
from Globals import Globals, GamepieceMode, GripperState


class SwitchRobotMode(CommandBase):
    def __init__(self, gripperSubsystem:GripperSubsystem, conditionSupplier: Awaitable, priority: int):
        super().__init__([gripperSubsystem], conditionSupplier, priority)
        
    async def init(self):
        Globals.Robot.gamepice_mode  = GamepieceMode.Cone if GamepieceMode.Cube else GamepieceMode.Cube

    async def isFinished(self): 
        return True
                
    async def end(self):
        pass