from Utils.Colors import COLOR
from typing import Awaitable
from Subsystems.DummySubsystem import DummySubsystem
from .base.CommandBase import CommandBase, CommandPhase

class PrintCommand(CommandBase):
    def __init__(self,scheduler,string, conditionSupplier: Awaitable, priority: int):
        super().__init__([DummySubsystem(scheduler=scheduler)], conditionSupplier, priority)
        self.string = string

    async def init(self):
        print(COLOR.OKCYAN,self.string,COLOR.RESET)
        
    async def isFinished(self):
        return True

    async def end(self):
        pass