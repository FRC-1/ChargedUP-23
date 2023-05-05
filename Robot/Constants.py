import RPiSim.GPIO

class Constants:
    class Simulation:
        Simulated = True
        GPIO = 'RPiSim.GPIO' if Simulated else 'RPI.GPIO'
    class Robot:
        pass
