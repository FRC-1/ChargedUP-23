from threading import Thread
import asyncio
from Constants import Constants
from typing import Awaitable

# first, we need a loop running in a parallel Thread
class AsyncLoopThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

class Scheduler():
    async def Continuous(self):
        while True:
            for task in self.continuous_tasks:
                asyncio.run_coroutine_threadsafe(task(),loop=self.loop)

            await asyncio.sleep(Constants.Simulation.dt)
        


    def __init__(self):
         # init a loop in another Thread
        loop_handler = AsyncLoopThread()
        loop_handler.start()
        self.loop = loop_handler.loop

        self.continuous_tasks = []

    def addTask(self,task:Awaitable):
        run_task = asyncio.run_coroutine_threadsafe(task,loop=self.loop)
        return run_task

    def startContinuous(self):
        self.addTask(self.runContinuous())

    def addContinuousTask(self,task:Awaitable):
        self.continuous_tasks.append(task)

    async def runContinuous(self):
        asyncio.run_coroutine_threadsafe(self.Continuous(),loop=self.loop)