import asyncio
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
        if(self.currentCommandPriority <= -1 and self.defaultCommand != None):
            self.currentCommand = self.defaultCommand
            await self.defaultCommand()
    
    def __init__(self,scheduler,defaultCommand = None):
        self.defaultCommand = None
        self.currentCommandPriority = -1
        self.currentCommand = None
        self.scheduler = scheduler
        self.ready = False
        scheduler.addContinuousTask(self.periodicMaster__)
        asyncio.run_coroutine_threadsafe(self.init__(),loop=scheduler.loop)