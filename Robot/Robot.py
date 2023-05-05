from Controllers.StepperMotorController import StepperMotorController
from Controllers.BrushlessMotorController import BrushlessMotorController
import asyncio

testStepper = StepperMotorController(2,3,4,400,True)
testBrushless = BrushlessMotorController(0,0,140,7)

loop = asyncio.new_event_loop()
loop.create_task(testStepper.moveToAngle(90,100))
loop.run_forever()
