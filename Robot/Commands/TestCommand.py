import asyncio
from typing import Awaitable
from Subsystems.SubsystemStepperExample import StepperSubsystem
from .base.CommandBase import CommandBase, CommandPhase

class TestCommand(CommandBase):
    def __init__(self, stepperSubsystem:StepperSubsystem, conditionSupplier: Awaitable, priority: int,target_angle):
        super().__init__([stepperSubsystem], conditionSupplier, priority)
        
        self.stepperSubsystem = stepperSubsystem
        self.target_angle = target_angle

    async def init(self):
        await self.stepperSubsystem.testStepper.moveToAngle(self.target_angle,100)
        
    async def isFinished(self):
        return abs(self.stepperSubsystem.testStepper.currentSteps - self.stepperSubsystem.testStepper.setpoint) == 0

    async def end(self):
        pass