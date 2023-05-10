from typing import Awaitable
from Subsystems.TurretSubsystem import TurretSubsystem
from Commands.base.CommandBase import CommandBase, CommandPhase
from Globals import *

class FlipTurretCommand(CommandBase):
    def __init__(self, turretSubsystem:TurretSubsystem, conditionSupplier: Awaitable, priority: int):
        super().__init__([turretSubsystem], conditionSupplier, priority)
        self.turretSubsystem = turretSubsystem

    async def init(self):
        await self.turretSubsystem.setAngle(int(Direction.BACK if Globals.Robot.turret_side == Direction.FRONT else Direction.FRONT))

    async def isFinished(self):
        return abs(self.turretSubsystem.turretStepper.currentSteps - self.turretSubsystem.turretStepper.setpoint) == 0

    async def end(self):
        pass