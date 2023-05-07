from .base.SubsystemBase import SubsystemBase

from .Controllers.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants

class BrushlessSubsystem(SubsystemBase):
    async def init(self):
        self.testBrushless = BrushlessMotorController(000000000,0,140,Constants.Robot.Odrive,Constants.Simulation)
        self.testBrushless.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)

    async def periodic(self):
        print("Subsystem Periodic",self.testBrushless.getPosition(),"/",self.testBrushless.position_setpoint)


    async def enable(self):
        self.testBrushless.enable()

    async def disable(self):
        self.testBrushless.disable()