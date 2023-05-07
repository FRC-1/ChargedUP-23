import asyncio
class SubsystemBase():
    defaultCommand = None
    currentCommandPriority = -1
    
    async def periodic(self):
        pass

    async def init(self):
        pass

    async def enable(self):
        pass

    async def disable(self):
        pass

    async def periodicMaster__(self):
        await self.periodic()
        if(self.currentCommandPriority <= -1 and self.defaultCommand != None):
            await self.defaultCommand()
    
    def __init__(self,scheduler,defaultCommand = None):
        scheduler.addContinuousTask(self.periodicMaster__)
        asyncio.run_coroutine_threadsafe(self.init(),loop=scheduler.loop)
            