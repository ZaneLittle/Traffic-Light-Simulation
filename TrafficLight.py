import math
from LightQueue import LightQueue
from Car import Car


class TrafficLight:
    '''
    Defines the representation of a single traffic light in our environment
    '''

    def __init__(self):
        self.directionIsNorthSouth = False
        self.queues = [LightQueue(), LightQueue(), LightQueue(), LightQueue()]
        self.neighbours = [None, None, None, None]
        self.dirs = {
            "n": 0,
            "e": 1,
            "s": 2,
            "w": 3
        }

    def updateDirection(self, time):
        self.directionIsNorthSouth = math.sin(time) > 0

    def getNumCars(self):
        return sum([queue.getNumCars() for queue in self.queues])

    def getWaitTime(self, time):
        def _bin(wait_time):
            # Bin total_wait_time
            if wait_time > 30:
                return  9
            elif wait_time > 20:
                return  4
            else:
                return 1
        ''' return wait times of queues at this light '''
        northSouth = self.queues[0].getWaitTime(
            time)+self.queues[2].getWaitTime(time)
        eastWest = self.queues[1].getWaitTime(
            time)+self.queues[3].getWaitTime(time)
        return _bin(northSouth), _bin(eastWest)

    def pushCar(self, car, action, time):
        """
            Takes in car to be pushed to an adjacent traffic lights queue
            action == "n" => push car to north neighbours south queue
            action == "s" => push car to south neighbours north queue
            ... etc.
        """
        queue = None
        if action == "n":
            queue = self.queues[2]  # add car to south queue
        elif action == "e":
            queue = self.queues[3]
        elif action == "s":
            queue = self.queues[0]
        else:  # w
            queue = self.queues[1]

        initLength = queue.getNumCars()
        initLightLength = self.getNumCars()

        queue.pushCar(car, time)

        assert(queue.getNumCars() - initLength == 1)
        assert(self.getNumCars() - initLightLength == 1)

    def updateQueues(self, time):
        ''' Move cars in direction the light is set '''
        self.updateDirection(time)
        queues = []
        if self.directionIsNorthSouth:
            queues = [self.queues[0], self.queues[2]]
        else:
            queues = [self.queues[1], self.queues[3]]

        for queue in queues:
            for car in queue.cars:
                initQueueLength = queue.getNumCars()
                queue.popCar()
                assert(initQueueLength - queue.getNumCars() == 1)
                if not car.route:
                    del car
                    break
                nextCarAction = car.route.pop(0)
                if self.dirs[nextCarAction] is None:
                    # If a car is at the north most intersection and want's to continue north,
                    # it exits the city
                    initLength = len(self.cars)
                    del car
                    assert(len(self.cars) - initLength == 1)
                else:
                    lightIndex = self.dirs[nextCarAction]
                    lightToPush = self.neighbours[lightIndex]
                    initLength = lightToPush.getNumCars()

                    lightToPush.pushCar(car, nextCarAction, time)
                    assert(lightToPush.getNumCars() -
                           initLength == 1)  # actually equals 4

    def addNeighbour(self, direction, light):
        """
            Takes in a direction (n,e,s,w) and a traffic light and adds it to be an adjacent
            traffic light.
        """
        lightToChange = self.dirs[direction]
        self.neighbours[lightToChange] = light
