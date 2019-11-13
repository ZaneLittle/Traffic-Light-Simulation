import math
from LightQueue import LightQueue
from Car import Car


class TrafficLight:
    '''
    Defines the representation of a single traffic light in our environment
    '''

    def __init__(self):
        self.direction = True
        self.qN = LightQueue()
        self.qE = LightQueue()
        self.qS = LightQueue()
        self.qW = LightQueue()
        self.northNeighbour = None
        self.eastNeighbour = None
        self.southNeighbour = None
        self.westNeighbour = None

    def updateDirection(self, time):
        self.direction = math.sin(time) > 0

    def numCars(self):
        return len(self.qN.cars)+len(self.qE.cars)+len(self.qS.cars)+len(self.qW.cars)

    def getCost(self, time):
        ''' return sum of cost of queues at this light '''
        return self.qN.getCost(time) + self.qE.getCost(time) + self.qS.getCost(time) + self.qW.getCost(time)

    def updateQueues(self, time):
        ''' Move cars in direction the light is set '''
        self.updateDirection(time)
        queues = []
        if self.direction:
            queues = [self.qN, self.qS]
        else:
            queues = [self.qE,  self.qW]

        for queue in queues:
            # print(len(queue.cars))
            for car in queue.cars:
                if not car.route:
                    queue.pop()
                else:
                    dirs = {
                        "n": self.northNeighbour,
                        "e": self.eastNeighbour,
                        "s": self.southNeighbour,
                        "w": self.westNeighbour
                    }
                    nextCarAction = car.route.pop(0)
                    poppedCar = queue.popCar()
                    if dirs[nextCarAction] is None:
                        # If a car is at the north most intersection and want's to continue north,
                        # it exits the city
                        del poppedCar
                    else:
                        dirs[nextCarAction].pushCar(poppedCar, time)
        self.updateCost(time)

    def addNeighbour(self, direction, light):
        """
            Takes in a direction (n,e,s,w) and a traffic light and adds it to be an adjacent
            traffic light.
        """
        dirs = {
            "n": self.northNeighbour,
            "e": self.eastNeighbour,
            "s": self.southNeighbour,
            "w": self.westNeighbour
        }
        dirs[direction] = light
