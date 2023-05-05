import RPiSim.GPIO

class Constants:
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
