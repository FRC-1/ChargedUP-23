from .Subsystems.base.CommandBase import CommandBase

class TestCommand(CommandBase):
    async def init(self):
        self.target_angle = 90
        await self.subsystem.testStepper.moveToAngle(self.target_angle,100)
        
    async def isFinished(self):
        return abs(self.subsystem.testStepper.getAngle() - self.target_angle) <= (360.0 / self.subsystem.testSteooer.stepsPerRevolution)

    async def end(self):
        pass