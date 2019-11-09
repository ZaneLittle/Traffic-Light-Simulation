from LightQueue import LightQueue
from Car import Car
from TrafficLight import TrafficLight

class Environment:
    '''
    Represents our environment with 4 traffic lights
    '''
    
    def __init__(self):
        self.lights = [TrafficLight(), TrafficLight(), TrafficLight(), TrafficLight()]