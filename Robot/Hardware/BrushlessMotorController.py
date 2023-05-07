import asyncio
import math
meth = math
import odrive
from enum import Enum
import Constants
import time
class ControlMode(Enum):
    TORQUE_CONTROL = 1,
    VELOCITY_CONTROL=2,
    POSITION_CONTROL=3,

class InputMode(Enum):
    PASSTHROUGH = 1 # VALID FOR ALL
    VEL_RAMP = 2 # ONLY FOR VELOCITY CONTROL
    TRAP_TRAJ = 5 # ONLY FOR POSITION CONTROL

class BrushlessMotorController():
    def __init__(self,odrive_serial_hex:int,axisIdx:int,kV:int,OdriveConstants:Constants.Constants.Robot.Odrive,SimulationConstants:Constants.Constants.Simulation):
        self.kV = kV
        self.polePairs = OdriveConstants.pole_pairs

        self.input_mode = InputMode.PASSTHROUGH
        self.control_mode = ControlMode.VELOCITY_CONTROL
        self.odrive = None # SERIAL HEX IS OBTAINED WHEN CONVERTING SERIAL FROM DECIMAL TO HEX OR WHEN CONNECTING ODRIVE TO ODRIVETOOL
        self.axis = None

        self.velocity_setpoint = 0
        self.position_setpoint = 0
        self.torque_setpoint = 0
        self.enabled = False
        self.velocity_feedthrough = 0

        self.simulated_position = 0
        self.simulation_constants = SimulationConstants
        self.odrive_constants = OdriveConstants

        if not self.simulation_constants.Simulated:
            self.odrive = odrive.find_any(serial_number=odrive_serial_hex)
            self.axis = self.odrive.axis0 if axisIdx == 0 else self.odrive.axis1

            self.axis.motor.config.current_lim = OdriveConstants.current_lim
            self.axis.controller.config.vel_limit = OdriveConstants.velocity_lim
            if(OdriveConstants.brake_enabled):
                self.odrive.config.enable_brake_resistor = True
                self.odrive.config.brake_resistance = OdriveConstants.brake_resistance
            self.axis.motor.config.pole_pairs = self.polePairs
            self.axis.motor.config.torque_constant = 8.27 / self.kV
            self.axis.motor.config.motor_type = 0 # HIGH CURRENT MOTOR

            self.axis.encoder.config.mode = 1 # HALL SENSORS
            self.axis.encoder.config.cpr = self.polePairs * 6   
            self.axis.encoder.config.calib_scan_distance = 150

            self.axis.encoder.config.bandwidth = 100
            self.axis.controller.config.pos_gain = OdriveConstants.position_kP
            self.axis.controller.config.vel_gain = OdriveConstants.velocity_kP * self.axis.motor.config.torque_constant * self.axis.encoder.config.cpr
            self.axis.controller.config.vel_integrator_gain = OdriveConstants.velocity_kI * self.axis.motor.config.torque_constant * self.axis.encoder.config.cpr

            self.axis.trap_traj.config.vel_limit = OdriveConstants.trap_traj_vel_limit
            self.axis.trap_traj.config.accel_limit = OdriveConstants.trap_traj_accel_limit
            self.axis.trap_traj.config.decel_limit = OdriveConstants.trap_traj_decel_limit

            self.axis.controller.config.vel_ramp_rate = OdriveConstants.vel_ramp_rate
            self.axis.controller.enable_torque_mode_vel_limit = True

            self.odrive.save_configuration()

        self.disable()
        self.setControlMode(ControlMode.POSITION_CONTROL,InputMode.TRAP_TRAJ)

    def CalibrateMotor(self):
        if not self.simulation_constants.Simulated:
            print("CALIBRATING MOTOR")
            self.axis.requested_state = 4 # MOTOR CALIBRATION
            if(self.axis.motor.error != 0):
                print("MOTOR ERROR!",self.axis.motor.error)
                exit()
            self.axis.motor.config.pre_calibrated = True
            self.axis.requested_state = 12 # HALL POLARITY CALIBRATION
            if(self.axis.encoder.error != 0):
                print("ENCODER ERROR!",self.axis.encoder.error)
                exit()
            self.axis.requested_state = 7 # ENCODER OFFSET CALIBRATION
            if(self.axis.encoder.error != 0):
                print("ENCODER ERROR!",self.axis.encoder.error)
                exit()
            self.axis.encoder.config.pre_calibrated = True

            self.odrive.save_configuration()
            self.odrive.reboot()


        else:
            print("CANT CALIBRATE MOTOR IN SIMULATION MODE!")

    def getErrors(self):
        return odrive.dump_errors(self.odrive)
    
    def clearErrors(self):
        self.odrive.clear_errors()

    async def simulationUpdate(self):
        if(self.simulation_constants.Simulated):
            max_rpm = self.simulation_constants.Voltage * self.kV
            max_rps = max_rpm/60
            
            if(self.enabled):    
                if(self.control_mode == ControlMode.POSITION_CONTROL):
                    self.simulated_position += max(min((self.position_setpoint - self.simulated_position) * (max_rps * self.simulation_constants.dt) * self.simulation_constants.kP + (self.velocity_feedthrough * self.simulation_constants.dt),self.odrive_constants.velocity_lim * self.simulation_constants.dt),-self.odrive_constants.velocity_lim * self.simulation_constants.dt)
                elif(self.control_mode == ControlMode.VELOCITY_CONTROL):
                    self.simulated_position += max(min(self.velocity_setpoint,self.simulation_constants.Voltage * self.kV) / 60.0 * self.simulation_constants.dt,-self.simulation_constants.Voltage * self.kV)

    def setControlMode(self,control_mode:ControlMode,input_mode:InputMode):
        self.input_mode = input_mode
        self.control_mode = control_mode
        if not self.simulation_constants.Simulated:
            self.axis.controller.config.control_mode = self.input_mode # CHANGE ODRIVE INPUT MODE
            self.axis.controller.config.control_mode = self.control_mode # CHANGE ODRIVE CONTROL MODE     

    def setTorqueSetpoint(self,torque:float=0.0):
        self.torque_setpoint = torque
        if not self.simulation_constants.Simulated:
            self.axis.controller.input_torque = torque # SET INPUT TORQUE

    def setVelocitySetpoint(self,rpm:float,torque:float=0.0):
        self.velocity_setpoint = min(rpm,self.simulation_constants.Voltage * self.kV)/60
        if not self.simulation_constants.Simulated:
            self.axis.controller.input_vel = self.velocity_setpoint # CHANGE ODRIVE VELOCITY SETPOINT
            self.axis.controller.input_torque = torque # SET FEEDFORWARD TORQUE

    def setPositionSetpoint(self,turns:float,rpm:float=0.0,torque:float=0.0):
        self.position_setpoint = turns
        self.velocity_feedthrough = rpm / 60.0
        if not self.simulation_constants.Simulated:
            self.axis.controller.input_pos = self.position_setpoint # CHANGE ODRIVE POSITION SETPOINT
            self.axis.controller.input_vel = self.velocity_feedthrough # SET FEEDFORWARD VELOCITY
            self.axis.controller.input_torque = torque # SET FEEDFORWARD TORQUE

    def getPosition(self):
        if not self.simulation_constants.Simulated:
            return self.axis.encoder.pos_estimate
        else:
            return self.simulated_position
        
    def getVelocity(self):
        if not self.simulation_constants.Simulated:
            return self.axis.encoder.vel_estimate * 60 # RPM
        else:
            return self.velocity_setpoint

    def enable(self):
        self.enabled = True
        if not self.simulation_constants.Simulated:
            self.axis.requested_state = 8 # SET ODRIVE AXIS STATE TO CLOSED_LOOP_CONTROL

    def disable(self):
        self.enabled = False
        if not self.simulation_constants.Simulated:
            self.axis.requested_state = 1 # SET ODRIVE AXIS STATE TO IDLE
