from .base.SubsystemBase import SubsystemBase
from Hardware.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants

class DriveSubsystem(SubsystemBase):
    async def init(self):
        self.leftMotor = BrushlessMotorController(111111,0,140,Constants.Robot.Odrive,Constants.Simulation)
        self.rightMotor = BrushlessMotorController(111111,1,140,Constants.Robot.Odrive,Constants.Simulation)

        self.unlockDrivetrain()

    def lockDrivetrain(self):
        left_position = self.leftMotor.getPosition()
        right_position = self.rightMotor.getPosition()

        self.leftMotor.setPositionSetpoint(left_position)
        self.leftMotor.setPositionSetpoint(right_position)
        
        self.leftMotor.setControlMode(ControlMode.POSITION_CONTROL)
        self.rightMotor.setControlMode(ControlMode.POSITION_CONTROL)
        
    def unlockDrivetrain(self):
        self.leftMotor.setControlMode(ControlMode.VELOCITY_CONTROL)
        self.rightMotor.setControlMode(ControlMode.VELOCITY_CONTROL)

    async def periodic(self):
        pass

    def setVelocity(self,leftVelocity:float, rightVelocity:float):
        self.leftMotor.setVelocitySetpoint(leftVelocity)
        self.rightMotor.setVelocitySetpoint(rightVelocity)
    
    def getLeftVeloctiy(self)->float:
        return self.leftMotor.getVelocity()
        
    def getRightVeloctiy(self)->float:
        return self.rightMotor.getVelocity()
    
    async def enable(self):
        self.leftMotor.enable()
        self.rightMotor.enable()

    async def disable(self):
        self.leftMotor.disable()
        self.rightMotor.disable()