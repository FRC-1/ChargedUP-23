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
        if not self.subsystem.ready:
            return
        if(self.subsystem.currentCommand != self):
            if(self.subsystem.currentCommandPriority <= self.priority):
                if(self.subsystem.currentCommand != None):
                    asyncio.run_coroutine_threadsafe(self.subsystem.currentCommand.abort__(),self.subsystem.scheduler.loop)
                    self.subsystem.currentCommand = self
                    self.subsystem.currentCommandPriority = self.priority
        else:
            return

        if(self.conditionSupplier() and self.phase == CommandPhase.READY):
            self.phase = CommandPhase.INIT

        if(self.phase == CommandPhase.INIT):
            asyncio.run_coroutine_threadsafe(self.init__(),self.subsystem.scheduler.loop)
        if(self.phase == CommandPhase.RUNNING):
            asyncio.run_coroutine_threadsafe(self.isFinished__(),self.subsystem.scheduler.loop)
        if(self.phase == CommandPhase.FINISHED):
            asyncio.run_coroutine_threadsafe(self.end__(),self.subsystem.scheduler.loop)

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
        self.subsystem.currentCommand = None
        self.subsystem.currentCommandPriority = -1
        self.phase = CommandPhase.READY

    def __init__(self,subsystem:SubsystemBase,conditionSupplier:Awaitable,priority:int):
        self.phase = CommandPhase.READY
        self.subsystem = subsystem
        self.conditionSupplier = conditionSupplier
        self.priority = priority
        self.subsystem.scheduler.addContinuousTask(self.run__)
