from Controllers.StepperMotorController import StepperMotorController
from Controllers.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants
import asyncio
import matplotlib.pyplot as plt

testStepper = StepperMotorController(2,3,4,400,Constants.Simulation.Simulated)
testBrushless = BrushlessMotorController(000000000,0,140,Constants.Robot.Odrive,Constants.Simulation)

testBrushless.enable()
testBrushless.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)

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
loop.create_task(testBrushless.simulationUpdate())
loop.create_task(plotPosition(loop))

testBrushless.setPositionSetpoint(360)

loop.run_forever()