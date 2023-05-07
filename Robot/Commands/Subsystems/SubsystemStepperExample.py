from .base.SubsystemBase import SubsystemBase

from .Controllers.StepperMotorController import StepperMotorController
from Constants import Constants

class StepperSubsystem(SubsystemBase):
    async def init(self):
        self.testStepper = StepperMotorController(2,3,4,400,Constants.Simulation.Simulated)

    async def periodic(self):
        print("Subsystem Periodic",self.testStepper.currentSteps,"/",self.testStepper.setpoint,self.testStepper.getAngle())
        pass

    async def enable(self):
        self.testStepper.enable()

    async def disable(self):
        self.testStepper.disable()