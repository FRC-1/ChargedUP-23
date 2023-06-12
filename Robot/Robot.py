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

from Subsystems.ArmSubsytem import ArmSubsytem
from Commands.ArmCommands.ArmMoveToStateCommand import ArmMoveToStateCommand

from Subsystems.DriveSubsystem import DriveSubsystem
from Commands.DriveCommands.DriveByJoyCommand import DriveByJoyCommand

from Commands.SwitchRobotMode import SwitchRobotMode

from Scheduler import Scheduler
sch = Scheduler()

from Visualizer.Visualizer import Visualizer
vis = Visualizer(Scheduler=sch,loadField=False)

from Driverstation.Controller import Controller
controller = Controller(sch)
    
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

def createArmSubsystem():
    # Subsystems
    armSubsystem = ArmSubsytem(sch)

    # Simulation Parameters
    vis.arm_angle_func = armSubsystem.getAngle
    vis.arm_distance_func = armSubsystem.getLength

    # Commands
    command1 = ArmMoveToStateCommand(armSubsystem, controller.dpad_up_button.onPress ,2,45,0.20)
    #ArmMoveToStateCommand(armSubsystem,command1.getFinished,1,20,0.45)

    command2 = ArmMoveToStateCommand(armSubsystem, lambda: (controller.dpad_left_button.onPress() and armSubsystem.getAngle() > 40 and armSubsystem.getLength() <= 0.22) ,2,20,0.45)
    command2 = ArmMoveToStateCommand(armSubsystem, lambda: (controller.dpad_down_button.onPress() and armSubsystem.getAngle() > 40 and armSubsystem.getLength() <= 0.22) ,2,0,0.0)
    #ArmMoveToStateCommand(armSubsystem,lambda : (controller.A_button.isPressed() and armSubsystem.getAngle() == 45) ,1,0,0.0)

    # Immediate Tasks
    sch.addTask(armSubsystem.enable())

def createDriveSubsytem():
    # Subsystems
    driveSubsytem = DriveSubsystem(sch)

    # Simulation Parameters
    vis.robot_position_func = driveSubsytem.getPosition
    vis.robot_rotation_func = driveSubsytem.getRotationDeg

    # Commands
    command = DriveByJoyCommand(driveSubsytem,lambda: (True),0,controller.getRightStick)

    # Immediate Tasks
    sch.addTask(driveSubsytem.enable())


createTurretSubsystem()
createGripperSubsystem()
createArmSubsystem()
createDriveSubsytem()

# Continuous Tasks
sch.startContinuous() # startContinuous needs to be called after all subsystems and continuous commands were added

print(COLOR.BOLD + ' '.join([COLOR.FAIL + "Tomer", COLOR.OKCYAN + "Yotam", COLOR.OKGREEN + "Ori","\n"]) + COLOR.RESET)
input(COLOR.WARNING + "\nENTER ANYTHING TO END EXECUTION ->\n\n" + COLOR.RESET)