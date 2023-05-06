
class SubsystemBase():
    currentCommandPriority = -1
    
    async def periodic(self):
        if(self.currentCommandPriority > -1):
            return
    
    async def __init__(self):
        while True:
            await self.periodic()
            