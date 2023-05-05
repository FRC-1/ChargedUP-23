import RPiSim.GPIO

class Constants:
    class Simulation:
        Simulated = True
        GPIO = 'RPiSim.GPIO' if Simulated else 'RPI.GPIO'
        Voltage = 40
        dt = 0.02
        kP = 0.1
    class Robot:
        pass
