import asyncio
from typing import Awaitable
from .SubsystemBase import SubsystemBase
from enum import Enum

class CommandPhase(Enum):
    INIT = 1,
    RUNNING = 2,
    FINISHED = 3,
    READY = 4,

class CommandBase():
    def init(self):
        pass

    async def isFinished(self):
        pass

    def end(self):
        pass
 

    async def run__(self) -> bool: # returns if ran or not
        for subsystem in self.subsystems:
            if not subsystem.ready or subsystem.currentCommand == self or subsystem.currentCommandPriority > self.priority:
                return False

        for subsystem in self.subsystems:
            if(subsystem.currentCommand != None):
                asyncio.run_coroutine_threadsafe(subsystem.currentCommand.abort__(),subsystem.scheduler.loop)
            subsystem.currentCommand = self
            subsystem.currentCommandPriority = self.priority

        if(self.conditionSupplier() and self.phase == CommandPhase.READY):
            self.phase = CommandPhase.INIT

        if(self.phase == CommandPhase.INIT):
            asyncio.run_coroutine_threadsafe(self.init__(),self.scheduler.loop)
        if(self.phase == CommandPhase.RUNNING):
            asyncio.run_coroutine_threadsafe(self.isFinished__(),self.scheduler.loop)
        if(self.phase == CommandPhase.FINISHED):
            asyncio.run_coroutine_threadsafe(self.end__(),self.scheduler.loop)

        return True

    async def abort__(self):
        self.phase = CommandPhase.FINISHED
        self.end__()

    async def init__(self):
        await self.init()
        self.phase = CommandPhase.RUNNING

    async def isFinished__(self):
        self.phase = CommandPhase.FINISHED if await self.isFinished() else CommandPhase.RUNNING

    async def end__(self):
        await self.end()
        for subsystem in self.subsystems:
            subsystem.currentCommand = None
            subsystem.currentCommandPriority = -1
        self.phase = CommandPhase.READY

    def __init__(self,subsystems:list[SubsystemBase],conditionSupplier:Awaitable,priority:int):
        self.phase = CommandPhase.READY
        self.subsystems = subsystems
        self.conditionSupplier = conditionSupplier
        self.priority = priority
        self.scheduler = self.subsystems[0].scheduler
        self.scheduler.addContinuousTask(self.run__)