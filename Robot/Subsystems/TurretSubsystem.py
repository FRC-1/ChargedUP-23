from Utils.Colors import COLOR
from .base.SubsystemBase import SubsystemBase
from Hardware.StepperMotorController import StepperMotorController
from Constants import Constants
Robot = Constants.Robot


class TurretSubsystem(SubsystemBase):
    async def init(self):
        self.turretStepper = StepperMotorController(17,27,22,Robot.TurretSubsystem.stepsPerRevolution * Robot.TurretSubsystem.gearing,Constants.Simulation.Simulated)
        self.beforeAngle = self.getAngle()
    async def setAngle(self,angle:float):
        if(0<=angle<=180):
            await self.turretStepper.moveToAngle(angle,Robot.TurretSubsystem.rpm)
        else:
            print(COLOR.FAIL, f"invalid angle must be between 0 to 180 got {angle} instead",COLOR.RESET)
            
    def getAngle(self)->float:
        return self.turretStepper.getAngle()
        
    async def periodic(self):
        pass

    async def enable(self):
        self.turretStepper.enable()


    async def disable(self):
        self.turretStepper.disable()