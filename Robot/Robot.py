
from Commands.Subsystems.SubsystemBrushlessExample import BrushlessSubsystem
from Commands.Subsystems.SubsystemStepperExample import StepperSubsystem

import matplotlib.pyplot as plt
from Scheduler import Scheduler

sch = Scheduler()
brushlesssubsystem = BrushlessSubsystem(sch)
# steppersubsystem = StepperSubsystem(sch)

sch.addTask(brushlesssubsystem.enable())
# sch.addTask(steppersubsystem.enable())

data = {
    'y' : [],
    'x' : [],
    'time' : 0.0,
    'extra' : 0.0,
    'done' : False
}

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
# sch.addContinuousTask(testBrushless.simulationUpdate)
# sch.addContinuousTask(plotPosition)
sch.startContinuous()

# testBrushless.setPositionSetpoint(100)