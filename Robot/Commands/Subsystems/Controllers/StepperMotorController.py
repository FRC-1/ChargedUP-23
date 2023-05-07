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

        self.setpoint = 0
 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.stepPort, GPIO.OUT)
        GPIO.setup(self.directionPort, GPIO.OUT)
        GPIO.setup(self.enablePort, GPIO.OUT)

        self.disable()

        self.newmove = False
        
        
    def enable(self):
        self.enabled = True
        GPIO.output(self.enablePort, GPIO.HIGH)
    
    def disable(self):
        self.enabled = False
        GPIO.output(self.enablePort, GPIO.LOW)
            
    async def moveToStep(self,target_step:int,rpm:float):
        if(target_step != self.setpoint):
            self.setpoint = target_step
            while abs(self.currentSteps - self.setpoint) > 0:
                GPIO.output(self.directionPort,GPIO.LOW if self.setpoint < self.currentSteps else GPIO.HIGH)
                sps = self.stepsPerRevolution * rpm/60
                sleep = 1/sps

                if(self.newmove):
                    break

                GPIO.output(self.stepPort, GPIO.HIGH)
                await asyncio.sleep(sleep/2)
                GPIO.output(self.stepPort, GPIO.LOW)
                await asyncio.sleep(sleep/2)
                self.currentSteps += (-1 if (self.setpoint < self.currentSteps) else 1) if self.enabled else 0
                self.currentSteps %= self.stepsPerRevolution
    
    async def moveToAngle(self, angle:float, rpm:float):
        await self.moveToStep(math.floor((angle / 360.0) * self.stepsPerRevolution),rpm)
        
    def getAngle(self)->float:
        return self.currentSteps/self.stepsPerRevolution * 360%360