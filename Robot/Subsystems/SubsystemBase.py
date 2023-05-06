
class SubsystemBase():
    currentCommand = None
    currentCommandPriority = -1
    
    async def periodic(self):
        
    
    async def __init__(self):
        while True:
            await self.periodic()
            