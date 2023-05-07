from .base.SubsystemBase import SubsystemBase

from .Controllers.StepperMotorController import StepperMotorController
from Constants import Constants

class StepperSubsystem(SubsystemBase):
    async def init(self):
        self.testStepper = StepperMotorController(2,3,4,400,Constants.Simulation.Simulated)

    async def periodic(self):
        # if(self.testStepper.currentSteps <= 0):
        #     await self.testStepper.moveToAngle(90,100)
        # elif(self.testStepper.currentSteps >= 100):
        #     await self.testStepper.moveToAngle(0,100)
        print("Subsystem Periodic",self.testStepper.currentSteps,"/",self.testStepper.setpoint,self.testStepper.getAngle())

    async def enable(self):
        self.testStepper.enable()

    async def disable(self):
        self.testStepper.disable()