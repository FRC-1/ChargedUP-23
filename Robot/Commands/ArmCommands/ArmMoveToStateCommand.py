import asyncio
from typing import Awaitable
from Subsystems.ArmSubsytem import ArmSubsytem
from Commands.base.CommandBase import CommandBase

class ArmMoveToStateCommand(CommandBase):
    def __init__(self, armSubsystem:ArmSubsytem, conditionSupplier: Awaitable, priority: int,target_angle:float,target_length:float):
        super().__init__([armSubsystem], conditionSupplier, priority)
        
        self.armSubsystem = armSubsystem
        self.target_angle = target_angle
        self.target_length = target_length

        self.angle_threshold = 1 # deg
        self.length_threshold = 0.05 # M

    async def init(self):
        await self.armSubsystem.setAngle(self.target_angle)
        await self.armSubsystem.setLength(self.target_length)

        
    async def isFinished(self):
        condition = abs(self.armSubsystem.getAngle() - self.target_angle) < self.angle_threshold and abs(self.armSubsystem.getLength() - self.target_length) < self.length_threshold 
        return condition

    async def end(self):
        pass