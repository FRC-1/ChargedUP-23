from Utils.Colors import COLOR

from Subsystems.SubsystemStepperExample import StepperSubsystem
from Commands.TestCommand import TestCommand
from Commands.PrintCommand import PrintCommand

from Subsystems.TurretSubsystem import TurretSubsystem
from Commands.TurretCommands.MoveTurretToAngleCommand import MoveTurretToAngleCommand
from Commands.TurretCommands.FlipTurretCommand import FlipTurretCommand

from Subsystems.GripperSubsystem import GripperSubsystem
from Commands.GripperCommand.MoveGripperToDistanceCommand import MoveGripperToDistance
from Commands.GripperCommand.GripperDefaultCommand import GripperDefaultCommand
from Commands.GripperCommand.GripperOpenCommand import GripperOpenCommand
from Commands.GripperCommand.GripperCloseCommand import GripperCloseCommand

from Commands.SwitchRobotMode import SwitchRobotMode

from Scheduler import Scheduler
sch = Scheduler()

from Visualizer.Visualizer import Visualizer
vis = Visualizer(Scheduler=sch,loadField=False)

from Driverstation.Controller import Controller
controller = Controller(sch)

def createTestSubsystem():
    # Subsystems
    steppersubsystem = StepperSubsystem(sch)

    # Simulation Parameters
    vis.turret_angle_func = steppersubsystem.testStepper.getAngle

    # Commands
    command = TestCommand(steppersubsystem, controller.A_button.onPress,1,target_angle=45)
    command = TestCommand(steppersubsystem, controller.A_button.onRelease,1,target_angle=0)

    # Immediate Tasks
    sch.addTask(steppersubsystem.enable())
    
def createTurretSubsystem():
    # Subsystems
    turretSubsystem = TurretSubsystem(sch)
    
    # Simulation Parameters
    vis.turret_angle_func = turretSubsystem.getAngle
    
    # Commands
    command = FlipTurretCommand(turretSubsystem, controller.B_button.onPress,3)
    
    # Immediate Tasks
    sch.addTask(turretSubsystem.enable())

def createGripperSubsystem():
    # Subsystems
    gripperSubsystem = GripperSubsystem(sch)
    
    # Commands
    GripperDefaultCommand(gripperSubsystem,lambda:True,0)
    GripperOpenCommand(gripperSubsystem,controller.right_bumper_button.onPress,1)
    GripperCloseCommand(gripperSubsystem,controller.left_bumper_button.onPress,1)
    SwitchRobotMode(gripperSubsystem,controller.Y_button.onPress,1)

    # Immediate Tasks
    sch.addTask(gripperSubsystem.enable())

createTurretSubsystem()
createGripperSubsystem()

# Continuous Tasks
sch.startContinuous() # startContinuous needs to be called after all subsystems and continuous commands were added

try:
    input(COLOR.WARNING + "\nENTER ANYTHING TO END EXECUTION ->\n\n" + COLOR.RESET)
except:
    pass