import asyncio
import math
meth = math
from Constants import Constants
import odrive
from enum import Enum

class ControlMode(Enum):
    TORQUE_CONTROL = 1,
    VELOCITY_CONTROL=2,
    POSITION_CONTROL=3,

class InputMode(Enum):
    PASSTHROUGH = 1 # VALID FOR ALL
    VEL_RAMP = 2 # ONLY FOR VELOCITY CONTROL
    TRAP_TRAJ = 5 # ONLY FOR POSITION CONTROL

class BrushlessMotorController():
    def __init__(self,odrive_serial_hex:int,axisIdx:int,kV:int,polePairs:int):
        self.kV = kV
        self.polePairs = polePairs

        self.input_mode = InputMode.PASSTHROUGH
        self.control_mode = ControlMode.VELOCITY_CONTROL
        self.odrive = None # SERIAL HEX IS OBTAINED WHEN CONVERTING SERIAL FROM DECIMAL TO HEX OR WHEN CONNECTING ODRIVE TO ODRIVETOOL
        self.axis = None

        self.velocity_setpoint = 0
        self.position_setpoint = 0
        self.torque_setpoint = 0
        self.enabled = False

        self.simulated_position = 0

        if not Constants.Simulation.Simulated:
            self.odrive = odrive.find_any(serial_number=odrive_serial_hex)
            self.axis = self.odrive.axis0 if axisIdx == 0 else self.odrive.axis1

            self.axis.motor.config.current_lim = Constants.Robot.Odrive.current_lim
            self.axis.controller.config.vel_limit = Constants.Robot.Odrive.velocity_lim
            if(Constants.Robot.Odrive.brake_enabled):
                self.odrive.config.enable_brake_resistor = True
                self.odrive.config.brake_resistance = Constants.Robot.Odrive.brake_resistance
            self.axis.motor.config.pole_pairs = self.polePairs
            self.axis.motor.config.torque_constant = 8.27 / self.kV
            self.axis.motor.config.motor_type = 0 # HIGH CURRENT MOTOR

            self.axis.encoder.config.mode = 1 # HALL SENSORS
            self.axis.encoder.config.cpr = self.polePairs * 6   
            self.axis.encoder.config.calib_scan_distance = 150

            self.axis.encoder.config.bandwidth = 100
            self.axis.controller.config.pos_gain = Constants.Robot.Odrive.position_kP
            self.axis.controller.config.vel_gain = Constants.Robot.Odrive.velocity_kP * self.axis.motor.config.torque_constant * self.axis.encoder.config.cpr
            self.axis.controller.config.vel_integrator_gain = Constants.Robot.Odrive.velocity_kI * self.axis.motor.config.torque_constant * self.axis.encoder.config.cpr

            self.axis.trap_traj.config.vel_limit = Constants.Robot.Odrive.trap_traj_vel_limit
            self.axis.trap_traj.config.accel_limit = Constants.Robot.Odrive.trap_traj_accel_limit
            self.axis.trap_traj.config.decel_limit = Constants.Robot.Odrive.trap_traj_decel_limit

            self.axis.controller.config.vel_ramp_rate = Constants.Robot.Odrive.vel_ramp_rate
            self.axis.controller.enable_torque_mode_vel_limit = True

            self.odrive.save_configuration()

        self.disable()
        self.setControlMode(ControlMode.POSITION_CONTROL,InputMode.TRAP_TRAJ)

    def CalibrateMotor(self):
        if not Constants.Simulation.Simulated:
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

    async def getErrors(self):
        return odrive.dump_errors(self.odrive)
    
    async def clearErrors(self):
        self.odrive.clear_errors()

    async def simulationUpdate(self):
        max_rpm = Constants.Simulation.Voltage * self.kV
        max_rps = max_rpm/60

        while True:
            if(self.enabled):    
                if(self.control_mode == ControlMode.POSITION_CONTROL):
                    self.simulated_position += (self.position_setpoint - self.simulated_position) * (max_rps * Constants.Simulation.dt) * Constants.Simulation.kP
                elif(self.control_mode == ControlMode.VELOCITY_CONTROL):
                    self.simulated_position += min(self.velocity_setpoint,Constants.Simulation.Voltage * self.kV) / 60.0 * Constants.Simulation.dt
                
            await asyncio.sleep(Constants.Simulation.dt)

    async def setControlMode(self,control_mode:ControlMode,input_mode:InputMode):
        self.input_mode = input_mode
        self.control_mode = control_mode
        if not Constants.Simulation.Simulated:
            self.axis.controller.config.control_mode = self.input_mode # CHANGE ODRIVE INPUT MODE
            self.axis.controller.config.control_mode = self.control_mode # CHANGE ODRIVE CONTROL MODE     

    async def setTorqueSetpoint(self,torque:float=0.0):
        self.torque_setpoint = torque
        if not Constants.Simulation.Simulated:
            self.axis.controller.input_torque = torque # SET INPUT TORQUE

    async def setVelocitySetpoint(self,rpm:float,torque:float=0.0):
        self.velocity_setpoint = min(rpm,Constants.Simulation.Voltage * self.kV)/60
        if not Constants.Simulation.Simulated:
            self.axis.controller.input_vel = self.velocity_setpoint # CHANGE ODRIVE VELOCITY SETPOINT
            self.axis.controller.input_torque = torque # SET FEEDFORWARD TORQUE

    async def setPositionSetpoint(self,turns:float,rpm:float=0.0,torque:float=0.0):
        self.position_setpoint = turns
        if not Constants.Simulation.Simulated:
            self.axis.controller.input_pos = self.position_setpoint # CHANGE ODRIVE POSITION SETPOINT
            self.axis.controller.input_vel = self.velocity_setpoint # SET FEEDFORWARD VELOCITY
            self.axis.controller.input_torque = torque # SET FEEDFORWARD TORQUE

    async def enable(self):
        self.enabled = True
        if not Constants.Simulation.Simulated:
            self.axis.requested_state = 8 # SET ODRIVE AXIS STATE TO CLOSED_LOOP_CONTROL

    async def disable(self):
        self.enabled = False
        if not Constants.Simulation.Simulated:
            self.axis.requested_state = 1 # SET ODRIVE AXIS STATE TO IDLE
