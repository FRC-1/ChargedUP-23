import asyncio
from typing import Awaitable
from .Subsystems.base.SubsystemBase import SubsystemBase
from .Subsystems.base.CommandBase import CommandBase, CommandPhase

class TestCommand(CommandBase):
    def __init__(self, stepperSubsystem:SubsystemBase, conditionSupplier: Awaitable, priority: int,target_angle):
        super().__init__([stepperSubsystem], conditionSupplier, priority)
        
        self.stepperSubsystem = stepperSubsystem
        self.target_angle = target_angle

    async def init(self):
        await self.stepperSubsystem.testStepper.moveToAngle(self.target_angle,100)
        
    async def isFinished(self):
        # print("TEST RUNNING")
        # print(self.time)
        # if(self.time >= 2):
        #     await self.stepperSubsystem.testStepper.moveSteps(100,100)
        # return abs(self.mainSubsystem.testStepper.getAngle() - self.target_angle) <= (360.0 / self.stepperSubsystem.testStepper.stepsPerRevolution)
        return False

    async def end(self):
        pass