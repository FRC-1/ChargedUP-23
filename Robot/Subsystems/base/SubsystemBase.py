import asyncio
from Constants import Constants

class SubsystemBase():
    async def periodic(self):
        pass

    async def init(self):
        pass

    async def enable(self):
        pass

    async def disable(self):
        pass

    async def init__(self):
        await self.init()
        self.ready = True

    async def periodicMaster__(self):
        await self.periodic()
    
    def waitForReady(self):
        while not self.ready:
            pass

    def __init__(self,scheduler):
        self.currentCommandPriority = Constants.lowest_command_priority
        self.currentCommand = None
        self.scheduler = scheduler
        self.ready = False
        scheduler.addContinuousTask(self.periodicMaster__)
        asyncio.run_coroutine_threadsafe(self.init__(),loop=scheduler.loop)