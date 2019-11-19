import math
from LightQueue import LightQueue
from Car import Car


class TrafficLight:
    '''
        Defines the representation of a single traffic light in our environment
    '''

    def __init__(self, id):
        self.directionIsNorthSouth = False
        self.timeChanged = 0
        self.id = id
        self.queues = [LightQueue(0), LightQueue(
            1), LightQueue(2), LightQueue(3)]
        # LIGHT NOTATION: 0 = northern neighbour, 1 = east neighbour, 2 = south neighbour, 3 = west neighbour
        self.neighbours = [None, None, None, None]
        self.dirs = {  # direction the car is facing in that queue
            "n": 0,
            "e": 1,
            "s": 2,
            "w": 3
        }
    
    def changeLight(self, time):
        ''' Toggle light direction and set time '''
        self.directionIsNorthSouth = not self.directionIsNorthSouth
        self.timeChanged = time

    def getNumCars(self):
        return sum([queue.getNumCars() for queue in self.queues])

    def getWaitTimes(self, time):
        def _bin(wait_time):
            # Bin total_wait_time
            if wait_time > 30:
                return 9
            elif wait_time > 15:
                return 4
            else:
                return 1

        NS = _bin(sum(self.queues[0].getWaitTimes(
            time) + self.queues[2].getWaitTimes(time)))
        EW = _bin(sum(self.queues[1].getWaitTimes(
            time) + self.queues[3].getWaitTimes(time)))
        return NS, EW

    def pushCarToNextLight(self, car, action, time):
        """
            Takes in car to be pushed to an adjacent traffic lights queue
            action == "n" => push car to north neighbour's north facing queue
            action == "s" => push car to south neighbour's south facing queue
            ... etc.
        """
        QUEUE_POSITION = {
            "NW": 0,
            "NE": 1,
            "SW": 2,
            "SE": 3
        }
        direction = self.dirs[action]
        assert self.neighbours[direction], "neighbor does not exist"
        queue = self.neighbours[direction].queues[direction]
        initLength = queue.getNumCars()
        queue.pushCar(car, time)
        car.position = (
            QUEUE_POSITION[self.neighbours[direction].id], queue.id)
        print(car.position)
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
                peakedCar = queue.peakCar()
                assert(peakedCar.route)
                nextCarAction = peakedCar.route[0]
                direction = self.dirs[nextCarAction]
                if not peakedCar.delay and self.neighbours[direction] is None:
                    # If a car is at the north most intersection and wants to continue north,
                    # it exits the city
                    queue.popCar()
                    del peakedCar
                elif not peakedCar.delay:
                    car = queue.popCar()
                    car.route.pop(0)
                    car.delay = car.MAX_DELAY
                    lightToPush = self.neighbours[direction]
                    self.pushCarToNextLight(car, nextCarAction, time)
                else:
                    peakedCar.delay -= 1

    def addNeighbour(self, direction, light):
        """
            Takes in a direction (n,e,s,w) and a traffic light and adds it to be an adjacent 
            traffic light.
        """
        lightToChange = self.dirs[direction]
        self.neighbours[lightToChange] = light

    def __str__(self):
        return "< {}. Total Cars: {}>".format(self.id, self.getNumCars())
