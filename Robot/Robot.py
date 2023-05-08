from Utils.Colors import COLOR

from Subsystems.SubsystemStepperExample import StepperSubsystem
from Commands.TestCommand import TestCommand
from Commands.PrintCommand import PrintCommand

from Scheduler import Scheduler
sch = Scheduler()

from Visualizer.Visualizer import Visualizer
vis = Visualizer(Scheduler=sch,loadField=False)

from Driverstation.Controller import Controller
controller = Controller(sch)

# Subsystems
steppersubsystem = StepperSubsystem(sch)

# Simulation Parameters
vis.turret_angle_func = steppersubsystem.testStepper.getAngle

# Commands
command = TestCommand(steppersubsystem, controller.A_button.onPress,1,target_angle=45)
command = TestCommand(steppersubsystem, controller.A_button.onRelease,1,target_angle=0)

# Immediate Tasks
sch.addTask(steppersubsystem.enable())

# Continuous Tasks
sch.startContinuous() # startContinuous needs to be called after all subsystems and continuous commands were added

try:
    input(COLOR.WARNING + "\nENTER ANYTHING TO END EXECUTION ->\n\n" + COLOR.RESET)
except:
    pass