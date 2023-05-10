from Utils.Colors import COLOR
from .base.SubsystemBase import SubsystemBase
from Hardware.StepperMotorController import StepperMotorController
from Constants import Constants

class GripperSubsystem(SubsystemBase):
    async def init(self):
        self.gripperStepper = StepperMotorController(2,3,4,Constants.Robot.GripperSubsystem.stepsPerRevolution,Constants.Simulation.Simulated)

    async def setDistance(self,distance_mm):
        if(0<=distance_mm<=30):
            rotations = distance_mm * Constants.Robot.GripperSubsystem.hydraulic_ratio / Constants.Robot.GripperSubsystem.rotation_to_mm
            degrees = rotations * 360
            await self.gripperStepper.moveToAngle(degrees,Constants.Robot.GripperSubsystem.rpm)
        else:
            print(COLOR.FAIL, "invalid distance must be between 0 to 30 got {distance_mm} instead",COLOR.RESET)

    def getDistance(self):
        return (self.gripperStepper.getAngle() / 360) * Constants.Robot.GripperSubsystem.rotation_to_mm / Constants.Robot.GripperSubsystem.hydraulic_ratio

    async def periodic(self):
        pass

    async def enable(self):
        self.gripperStepper.enable()

    async def disable(self):
        self.gripperStepper.disable()