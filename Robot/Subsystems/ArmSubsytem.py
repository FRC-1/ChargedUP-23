from .base.SubsystemBase import SubsystemBase
from Hardware.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants

import math

def cable_length_to_angle(length_m):
    sideA = 148.66/1000
    sideB = 21/100 # CABLE HOOK FROM ROTATION AXIS
    if(length_m > sideA + sideB or length_m < abs(sideA-sideB)):
        print("CABLE LENGTH ERROR, SHOULD BE",abs(sideA-sideB),"<",length_m,"<",sideA+sideB)
    #     return -999
    angle = math.acos((math.pow(sideA,2)+math.pow(sideB,2)-math.pow(length_m,2))/(2*sideA*sideB))
    return 180-(math.degrees(angle)+19.472)+10.148

def angle_to_cable_length(angle_deg):
    sideA = 148.66/1000
    sideB = 21/100 # CABLE HOOK FROM ROTATION AXIS
    angle_deg+=10.148
    angle_deg = 180 - angle_deg - 19.472
    angle_rad = math.radians(angle_deg)
    length_m = math.sqrt(math.pow(sideA, 2) + math.pow(sideB, 2) - 2 * sideA * sideB * math.cos(angle_rad))
    return length_m


class ArmSubsytem(SubsystemBase):
    async def init(self):
        self.angleMotor = BrushlessMotorController(000000,0,140,Constants.Robot.Odrive,Constants.Simulation)
        self.lengthMotor = BrushlessMotorController(000000,1,140,Constants.Robot.Odrive,Constants.Simulation)
        self.angleMotor.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)
        self.lengthMotor.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)
        
        self.angleMotor.simulated_position = (angle_to_cable_length(0) / Constants.Robot.ArmSubsystem.winch_circumfrence) * Constants.Robot.ArmSubsystem.gearing
        self.angleMotor.position_setpoint = self.angleMotor.simulated_position
        
    async def setAngle(self,angle:float):
        turns = (angle_to_cable_length(angle) / Constants.Robot.ArmSubsystem.winch_circumfrence) * Constants.Robot.ArmSubsystem.gearing
        self.angleMotor.setPositionSetpoint(turns)
    
    def getAngle(self):
        cable_length = (self.angleMotor.getPosition() / Constants.Robot.ArmSubsystem.gearing) * Constants.Robot.ArmSubsystem.winch_circumfrence
        return cable_length_to_angle(cable_length) - 19.472

    async def setLength(self, length:float):
        self.lengthMotor.setPositionSetpoint((length /  Constants.Robot.ArmSubsystem.winch_circumfrence) * Constants.Robot.ArmSubsystem.gearing)
    
    def getLength(self):
        return (self.lengthMotor.getPosition() / Constants.Robot.ArmSubsystem.gearing) * Constants.Robot.ArmSubsystem.winch_circumfrence
    
    async def periodic(self):
        if(Constants.Simulation.Simulated):
            await self.angleMotor.simulationUpdate()
            await self.lengthMotor.simulationUpdate()

    async def enable(self):
        self.angleMotor.enable()
        self.lengthMotor.enable()

    async def disable(self):
        self.angleMotor.disable()
        self.lengthMotor.disable()