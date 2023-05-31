from .base.SubsystemBase import SubsystemBase
from Hardware.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants

import math

def cable_length_to_angle(length_m):
    sideA = 148.66/1000
    sideB = 21/100 # CABLE HOOK FROM ROTATION AXIS
    if(length_m > sideA + sideB or length_m < abs(sideA-sideB)):
        print("CABLE LENGTH ERROR, SHOULD BE",abs(sideA-sideB),"<",length_m,"<",sideA+sideB)
        return -999
    angle = math.acos((math.pow(sideA,2)+math.pow(sideB,2)-math.pow(length_m,2))/(2*sideA*sideB))
    return 180-(math.degrees(angle)+19.472)+10

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
        
    async def setAngle(self,angle:float):
        turns = (angle_to_cable_length(angle) / Constants.Robot.ArmSubsystem.winch_circumfrence) * Constants.Robot.ArmSubsystem.gearing
        await self.angleMotor.setPositionSetpoint(turns)
    
    def getAngle(self):
        return (self.angleMotor.getPosition() / Constants.Robot.ArmSubsystem.gearing) * Constants.Robot.ArmSubsystem.winch_circumfrence

    async def setDistance(self, distance:float):
        await self.lengthMotor.setPositionSetpoint((distance /  Constants.Robot.ArmSubsystem.winch_circumfrence) * Constants.Robot.ArmSubsystem.gearing)
    
    def getDistance(self):
        return (self.distance_motor.getPosition() / Constants.Robot.ArmSubsystem.gearing) * Constants.Robot.ArmSubsystem.winch_circumfrence
    
    async def periodic(self):
        if(Constants.Simulation.Simulated):
            await self.angleMotor.simulationUpdate()
            await self.distanceMotor.simulationUpdate()

    async def enable(self):
        pass

    async def disable(self):
        pass