
from Commands.Subsystems.SubsystemBrushlessExample import BrushlessSubsystem
from Commands.Subsystems.SubsystemStepperExample import StepperSubsystem
from Commands.TestCommand import TestCommand

from Scheduler import Scheduler

sch = Scheduler()
# brushlesssubsystem = BrushlessSubsystem(sch)
# sch.addTask(brushlesssubsystem.enable())

steppersubsystem = StepperSubsystem(sch)
command = TestCommand(steppersubsystem, lambda : 1 == 1,1,target_angle=90)
command2 = TestCommand(steppersubsystem, lambda : 1 == 1,2,target_angle=45)


sch.addTask(steppersubsystem.enable())


# Continuous Tasks
sch.startContinuous() # startContinuous needs to be called after all subsystems and continuous commands were added