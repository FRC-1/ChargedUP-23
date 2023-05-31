from typing import Awaitable
from Subsystems.GripperSubsystem import GripperSubsystem
from Commands.base.CommandBase import CommandBase, CommandPhase
from Constants import Constants
GripperConstants = Constants.Robot.GripperSubsystem
from Globals import Globals, GamepieceMode, GripperState


class GripperDefaultCommand(CommandBase):
    def __init__(self, gripperSubsystem:GripperSubsystem, conditionSupplier: Awaitable, priority: int):
        super().__init__([gripperSubsystem], conditionSupplier, priority)
        
        self.gripperSubsystem = gripperSubsystem
        self.setSetpoint()

    async def init(self):
        pass
        
    async def execute(self):
        self.setSetpoint()
        await self.gripperSubsystem.setDistance(self.gripperSetpoint)

    async def isFinished(self):
        await self.execute()
        return False
    
    def setSetpoint(self):
        if(Globals.Robot.gamepice_mode == GamepieceMode.Cone):
            if(Globals.Robot.gripper_state == GripperState.Closed):
                self.gripperSetpoint = GripperConstants.cone_closed
            else:
                self.gripperSetpoint = GripperConstants.cone_open
        else:
            if(Globals.Robot.gripper_state == GripperState.Closed):
                self.gripperSetpoint = GripperConstants.cube_closed
            else:
                self.gripperSetpoint = GripperConstants.cube_open
                
    async def end(self):
        pass