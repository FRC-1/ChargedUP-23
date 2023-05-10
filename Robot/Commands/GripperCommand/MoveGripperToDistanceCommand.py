import asyncio
from typing import Awaitable
from Subsystems.GripperSubsystem import GripperSubsystem
from Commands.base.CommandBase import CommandBase, CommandPhase

class MoveGripperToDistance(CommandBase):
    def __init__(self, gripperSubsystem:GripperSubsystem, conditionSupplier: Awaitable, priority: int,target_distance):
        super().__init__([gripperSubsystem], conditionSupplier, priority)
        
        self.gripperSubsystem = gripperSubsystem
        self.target_distance = target_distance

    async def init(self):
        await self.gripperSubsystem.setDistance(self.target_distance)
        
    async def isFinished(self):
        return abs(self.gripperSubsystem.gripperStepper.currentSteps - self.gripperSubsystem.gripperStepper.setpoint) == 0

    async def end(self):
        pass