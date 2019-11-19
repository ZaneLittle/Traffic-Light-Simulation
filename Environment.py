import random
from LightQueue import LightQueue
from Car import Car
from TrafficLight import TrafficLight


class Environment:
    '''
        Represents our environment with 4 traffic lights
    '''

    def __init__(self, time, MAX_CARS=100):

        # [0] = north-west
        # [1] = north-east
        # [2] = south-west
        # [3] = south-east
        self.lights = [TrafficLight("NW"), TrafficLight("NE"),
                       TrafficLight("SE"), TrafficLight("SW")]

        self.lights[0].addNeighbour('e', self.lights[1])
        self.lights[0].addNeighbour('s', self.lights[3])

        self.lights[1].addNeighbour('w', self.lights[0])
        self.lights[1].addNeighbour('s', self.lights[2])

        self.lights[2].addNeighbour('n', self.lights[1])
        self.lights[2].addNeighbour('w', self.lights[3])

        self.lights[3].addNeighbour('n', self.lights[0])
        self.lights[3].addNeighbour('e', self.lights[2])

        self.MAX_CARS = MAX_CARS

    def addCarToQueue(self, car, time):
        position = car.route.pop(0)
        lightIdx = position[0]
        light = self.lights[lightIdx]
        queueIdx = position[1]
        queue = light.queues[queueIdx]

        initNumCars = light.getNumCars()
        queue.pushCar(car, time)
        numCars = light.getNumCars()

    def addAllCars(self, time):
        """
            Probabilistically determines how many cars should be added at a given
            time step
        """
        if self.getNumCars >= self.MAX_CARS:
            return

    def update(self, time):
        # Add car
        # For now only add one car so we can see if the environment is working properly
        newCar1 = Car([(0, 2), "s", "s"], startTime=time)
        newCar2 = Car([(3, 0), "n", "e", "e"], startTime=time)
        newCar3 = Car([(1, 1), "w", "s", "s"], startTime=time)
        newCar4 = Car([(2, 0), "n", "e", "s", "s"], startTime=time)
        if time == 0:
            self.addCarToQueue(newCar1, time)
            self.addCarToQueue(newCar2, time)
            self.addCarToQueue(newCar3, time)
            self.addCarToQueue(newCar4, time)
        if time == 5:
            self.addCarToQueue(newCar1, time)
            self.addCarToQueue(newCar2, time)
            self.addCarToQueue(newCar3, time)
            self.addCarToQueue(newCar4, time)
        for light in self.lights:
            light.updateQueues(time)

    # def getWaitTime(self, time):
    #     return sum([light.getWaitTime(time)[0]+light.getWaitTime(time)[1] for light in self.lights])

    def getNumCars(self):
        """
            Returns the total number of cars in the system.
        """
        return sum([light.getNumCars() for light in self.lights])

    def mapEnvironmentToState(self, time):
        """
            returns the state based on the environment
            [
                L1Direction,...,L4Direction,
                f(L1CulmTime(N/S)),f(L1CulmTime(E/W)),...,f(L4CulmTime(N/S)),f(L4CulmTime(E/W))
            ]
        """
        state = [1 if light.directionIsNorthSouth else 0 for light in self.lights]
        for light in self.lights:
            NSTotalTime, EWTotalTime = light.getWaitTimes(time)
            state += [NSTotalTime, EWTotalTime]
        return state

    def getCost(self, time):
        return sum(self.mapEnvironmentToState(time)[4:])

    def generateRoutes(self):
        """
        Returns a list of all possible routes a car can take
        Each route is a list where the first and last elements are the start and end points, and all elements
        in between are the queues (in order) that the car will take
        """
        # all_routes = []

        # # Traffic lights
        # nw_light = self.lights[0]
        # ne_light = self.lights[1]
        # sw_light = self.lights[2]
        # se_light = self.lights[3]

        # # Direction a queue is facing
        # dirs = {0: "n",
        #         1: "e",
        #         2: "s",
        #         3: "w"}

        # # Construct graph with the value of each vertex being a list of its neighbours
        # # Vertices 1, 2, 3, etc. are start/exit points beginning from the nw light north point
        # # going clockwise. Representing queues as strings and start/end points as ints for
        # # now just for testing
        # graph = {dirs[nw_light.queues[2].id]: [8, dirs[ne_light.queues[1].id], dirs[sw_light.queues[2].id]],
        #          dirs[nw_light.queues[3].id]: [1, 8, dirs[sw_light.queues[2].id]],
        #          "nw_light.qS": [8, 1, "ne_light.qW"],
        #          "nw_light.qW": [1, "ne_light.qW", "sw_light.qN"],
        #          "ne_light.qN": [3, "se_light.qN", "nw_light.qE"],
        #          "ne_light.qE": [2, "nw_light.qE", "se_light.qN"],
        #          "ne_light.qS": [3, 2, "nw_light.qE"],
        #          "ne_light.qW": [2, 3, "se_light.qN"],
        #          "se_light.qN": [4, 5, "sw_light.qE"],
        #          "se_light.qE": [5, "ne_light.qS", "sw_light.qE"],
        #          "se_light.qS": [4, "ne_light.qS", "sw_light.qE"],
        #          "se_light.qW": [5, 4, "ne_light.qS"],
        #          "sw_light.qN": [7, 6, "se_light.qW"],
        #          "sw_light.qE": [6, 7, "nw_light.qS"],
        #          "sw_light.qS": [7, "nw_light.qS", "se_light.qW"],
        #          "sw_light.qW": [6, "se_light.qW", "nw_light.qS"],
        #          1: ["nw_light.qN"],
        #          2: ["ne_light.qN"],
        #          3: ["ne_light.qE"],
        #          4: ["se_light.qE"],
        #          5: ["se_light.qS"],
        #          6: ["sw_light.qS"],
        #          7: ["sw_light.qW"],
        #          8: ["nw_light.qW"]}

        # def BFS(g, start_point, end_point):
        #     # Breadth first search for directed graph with no weights
        #     explored = []
        #     queue = [[start_point]]

        #     if start_point == end_point:
        #         return []

        #     while queue:
        #         path = queue.pop(0)
        #         node = path[-1]
        #         if node not in explored:
        #             neighbours = g[node]
        #             # Expand to neighbours and check if we have a complete path
        #             for neighbour in neighbours:
        #                 new_path = list(path) + [neighbour]
        #                 queue.append(new_path)
        #                 if neighbour == end_point:
        #                     return new_path

        #             explored.append(node)

        #     return []

            # # Shortest point from point a to point b can be found with BFS
            # for start in set(graph.keys()):
            #     if type(start) is int:
            #         # Exclude start point and iterate through every possible end point
            #         new_graph = {k: graph[k] for k in set(
            #             list(graph.keys())) - set([start])}
            #         for end in set(new_graph.keys()):
            #             if type(end) is int:
            #                 route = BFS(graph, start, end)
            #                 all_routes.append(route)

            # return all_routes}

    def __str__(self):
        nw = self.lights[0]
        ne = self.lights[1]
        sw = self.lights[2]
        se = self.lights[3]
        to_str = "\t   {} \t\t  {}\n".format(
            nw.queues[2].getNumCars(), ne.queues[2].getNumCars())
        to_str += "\t {} NW {}\t\t{} NE {}\n".format(nw.queues[1].getNumCars(
        ), nw.queues[3].getNumCars(), ne.queues[1].getNumCars(), nw.queues[3].getNumCars())
        to_str += "\t   {}\t\t  {}\n".format(
            nw.queues[0].getNumCars(), ne.queues[0].getNumCars())
        to_str += "\n\n"
        to_str += "\t   {} \t\t  {}\n".format(
            sw.queues[2].getNumCars(), se.queues[2].getNumCars())
        to_str += "\t {} SW {}\t\t{} SE {}\n".format(sw.queues[1].getNumCars(
        ), sw.queues[3].getNumCars(), se.queues[1].getNumCars(), sw.queues[3].getNumCars())
        to_str += "\t   {} \t\t  {}".format(
            sw.queues[0].getNumCars(), se.queues[0].getNumCars())

        return to_str
