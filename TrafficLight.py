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
        self.cost = 0

    def updateCost(self, time):
        ''' return sum of cost of queues at this light '''
        self.cost = self.qN.cost(time) + self.qE.cost(time) + \
            self.qS.cost(time) + self.qW.cost(time)

    def updateQueues(self, time):
        ''' Move cars in direction the light is set '''
        queues = []
        if self.direction:
            queues = [self.qN, self.qS]
        else:
            queues = [self.qE,  self.qW]

        for queue in queues:
            for car in queue.cars:
                if not car.route:
                    queue.pop()
                else:
                    nextCarAction = car.route.pop()
                    if nextCarAction == "n":
                        self.northNeighbour.push(queue.pop(), time)
                    elif nextCarAction == "e":
                        self.eastNeighbour.push(queue.pop(), time)
                    elif nextCarAction == "s":
                        self.southNeighbour.push(queue.pop(), time)
                    else:  # w
                        self.westNeighbour.push(queue.pop(), time)
        self.updateCost(time)
