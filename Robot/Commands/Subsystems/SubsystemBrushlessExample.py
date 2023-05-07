from .SubsystemBase.SubsystemBase import SubsystemBase

from .Controllers.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants

class BrushlessSubsystem(SubsystemBase):
    async def init(self):
        self.testBrushless = BrushlessMotorController(000000000,0,140,Constants.Robot.Odrive,Constants.Simulation)
        self.testBrushless.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)

    async def periodic(self):
        if(self.testBrushless.simulated_position < 1):
            self.testBrushless.setPositionSetpoint(100)
        elif(self.testBrushless.simulated_position > 99):
            self.testBrushless.setPositionSetpoint(0)
        await self.testBrushless.simulationUpdate()
        print("Subsystem Periodic",self.testBrushless.simulated_position,"/",self.testBrushless.position_setpoint)


    async def enable(self):
        self.testBrushless.enable()

    async def disable(self):
        self.testBrushless.disable()