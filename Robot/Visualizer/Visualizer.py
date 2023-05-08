import math
import time
import numpy as np
import Visualizer.Robosim as Robosim
from Constants import Constants

robot_speed = 6 #m/s
robot_turn_speed = 180 #deg/s
robot_rope_speed = 5.71666667*0.1885 #m/s # Max Winch Speed
max_turret_speed = 3000 #deg/s

def point_at_angle_and_distance(point,distance,degrees):
    x = point[0] + distance * math.cos(math.radians(degrees))
    y = point[1] + distance * math.sin(math.radians(degrees))
    return (x,y)

class Visualizer():
    def __init__(self,Constants:Constants = Constants,loadField:bool = True,Scheduler = None) -> None:
        self.constants = Constants
        self.vis = Robosim.Init()
        self.robot_simulation = Robosim.Robot(self.vis)
        if(loadField):
            self.field = Robosim.Field(self.vis)
        self.scheduler = Scheduler
        if(self.scheduler != None):
            self.scheduler.addContinuousTask(self.setData)
            self.scheduler.addContinuousTask(self.Visualize)
            pass

        # robot data
        self.arm_angle_rope_length = 0.3579
        self.arm_distance_rope_length = 0.0

        # return funcs
        self.robot_position_func = None
        self.robot_rotation_func = None
        self.arm_angle_winch_velcotiy_func = None
        self.arm_distance_winch_velocity_func = None
        self.turret_angle_func = None

        # to be set by commands
        self.robot_position = (0,0)
        self.robot_rotation = 0.0

        self.arm_angle_winch_velcotiy = 0.0
        self.arm_distance_winch_velocity = 0.0
        self.turret_angle = 0.0

    async def setData(self):
        if(self.robot_position_func != None):
            self.robot_position = self.robot_position_func()
        if(self.robot_rotation_func != None):
            self.robot_rotation = self.robot_rotation_func()
        if(self.arm_angle_winch_velcotiy_func != None):
            self.arm_angle_winch_velcotiy = self.arm_angle_winch_velcotiy_func()
        if(self.arm_distance_winch_velocity_func != None):
            self.arm_distance_winch_velocity = self.arm_distance_winch_velocity_func()
        if(self.turret_angle_func != None):
            self.turret_angle = self.turret_angle_func()    
        

    def get_showpose(self,off_center_origin = 0.25):
        pose = point_at_angle_and_distance(self.robot_position,off_center_origin,self.robot_rotation)
        return np.array([pose[0],pose[1],0])

    def cable_length_to_angle(self,length_m):
        if(length_m < 0.06135 or length_m > 0.3579):
            print("ANGLE CABLE LENGTH",length_m,"POTENTIALLY DANGEROUS. PLEASE KEEP CABLE LENGTH BETWEEN 0.06135 <-> 0.3579")
        length_m = min(max(length_m,0.06135),0.3579)
        sideA = 148.66/1000
        sideB = 21/100 # CABLE HOOK FROM ROTATION AXIS
        if(length_m > sideA + sideB or length_m < abs(sideA-sideB)):
            print("CABLE LENGTH ERROR, SHOULD BE",abs(sideA-sideB),"<",length_m,"<",sideA+sideB)
            return -999
        angle = math.acos((math.pow(sideA,2)+math.pow(sideB,2)-math.pow(length_m,2))/(2*sideA*sideB))
        return 180-(math.degrees(angle)+19.472)+10


    async def Visualize(self):
        self.robot_simulation.set_location(self.get_showpose())
        self.robot_simulation.set_rotation(self.robot_rotation)
        
        self.arm_angle_rope_length = self.arm_angle_rope_length + self.constants.Simulation.dt * self.arm_angle_winch_velcotiy
        self.robot_simulation.set_arm_angle(self.cable_length_to_angle(self.arm_angle_rope_length))
        
        self.arm_distance_rope_length = self.arm_distance_rope_length + self.constants.Simulation.dt * self.arm_distance_winch_velocity * 0.5
        if(self.arm_distance_rope_length < 0.0 or self.arm_distance_rope_length > 0.45):
            print("DISTANCE CABLE LENGTH",self.arm_distance_rope_length,"POTENTIALLY DANGEROUS. PLEASE KEEP CABLE LENGTH BETWEEN 0.0 <-> 0.45")
        self.robot_simulation.set_arm_distance(self.arm_distance_rope_length)

        self.robot_simulation.set_turret_angle(self.turret_angle)