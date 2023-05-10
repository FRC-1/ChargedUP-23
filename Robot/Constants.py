import RPiSim.GPIO

class Constants:
    lowest_command_priority = -999999

    class Simulation:
        Simulated = True
        GPIO = 'RPiSim.GPIO' if Simulated else 'RPI.GPIO'
        Voltage = 31.75
        dt = 0.02
        kP = 0.1

    class Robot:
        class Odrive:
            current_lim = 60 # A
            velocity_lim = 60 # turn/s
            brake_resistance = 0 # ohms

            vel_ramp_rate = 0.5 # turn/s

            trap_traj_vel_limit = 10 # turn/s
            trap_traj_accel_limit = 1 # turn/s
            trap_traj_decel_limit = 1 # turn/s

            brake_enabled = False
            pole_pairs = 7

            position_kP = 1
            velocity_kP = 0.02
            velocity_kI = 0.1
        class TurretSubsystem:
            stepsPerRevolution = 400
            gearing = 2
            rpm = 60 # time to complete half revolution-> 0.5/(RPM/60)
        
        class GripperSubsystem:
            stepsPerRevolution = 400
            rotation_to_mm = 8 # 1 rot = 8 mm
            hydraulic_ratio = (804.25/314.16) # 2.56000127:1
            rpm = 1000

            cone_closed = 30
            cone_open = 25

            cube_closed = 10
            cube_open = 0