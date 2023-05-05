import RPiSim.GPIO

class Constants:
    simulated = True
    GPIO = 'RPiSim.GPIO' if simulated else 'RPI.GPIO'



    