from Utils.Colors import COLOR
from .base.SubsystemBase import SubsystemBase
from Hardware.StepperMotorController import StepperMotorController
from Constants import Constants

class StepperSubsystem(SubsystemBase):
    async def init(self):
        self.testStepper = StepperMotorController(2,3,4,400,Constants.Simulation.Simulated)

    async def periodic(self):
        pass

    async def enable(self):
        self.testStepper.enable()

    async def disable(self):
        self.testStepper.disable()