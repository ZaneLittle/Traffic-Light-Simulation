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
            Each route is a list where the first element is a tuple (start light, queue direction) and
            subsequent elements are optimal actions for the car
        """

       #====================== Helper functions here ======================
        def BFS(g, start_point, end_point):
            """
                Breadth first search for directed graph with no weights
            """
            explored = []
            queue = [[start_point]]

            if start_point == end_point:
                return []

            while queue:
                path = queue.pop(0)
                node = path[-1]
                if node not in explored:
                    neighbours = g[node]
                    # Expand to neighbours and check if we have a complete path
                    for neighbour in neighbours:
                        new_path = list(path) + [neighbour]
                        queue.append(new_path)
                        if neighbour == end_point:
                            return new_path

                    explored.append(node)

            return []

        all_routes = []

        def get_exit_action(exit_point):
            """
                :param exit_point: integer represeting exit location
                :return: action that car should take to exit the environment
            """
            if exit_point == 1 or exit_point == 2:
                return "n"
            elif exit_point == 3 or exit_point == 4:
                return "e"
            elif exit_point == 5 or exit_point == 6:
                return "s"
            else:
                return "w"

        # Construct graph with the value of each vertex being a list of its neighbours
        # Vertices 1, 2, 3, etc. are start/exit points beginning from the NW light north point
        # going clockwise. Light queues are represented as a tuple (Traffic light, direction)
        # Traffic light dictionary:
        #   0: NW
        #   1: NE
        #   2: SE
        #   3: SW
        graph = {(0, "s"): [8, (1, "e"), (3, "s")],
                 (0, "w"): [1, 8, (3, "s")],
                 (0, "n"): [8, 1, (1, "e")],
                 (0, "e"): [1, (1, "e"), (3, "s")],
                 (1, "s"): [3, (2, "s"), (0, "w")],
                 (1, "w"): [2, (0, "w"), (2, "s")],
                 (1, "n"): [3, 2, (0, "w")],
                 (1, "e"): [2, 3, (2, "s")],
                 (2, "s"): [4, 5, (3, "w")],
                 (2, "w"): [5, (1, "n"), (3, "w")],
                 (2, "n"): [4, (1, "n"), (3, "w")],
                 (2, "e"): [5, 4, (1, "n")],
                 (3, "s"): [7, 6, (2, "e")],
                 (3, "w"): [6, 7, (0, "n")],
                 (3, "n"): [7, (0, "n"), (2, "e")],
                 (3, "e"): [6, (2, "e"), (0, "n")],
                 1: [(0, "s")],
                 2: [(1, "s")],
                 3: [(1, "w")],
                 4: [(2, "w")],
                 5: [(2, "n")],
                 6: [(3, "n")],
                 7: [(3, "e")],
                 8: [(0, "e")]}

        # Shortest point from point a to point b can be found with BFS
        for start in set(graph.keys()):
            if type(start) is int:
                # Exclude start point and iterate through every possible end point
                new_graph = {k: graph[k] for k in set(
                    list(graph.keys())) - set([start])}
                for end in set(new_graph.keys()):
                    if type(end) is int:
                        route = BFS(graph, start, end)
                        all_routes.append(route)

        # Currently a route has the form [start, (light, dir), ..., (light, dir), end]. We need to
        # modify the list so that each route has first element as tuple (starting light, direction) and
        # subsequent elements as actions.
        # e.g. [(0, 2), "s", "s"] ==> starting at NW light's queue facing south, go south, go south
        dirs = {"n": 0, "e": 1, "s": 2, "w": 3}
        for idx, route in enumerate(all_routes):
            new_route = []
            start_light = route[1][0]
            start_dir = dirs[route[1][1]]
            new_route.append((start_light, start_dir))  # Add on starting light and queue
            for queue in route[2:-1]:
                new_route.append(queue[1])  # Add on action
            new_route.append(get_exit_action(route[-1]))
            all_routes[idx] = new_route

        return all_routes

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
