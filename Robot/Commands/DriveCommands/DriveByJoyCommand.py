import asyncio
from typing import Awaitable
from Subsystems.DriveSubsystem import DriveSubsystem
from Commands.base.CommandBase import CommandBase
from Constants import Constants

class DriveByJoyCommand(CommandBase):
    def __init__(self, driveSubsystem:DriveSubsystem, conditionSupplier: Awaitable, priority: int,stick_supplier):
        super().__init__([driveSubsystem], conditionSupplier, priority)
        
        self.driveSubsystem = driveSubsystem
        self.stick_supplier = stick_supplier

        self.angle_threshold = 1 # deg
        self.length_threshold = 0.05 # M

    async def init(self):
        pass
        
    def deadZone(self,val,zone):
        if(abs(val)<zone):
            return 0
        else: return val

    async def isFinished(self):
        x,y = self.stick_supplier()
        x = self.deadZone(x,Constants.Controller.stick_deadzone)
        y = self.deadZone(y,Constants.Controller.stick_deadzone)
        self.driveSubsystem.setCurveture(-y,x)
        return False

    async def end(self):
        pass