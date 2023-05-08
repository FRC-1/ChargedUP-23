import asyncio
from typing import Awaitable
from enum import Enum
import time
from Constants import Constants

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
 
    def shouldStart(self):
        return self.phase == CommandPhase.INIT

    async def run__(self) -> bool: # returns if ran or not
        for subsystem in self.subsystems:
            if not subsystem.ready or subsystem.currentCommandPriority > self.priority or (subsystem.currentCommand != self and subsystem.currentCommandPriority == self.priority):
                return False

        if(self.conditionSupplier() and self.phase == CommandPhase.READY):
            for subsystem in self.subsystems:
                if(subsystem.currentCommand != None and subsystem.currentCommand != self):
                    asyncio.run_coroutine_threadsafe(subsystem.currentCommand.abort__(),subsystem.scheduler.loop)
                subsystem.currentCommand = self
                subsystem.currentCommandPriority = self.priority
            self.phase = CommandPhase.INIT

        if(self.phase == CommandPhase.INIT):
            asyncio.run_coroutine_threadsafe(self.init__(),self.scheduler.loop)
        if(self.phase == CommandPhase.RUNNING):
            asyncio.run_coroutine_threadsafe(self.isFinished__(),self.scheduler.loop)
        if(self.phase == CommandPhase.FINISHED):
            asyncio.run_coroutine_threadsafe(self.end__(False),self.scheduler.loop)

        return True

    async def abort__(self):
        self.phase = CommandPhase.FINISHED
        await self.end__(True)

    async def init__(self):
        self.start_time = time.time()
        await self.init()
        self.phase = CommandPhase.RUNNING

    async def isFinished__(self):
        self.time = time.time() - self.start_time
        if(self.phase == CommandPhase.RUNNING):
            ended = await self.isFinished()
            self.phase = CommandPhase.FINISHED if ended or self.phase == CommandPhase.FINISHED else CommandPhase.RUNNING
        else:
            self.phase = CommandPhase.FINISHED

    async def end__(self,aborted):
        await self.end()
        if(not aborted):
            for subsystem in self.subsystems:
                subsystem.currentCommand = None
                subsystem.currentCommandPriority = Constants.lowest_command_priority
        self.phase = CommandPhase.READY

    def __init__(self,subsystems:list,conditionSupplier:Awaitable,priority:int):
        self.phase = CommandPhase.READY
        self.subsystems = subsystems
        self.conditionSupplier = conditionSupplier
        self.priority = priority
        self.scheduler = self.subsystems[0].scheduler
        self.scheduler.addContinuousTask(self.run__)
        self.start_time = 0.0
        self.time = 0.0