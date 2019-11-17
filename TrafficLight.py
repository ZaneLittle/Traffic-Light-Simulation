import math
from LightQueue import LightQueue
from Car import Car


class TrafficLight:
    '''
        Defines the representation of a single traffic light in our environment
    '''

    def __init__(self, id):
        self.directionIsNorthSouth = False
        self.id = id
        self.queues = [LightQueue("{} - Direction north".format(id)), LightQueue(
            "{} - Direction east".format(id)), LightQueue("{} - Direction south".format(id)), LightQueue("{} - Direction west".format(id))]
        # LIGHT NOTATION: 0 = northern neighbour, 1 = east neighbour, 2 = south neighbour, 3 = west neighbour
        self.neighbours = [None, None, None, None]
        self.dirs = {  # direction the car is facing in that queue
            "n": 0,
            "e": 1,
            "s": 2,
            "w": 3
        }

    def getNumCars(self):
        return sum([queue.getNumCars() for queue in self.queues])

    def getWaitTime(self, time):
        def _bin(wait_time):
            # Bin total_wait_time
            if wait_time > 30:
                return 9
            elif wait_time > 15:
                return 4
            else:
                return 1
        ''' return wait times of queues at this light '''
        northSouth = self.queues[0].getWaitTime(
            time)+self.queues[2].getWaitTime(time)
        eastWest = self.queues[1].getWaitTime(
            time)+self.queues[3].getWaitTime(time)
        return _bin(northSouth), _bin(eastWest)

    def pushCarToNextLight(self, car, action, time):
        """
            Takes in car to be pushed to an adjacent traffic lights queue
            action == "n" => push car to north neighbour's north facing queue
            action == "s" => push car to south neighbour's south facing queue
            ... etc.
        """
        direction = self.dirs[action]
        assert self.neighbours[direction], "neighbor does not exist"
        queue = self.neighbours[direction].queues[direction]
        initLength = queue.getNumCars()
        queue.pushCar(car, time)
        assert(queue.getNumCars() - initLength == 1)

    def updateQueues(self, time):
        ''' Move cars in direction the light is set '''
        queues = []
        if self.directionIsNorthSouth:
            queues = [self.queues[0], self.queues[2]]
        else:
            queues = [self.queues[1], self.queues[3]]

        for queue in queues:
            if queue.getNumCars():
                initQueueLength = queue.getNumCars()
                car = queue.peakCar()
                assert(car.route)
                nextCarAction = car.route.pop(0)
                direction = self.dirs[nextCarAction]
                assert(nextCarAction)
                if self.neighbours[direction] is None:
                    # If a car is at the north most intersection and wants to continue north,
                    # it exits the city
                    del car
                else:
                    if not car.delay:
                        car = queue.popCar()
                        car.delay = car.MAX_DELAY
                        lightToPush = self.neighbours[direction]
                        print("Pushing car from {} to {}".format(
                            self.id, lightToPush))
                        self.pushCarToNextLight(car, nextCarAction, time)
                        print(lightToPush)
                    else:
                        print("Delay: {} -> {}".format(car.delay, car.delay-1))
                        car.delay -= 1

    def addNeighbour(self, direction, light):
        """
            Takes in a direction (n,e,s,w) and a traffic light and adds it to be an adjacent 
            traffic light.
        """
        lightToChange = self.dirs[direction]
        self.neighbours[lightToChange] = light

    def __repr__(self):
        return "< {}. Total Cars: {}>".format(self.id, self.getNumCars())
