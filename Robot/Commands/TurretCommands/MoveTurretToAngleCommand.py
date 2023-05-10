import asyncio
from typing import Awaitable
from Subsystems.TurretSubsystem import TurretSubsystem
from Commands.base.CommandBase import CommandBase, CommandPhase

class MoveTurretToAngleCommand(CommandBase):
    def __init__(self, turretSubsystem:TurretSubsystem, conditionSupplier: Awaitable, priority: int,target_angle:float):
        super().__init__([turretSubsystem], conditionSupplier, priority)
        self.turretSubsystem = turretSubsystem
        self.target_angle = target_angle

    async def init(self):
        await self.turretSubsystem.setAngle(self.target_angle)
        
    async def isFinished(self):
        return abs(self.turretSubsystem.turretStepper.currentSteps - self.turretSubsystem.turretStepper.setpoint) == 0

    async def end(self):
        pass