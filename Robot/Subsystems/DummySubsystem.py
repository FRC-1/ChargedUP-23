from .base.SubsystemBase import SubsystemBase

from Constants import Constants

class DummySubsystem(SubsystemBase):
    async def init(self):
        pass

    async def periodic(self):
        pass

    async def enable(self):
        pass

    async def disable(self):
        pass