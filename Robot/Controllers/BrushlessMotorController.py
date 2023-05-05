import asyncio
import math
meth = math
from Constants import Constants
import odrive
from enum import Enum

class ControlType(Enum):
    POSITION_CONTROL=0
    VELOCITY_CONTROL=1
    TORQUE_CONTROL = 2

class BrushlessMotorController():
    def __init__(self,odriveIdx:int,axisIdx:int,kV:int,polePairs:int):
        self.kV = kV
        self.polePairs = polePairs

        self.control_type = ControlType.VELOCITY_CONTROL
        self.target_odrive = None
        self.target_axis = None

        self.velocity_setpoint = 0
        self.position_setpoint = 0
        self.enabled = False

        self.simulated_position = 0

    async def simulationUpdate(self):
        max_rpm = Constants.Simulation.Voltage * self.kV
        max_rps = max_rpm/60

        while True:
            if(self.enabled):    
                if(self.control_type == ControlType.POSITION_CONTROL):
                    self.simulated_position += (self.position_setpoint - self.simulated_position) * (max_rps * Constants.Simulation.dt) * Constants.Simulation.kP
                elif(self.control_type == ControlType.VELOCITY_CONTROL):
                    self.simulated_position += min(self.velocity_setpoint,Constants.Simulation.Voltage * self.kV) / 60.0 * Constants.Simulation.dt
                
            await asyncio.sleep(Constants.Simulation.dt)


    async def setControlType(self,control_type:ControlType):
        self.control_type = control_type
        if not Constants.Simulation.Simulated:
            pass # CHANGE ODRIVE CONTROL TYPE

    async def setVelocitySetpoint(self,setpoint:float):
        self.velocity_setpoint = min(setpoint,Constants.Simulation.Voltage * self.kV)
        if not Constants.Simulation.Simulated:
            pass # CHANGE ODRIVE VELOCITY SETPOINT
        

    async def setPositionSetpoint(self,setpoint:float):
        self.position_setpoint = setpoint
        if not Constants.Simulation.Simulated:
            pass # CHANGE ODRIVE POSITION SETPOINT

    async def enable(self):
        self.enabled = True
        if not Constants.Simulation.Simulated:
            pass # SET ODRIVE AXIS STATE TO CLOSED_LOOP_CONTROL

    async def disable(self):
        self.enabled = False
        if not Constants.Simulation.Simulated:
            pass # SET ODRIVE AXIS STATE TO IDLE
