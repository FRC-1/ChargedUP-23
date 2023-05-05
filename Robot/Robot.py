from Controllers.StepperMotorController import StepperMotorController
from Controllers.BrushlessMotorController import BrushlessMotorController, ControlType
from Constants import Constants
import asyncio
import matplotlib.pyplot as plt

testStepper = StepperMotorController(2,3,4,400,True)
testBrushless = BrushlessMotorController(0,0,140,7)

async def plotPosition(loop):
    y = []
    x = []

    time = 0.0
    extra = 0.0

    while True:
        y.append(testBrushless.simulated_position)
        x.append(time)

        if((testBrushless.position_setpoint - testBrushless.simulated_position) < 0.1):
            extra += Constants.Simulation.dt
            if(extra >= 1):
                plt.title("Line graph")
                plt.plot(x, y, color="red")
                plt.show()

                loop.stop()
                break

        time += Constants.Simulation.dt
        await asyncio.sleep(Constants.Simulation.dt)


loop = asyncio.new_event_loop()

# Continuous Tasks
loop.create_task(testBrushless.enable())
loop.create_task(testBrushless.simulationUpdate())
loop.create_task(plotPosition(loop))

# Immediate Tasks
loop.create_task(testBrushless.setControlType(ControlType.POSITION_CONTROL))
loop.create_task(testBrushless.setPositionSetpoint(360))
loop.create_task(testBrushless.setVelocitySetpoint(5000))

loop.run_forever()