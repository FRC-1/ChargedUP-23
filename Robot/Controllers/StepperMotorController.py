import asyncio
import math
meth = math
from Constants import Constants

import importlib
GPIO = importlib.import_module(Constants.Simulation.GPIO).GPIO

class StepperMotorController:
    def __init__(self,enablePort:int,stepPort:int,directionPort:int,stepsPerRevolution:int,simulated:bool):
        self.enablePort = enablePort
        self.stepPort = stepPort
        self.directionPort = directionPort
        self.simulated = simulated
        self.currentSteps = 0
        self.stepsPerRevolution = stepsPerRevolution
        self.enabled = False
 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.stepPort, GPIO.OUT)
        GPIO.setup(self.directionPort, GPIO.OUT)
        GPIO.setup(self.enablePort, GPIO.OUT)
        
        
    def enable(self):
        self.enabled = True
        GPIO.output(self.enablePort, GPIO.HIGH)
    
    def disable(self):
        self.enabled = False
        GPIO.output(self.enablePort, GPIO.LOW)

    async def moveSteps(self,steps:int,rpm:float):
        if(self.enabled):
            GPIO.output(self.directionPort,GPIO.LOW if steps < 0 else GPIO.HIGH)
            sps = self.stepsPerRevolution * rpm/60
            sleep = 1/sps
            for i in range(steps):
                GPIO.output(self.stepPort, GPIO.HIGH)
                await asyncio.sleep(sleep/2)
                GPIO.output(self.stepPort, GPIO.LOW)
                await asyncio.sleep(sleep/2)
                self.currentSteps += (-1 if steps < 0 else 1) if self.enabled else 0

                self.currentSteps %= self.stepsPerRevolution
            
    async def moveToStep(self,target_step:int,rpm:float):
        await self.moveSteps(target_step - self.currentSteps,rpm)
    
    async def moveToAngle(self, angle:float, rpm:float):
        await self.moveToStep(math.floor((angle / 360.0) * self.stepsPerRevolution),rpm)
        
    def getAngle(self)->float:
        return self.currentSteps/self.stepsPerRevolution * 360%360