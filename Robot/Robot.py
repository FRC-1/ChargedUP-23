from Subsystems.SubsystemBrushlessExample import BrushlessSubsystem
from Subsystems.SubsystemStepperExample import StepperSubsystem
from Commands.TestCommand import TestCommand

from Scheduler import Scheduler
sch = Scheduler()

from Visualizer.Visualizer import Visualizer
vis = Visualizer(loadField=False,Scheduler=sch)

# Subsystems
steppersubsystem = StepperSubsystem(sch)

steppersubsystem.waitForReady()
vis.turret_angle_func = steppersubsystem.testStepper.getAngle


# Commands
command = TestCommand(steppersubsystem, lambda : (1 == 1),-1,target_angle=45)

# Immediate Tasks
sch.addTask(steppersubsystem.enable())

# Continuous Tasks
sch.startContinuous() # startContinuous needs to be called after all subsystems and continuous commands were added