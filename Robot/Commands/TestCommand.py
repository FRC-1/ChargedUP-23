import asyncio
from typing import Awaitable
from .Subsystems.SubsystemStepperExample import StepperSubsystem
from .Subsystems.base.CommandBase import CommandBase, CommandPhase

class TestCommand(CommandBase):
    def __init__(self, stepperSubsystem:StepperSubsystem, conditionSupplier: Awaitable, priority: int,target_angle):
        super().__init__([stepperSubsystem], conditionSupplier, priority)
        
        self.stepperSubsystem = stepperSubsystem
        self.target_angle = target_angle

    async def init(self):
        await self.stepperSubsystem.testStepper.moveToAngle(self.target_angle,100)
        
    async def isFinished(self):
        if(self.time >= 2 and self.stepperSubsystem.testStepper.getAngle() == self.target_angle):
            await self.stepperSubsystem.testStepper.moveToAngle(self.target_angle*2,100)
        return abs(self.stepperSubsystem.testStepper.getAngle() - self.target_angle*2) <= (360.0 / self.stepperSubsystem.testStepper.stepsPerRevolution)

    async def end(self):
        pass