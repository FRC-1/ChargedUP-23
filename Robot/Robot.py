import threading
import time
from Utils.Colors import COLOR

from Driverstation.Server import run_server, GetController, isReady, isEnable

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

async def enable_subsytems():
    for subsytem in subsytems:
        await subsytem.enable()
async def disable_subsytems():
    for subsytem in subsytems:
        await subsytem.disable()

was_enabled = False
async def checkEnabled():
    if(isEnable()):
        if not was_enabled:
            await enable_subsytems()
            was_enabled = True
    else:
        if was_enabled:
            await disable_subsytems()
            was_enabled = False
sch.addContinuousTask(checkEnabled)

# Run server
thread = threading.Thread(target=run_server, args=())
thread.daemon = True
thread.start()

print(COLOR.OKCYAN + "AWAITING CONNECTION" + COLOR.RESET)
while not isReady():
    time.sleep(1)
    print("...")

while GetController() is None:
    time.sleep(1)
    print(",,,")

subsytems = []

def createTurretSubsystem():
    # Subsystems
    turretSubsystem = TurretSubsystem(sch)
    subsytems.append(turretSubsystem)
    
    # Simulation Parameters
    vis.turret_angle_func = turretSubsystem.getAngle
    
    # Commands
    command = FlipTurretCommand(turretSubsystem, lambda : GetController().B_button.onPress(),3)

def createGripperSubsystem():
    # Subsystems
    gripperSubsystem = GripperSubsystem(sch)
    subsytems.append(gripperSubsystem)

    
    # Commands
    GripperDefaultCommand(gripperSubsystem,lambda:True,0)
    GripperOpenCommand(gripperSubsystem,lambda :GetController().right_bumper_button.onPress,1)
    GripperCloseCommand(gripperSubsystem,lambda :GetController().left_bumper_button.onPress,1)
    SwitchRobotMode(gripperSubsystem,lambda :GetController().Y_button.onPress,1)

def createArmSubsystem():
    # Subsystems
    armSubsystem = ArmSubsytem(sch)
    subsytems.append(armSubsystem)

    # Simulation Parameters
    vis.arm_angle_func = armSubsystem.getAngle
    vis.arm_distance_func = armSubsystem.getLength

    # Commands
    command1 = ArmMoveToStateCommand(armSubsystem, lambda : GetController().dpad_up_button.onPress() ,2,45,0.20)
    #ArmMoveToStateCommand(armSubsystem,command1.getFinished,1,20,0.45)

    command2 = ArmMoveToStateCommand(armSubsystem, lambda: (GetController().dpad_left_button.onPress() and armSubsystem.getAngle() > 40 and armSubsystem.getLength() <= 0.22) ,2,20,0.45)
    command2 = ArmMoveToStateCommand(armSubsystem, lambda: (GetController().dpad_down_button.onPress() and armSubsystem.getAngle() > 40 and armSubsystem.getLength() <= 0.22) ,2,0,0.0)


def createDriveSubsytem():
    # Subsystems
    driveSubsytem = DriveSubsystem(sch)
    subsytems.append(driveSubsytem)

    # Simulation Parameters
    vis.robot_position_func = driveSubsytem.getPosition
    vis.robot_rotation_func = driveSubsytem.getRotationDeg

    # Commands
    command = DriveByJoyCommand(driveSubsytem,lambda: (True),0,GetController().getRightStick)

createTurretSubsystem()
createGripperSubsystem()
createArmSubsystem()
createDriveSubsytem()

# Continuous Tasks
sch.startContinuous() # startContinuous needs to be called after all subsystems and continuous commands were added

print(COLOR.BOLD + ' '.join([COLOR.FAIL + "Tomer", COLOR.OKCYAN + "Yotam", COLOR.OKGREEN + "Ori","\n"]) + COLOR.RESET)
input(COLOR.WARNING + "\nENTER ANYTHING TO END EXECUTION ->\n\n" + COLOR.RESET)