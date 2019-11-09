from LightQueue import LightQueue
from Car import Car

class TrafficLight:
    '''
    Defines the representation of a single traffic light in our environment
    '''

    def __init__(self):
        self.direction = True
        self.qN = LightQueue()
        self.qS = LightQueue()
        self.qE = LightQueue()
        self.qW = LightQueue()