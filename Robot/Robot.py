from Controllers.StepperMotorController import StepperMotorController
import asyncio

test = StepperMotorController(2,3,4,400,True)

async def getAngle():
    while True:
        print(test.getAngle())
        await asyncio.sleep(0.02)

loop = asyncio.new_event_loop()
loop.create_task(test.moveToAngle(90,100))
loop.create_task(getAngle())
loop.run_forever()
