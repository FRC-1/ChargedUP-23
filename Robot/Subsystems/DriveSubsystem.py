from .base.SubsystemBase import SubsystemBase
from Hardware.BrushlessMotorController import BrushlessMotorController, ControlMode, InputMode
from Constants import Constants
from Utils.StateSpace import StateSpaceSystem
from Utils.Colors import COLOR
import math
from math import cos, sin
import numpy as np
import time
class DrivetrainSystem(StateSpaceSystem): # Override the default Time-Invariant method to use ΔT
        #INPUTS
        # VEL M/s
        # THETA VEL M/s

        #OUTPUTS
        # POS_X M
        # POS_Y M
        # ROT Rad

        #STATES
        # POS_X M
        # POS_Y M
        # POS_theta Rad

        # X CHANGE -> cos(self.Get_x()[2])*np.sign(self.Get_x()[3])
        # Y Change -> sin(self.Get_x()[2])*np.sign(self.Get_x()[3])
        def Get_A(self):
            temp_A = [[0,0,0,],  # POS X
                     [0,0,0,],  # POS Y
                     [0,0,0,],]  # POS THETA
            return temp_A
        
        def Get_B(self):
            temp_B = [[cos(self.Get_x()[2]),0], # POS X
                      [sin(self.Get_x()[2]),0], # POS Y
                      [0,1],] # POS THETA
            return temp_B

        def __init__(self, p, q, n, A=None, B=None, C=None, D=None):
            super().__init__(p, q, n, A, B, C, D)

            self.A = self.Get_A()

            self.B = self.Get_B()

            self.C = [[1,0,0,0,0],
                      [0,1,0,0,0],
                      [0,0,1,0,0],]

            self.D = [[0]]

        def Get_ẋ(self, u = None, dt = None):
            if(dt is None): # Assume dt of 1 if not specified
                dt = 1
            if(u is None):
                u = self.u
            if (u.shape == (self.p,)):
                self.A = self.Get_A()
                self.B = self.Get_B()
                
                return np.multiply(self.A,dt) @ self.x + np.multiply(self.B,dt) @ u
            else:
                print(COLOR.FAIL + ("u (input) must be a vector of len p ["+str(self.p)+"]","red") + COLOR.RESET)
                exit()

class DriveSubsystem(SubsystemBase):
    async def init(self):
        self.leftMotor = BrushlessMotorController(111111,0,140,Constants.Robot.Odrive,Constants.Simulation)
        self.rightMotor = BrushlessMotorController(111111,1,140,Constants.Robot.Odrive,Constants.Simulation)

        self.statespace = DrivetrainSystem(2,4,3)
        self.prev_time = time.time()

        self.unlockDrivetrain()
        print("Drive INIT")

    def lockDrivetrain(self):
        left_position = self.leftMotor.getPosition()
        right_position = self.rightMotor.getPosition()

        self.leftMotor.setPositionSetpoint(left_position)
        self.rightMotor.setPositionSetpoint(right_position)
        
        self.leftMotor.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)
        self.rightMotor.setControlMode(ControlMode.POSITION_CONTROL,InputMode.PASSTHROUGH)
        
    def unlockDrivetrain(self):
        self.leftMotor.setControlMode(ControlMode.VELOCITY_CONTROL,InputMode.PASSTHROUGH)
        self.rightMotor.setControlMode(ControlMode.VELOCITY_CONTROL,InputMode.PASSTHROUGH)

    async def periodic(self):
        current_time = time.time()
        dt = self.prev_time - current_time
        self.prev_time = current_time
        
        
        left_turnsPerSecond = 1
        right_turnsPerSecond = -1
        
        velocity = (-Constants.Robot.DriveSubsystem.wheel_circumference / 2.0)*(left_turnsPerSecond + right_turnsPerSecond)
        rot_vel = (Constants.Robot.DriveSubsystem.wheel_circumference/Constants.Robot.DriveSubsystem.wheel_distance)*(right_turnsPerSecond-left_turnsPerSecond)
        
        curr_state = self.statespace.Get_x()
        dx = self.statespace.Get_ẋ(np.array([velocity,rot_vel]),dt)
        self.statespace.Set_x(curr_state + dx) # UPDATE STATE
        print("STATE",self.statespace.Get_x())

    def getPosition(self):
        curr_state = self.statespace.Get_x()
        return (curr_state[0],curr_state[1])
    
    def getRotation(self):
        curr_state = self.statespace.Get_x()
        return curr_state[2]

    def getRotationDeg(self):
        return np.degrees(self.getRotation())

    def setVelocity(self,leftVelocity:float, rightVelocity:float):
        self.leftMotor.setVelocitySetpoint(leftVelocity)
        self.rightMotor.setVelocitySetpoint(rightVelocity)
    
    def getLeftVeloctiy(self)->float:
        return self.leftMotor.getVelocity()
        
    def getRightVeloctiy(self)->float:
        return self.rightMotor.getVelocity()
    
    async def enable(self):
        self.leftMotor.enable()
        self.rightMotor.enable()

    async def disable(self):
        self.leftMotor.disable()
        self.rightMotor.disable()