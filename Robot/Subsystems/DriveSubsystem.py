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

        #self.statespace = DrivetrainSystem(2,4,3)
        self.prev_time = time.time()
        self.prevLeftDistance = 0
        self.prevRightDistance = 0

        self.currPose = (0,0,0)

        self.unlockDrivetrain()

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

    def setCurveture(self,speedPrecentage:float, rotationalSpeedPrecentage:float,drive_in_place:bool = False):
        
        if(speedPrecentage > 0):
            rotationalSpeedPrecentage *= -1
        if(drive_in_place):
            leftSpeed = speedPrecentage - rotationalSpeedPrecentage
            rightSpeed = speedPrecentage + rotationalSpeedPrecentage
        else:
            leftSpeed = speedPrecentage - abs(speedPrecentage) *rotationalSpeedPrecentage
            rightSpeed = speedPrecentage + abs(speedPrecentage) * rotationalSpeedPrecentage
        maxMagnitutde =  max(abs(leftSpeed),abs(rightSpeed))
        if (maxMagnitutde>1):
            leftSpeed /= maxMagnitutde
            rightSpeed /= maxMagnitutde
        self.setVelocity(leftSpeed * Constants.Robot.DriveSubsystem.max_velocity,rightSpeed * Constants.Robot.DriveSubsystem.max_velocity)
        
    async def periodic(self):
        current_time = time.time()
        dt = self.prev_time - current_time
        self.prev_time = current_time

        self.updateOdemetry(dt)
        # left_turnsPerSecond = 1
        # right_turnsPerSecond = -1
        
        # velocity = (-Constants.Robot.DriveSubsystem.wheel_circumference / 2.0)*(left_turnsPerSecond + right_turnsPerSecond)
        # rot_vel = (Constants.Robot.DriveSubsystem.wheel_circumference/Constants.Robot.DriveSubsystem.wheel_distance)*(right_turnsPerSecond-left_turnsPerSecond)
        
        # curr_state = self.statespace.Get_x()
        # dx = self.statespace.Get_ẋ(np.array([velocity,rot_vel]),dt)
        # self.statespace.Set_x(curr_state + dx) # UPDATE STATE
        # print("STATE",self.statespace.Get_x())

    def diffdrive(self,x, y, theta, v_l, v_r, t, l):
        # straight line
        if (v_l == v_r):
            theta_n = theta
            x_n = x + v_l * t * np.cos(theta)
            y_n = y + v_l * t * np.sin(theta)
        # circular motion
        else:
            # Calculate the radius
            R = l/2.0 * ((v_l + v_r) / (v_r - v_l))
            # computing center of curvature
            ICC_x = x - R * np.sin(theta)
            ICC_y = y + R * np.cos(theta)
            # compute the angular velocity
            omega = (v_r - v_l) / l
            # computing angle change
            dtheta = omega * t
            # forward kinematics for differential drive
            x_n = np.cos(dtheta)*(x-ICC_x) - np.sin(dtheta)*(y-ICC_y) + ICC_x
            y_n = np.sin(dtheta)*(x-ICC_x) + np.cos(dtheta)*(y-ICC_y) + ICC_y
            theta_n = theta + dtheta
        return x_n, y_n, theta_n

    def updateOdemetry(self, dt):
        new_pose = self.diffdrive(self.currPose[0],self.currPose[1],self.currPose[2],self.getLeftVeloctiy()/60*Constants.Robot.DriveSubsystem.wheel_circumference,self.getRightVeloctiy()/60*Constants.Robot.DriveSubsystem.wheel_circumference,dt,Constants.Robot.DriveSubsystem.wheel_distance)
        self.currPose = new_pose

    def getPosition(self):
        curr_state = self.currPose
        return (curr_state[0],curr_state[1])
    
    def getRotation(self):
        curr_state = self.currPose
        return curr_state[2]

    def getRotationDeg(self):
        return np.degrees(self.getRotation())

    def setVelocity(self,leftVelocity:float, rightVelocity:float):
        self.leftMotor.setVelocitySetpoint(leftVelocity)
        self.rightMotor.setVelocitySetpoint(rightVelocity)
    
    def getLeftVeloctiy(self)->float:
        return self.leftMotor.getVelocity()/4
        
    def getRightVeloctiy(self)->float:
        return self.rightMotor.getVelocity()/4
    
    async def enable(self):
        self.leftMotor.enable()
        self.rightMotor.enable()

    async def disable(self):
        self.leftMotor.disable()
        self.rightMotor.disable()