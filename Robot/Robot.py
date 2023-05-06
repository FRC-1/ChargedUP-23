from Controllers.StepperMotorController import StepperMotorController
from Controllers.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants
import asyncio
import matplotlib.pyplot as plt
from Scheduler import Scheduler

testStepper = StepperMotorController(2,3,4,400,Constants.Simulation.Simulated)
testBrushless = BrushlessMotorController(000000000,0,140,Constants.Robot.Odrive,Constants.Simulation)

testBrushless.enable()
testBrushless.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)

sch = Scheduler()

data = {
    'y' : [],
    'x' : [],
    'time' : 0.0,
    'extra' : 0.0,
    'done' : False
}

runTask = None

async def plotPosition():
    if not data['done']:
        data['y'].append(testBrushless.simulated_position)
        data['x'].append(data['time'])

        if((testBrushless.position_setpoint - testBrushless.simulated_position) < 0.1):
            data['extra'] = data['extra'] + Constants.Simulation.dt
            if(data['extra'] >= 1):
                plt.title("Line graph")
                plt.plot(data['x'], data['y'], color="red")
                plt.show()
                data['done'] = True
        data['time'] = data['time'] + Constants.Simulation.dt

        print(data['time'])

# Continuous Tasks
sch.addContinuousTask(testBrushless.simulationUpdate)
sch.addContinuousTask(plotPosition)
sch.startContinuous()

testBrushless.setPositionSetpoint(100)