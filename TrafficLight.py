import math
from LightQueue import LightQueue
from Car import Car
from config import LIGHT_CONSTANTS
import random


class TrafficLight:
    '''
        Defines the representation of a single traffic light in our environment
    '''

    def __init__(self, id):
        self.directionIsNorthSouth = bool(random.getrandbits(1))
        self.timeChanged = 0
        self.id = id
        self.queues = self.__init_queues()
        # LIGHT NOTATION: 0 = northern neighbour, 1 = east neighbour, 2 = south neighbour, 3 = west neighbour
        self.neighbours = [None, None, None, None]
    
    def __init_queues(self):
        queues = []
        for direction in LIGHT_CONSTANTS["ACTION_DIR"]:
            id = LIGHT_CONSTANTS["ACTION_DIR"][direction]
            queues.append(LightQueue(id))
        return queues

    def changeLight(self, time):
        ''' Toggle light direction and set time '''
        self.directionIsNorthSouth = not self.directionIsNorthSouth
        self.timeChanged = time

    def getNumCars(self):
        return sum([queue.getNumCars() for queue in self.queues])

    def getNumCarsWaiting(self):
        return sum([queue.getNumCarsWaiting() for queue in self.queues])

    def getWaitTimes(self, time):
        def __bin(wait_time):
            # Bin the total wait time
            # Update size of Q table if number of bins changes
            if wait_time > LIGHT_CONSTANTS["TIME_BINS"]["large"]["lowerBound"]:
                return LIGHT_CONSTANTS["TIME_BINS"]["large"]["penalty"]
            elif wait_time > LIGHT_CONSTANTS["TIME_BINS"]["medium"]["lowerBound"]:
                return LIGHT_CONSTANTS["TIME_BINS"]["medium"]["penalty"]
            else:
                return LIGHT_CONSTANTS["TIME_BINS"]["small"]["penalty"]
        NS = __bin(self.queues[0].getWaitTimes(time) + self.queues[2].getWaitTimes(time))
        EW = __bin(self.queues[1].getWaitTimes(time) + self.queues[3].getWaitTimes(time))
        return NS, EW

    def pushCarToNextLight(self, car, action, time):
        """
            Takes in car to be pushed to an adjacent traffic lights queue
            action == "n" => push car to north neighbour's north facing queue
            action == "s" => push car to south neighbour's south facing queue
            ... etc.
        """
        direction = LIGHT_CONSTANTS["ACTION_DIR"][action]
        assert self.neighbours[direction], "neighbor does not exist"
        queue = self.neighbours[direction].queues[direction]
        initLength = queue.getNumCars()
        queue.pushCar(car, time)
        assert(queue.getNumCars() - initLength == 1)

    def updateQueues(self, time):
        ''' Move cars in direction the light is set '''
        def __subtract(car): car.delay = max(0,car.delay-1)
        queues = []
        if self.directionIsNorthSouth:
            queues = [self.queues[0], self.queues[2]]
        else:
            queues = [self.queues[1], self.queues[3]]

        for queue in self.queues:
            for car in queue.cars:
                car.delay = max(0,car.delay-1)
                # map(__subtract,queue.cars)
        for queue in queues:
            if queue.getNumCars():
                peakedCar = queue.peakCar()
                assert(peakedCar.route)
                nextCarAction = peakedCar.route[0]
                direction = LIGHT_CONSTANTS["ACTION_DIR"][nextCarAction]
                if peakedCar.delay > 0:
                    peakedCar.delay = max(0,peakedCar.delay-1)
                else:
                    if peakedCar.canClear and self.neighbours[direction] is None:
                        # If a car is at the north most intersection and wants to continue north,
                        # it exits the city
                        queue.popCar()
                        del peakedCar
                    elif not peakedCar.canClear: 
                        # add a delay so that the car doesn't immediately pass through the intersection
                        peakedCar.canClear = not peakedCar.canClear
                    else:
                        car = queue.popCar()
                        car.route.pop(0)
                        car.canClear = False
                        car.delay = car.MAX_DELAY
                        self.pushCarToNextLight(car, nextCarAction, time)

    def addNeighbour(self, direction, light):
        """
            Takes in a direction (n,e,s,w) and a traffic light and adds it to be an adjacent 
            traffic light.
        """
        lightToChange = LIGHT_CONSTANTS["ACTION_DIR"][direction]
        self.neighbours[lightToChange] = light

    def __str__(self):
        return "< {}. Total Cars: {}>".format(self.id, self.getNumCars())
