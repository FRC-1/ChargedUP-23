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

    async def moveToPoint(self):
        max_rpm = setpoint,Constants.Simulation.Voltage * self.KV
        max_rps = max_rpm/60

        while self.simulated_position != self.position_setpoint:
            self.simulated_position += (self.position_setpoint - self.simulated_position) * (max_rps * 0.02)
            await asyncio.sleep(Constants.Simulation.dt)

    async def setControlType(self,control_type:ControlType):
        self.control_type = control_type
        if not Constants.Simulation.Simulated:
            pass # CHANGE ODRIVE CONTROL TYPE
        else:
            if(self.control_type == ControlType.POSITION_CONTROL):
                await self.moveToPoint()

    async def setVelocitySetpoint(self,setpoint:float):
        self.velocity_setpoint = math.min(setpoint,Constants.Simulation.Voltage * self.KV)
        if not Constants.Simulation.Simulated:
            pass # CHANGE ODRIVE VELOCITY SETPOINT
        

    async def setPositionSetpoint(self,setpoint:float):
        self.velocity_setpoint = setpoint
        if not Constants.Simulation.Simulated:
            pass # CHANGE ODRIVE POSITION SETPOINT
        if(self.control_type == ControlType.POSITION_CONTROL):
                await self.moveToPoint()

    def enable(self):
        self.enabled = True
        if not Constants.Simulation.Simulated:
            pass # SET ODRIVE AXIS STATE TO CLOSED_LOOP_CONTROL

    def disable(self):
        self.enabled = False
        if not Constants.Simulation.Simulated:
            pass # SET ODRIVE AXIS STATE TO IDLE
