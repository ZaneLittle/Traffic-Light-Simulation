import random
from LightQueue import LightQueue
from Car import Car
from TrafficLight import TrafficLight


class Environment:
    '''
    Represents our environment with 4 traffic lights
    '''

    def __init__(self, time):

        # [0] = north-west
        # [1] = north-east
        # [2] = south-west
        # [3] = south-east
        self.lights = [TrafficLight(), TrafficLight(),
                       TrafficLight(), TrafficLight()]

        self.lights[0].eastNeighbor = self.lights[1]
        self.lights[0].southNeighbor = self.lights[2]

        self.lights[1].westNeighbor = self.lights[0]
        self.lights[1].southNeighbor = self.lights[3]

        self.lights[2].northNeighbor = self.lights[0]
        self.lights[2].eastNeighbor = self.lights[3]

        self.lights[3].northNeighbor = self.lights[1]
        self.lights[3].westNeighbor = self.lights[2]

        self.cars = []
        self.cost = sum([light.cost for light in self.lights])

        self.possibleRoutes = [[(0, 0), "n", "n"]]

    def removeCompleteCars(self):
        self.cars = [c for c in self.cars if c.route]

    def update(self, time):
        # Add car
        route = random.choice(self.possibleRoutes)
        self.cars.append(Car(route, start_time=time))
        # TODO: initialize car in a queue based on start position
        # Check if cars should be removed
        for light in self.lights:
            light.updateQueues(time)

        self.removeCompleteCars()
        self.updateCost(time)

    def updateCost(self, time):
        self.cost = sum([light.cost for light in self.lights])
