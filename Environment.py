import random
from LightQueue import LightQueue
from Car import Car
from TrafficLight import TrafficLight
from config import ENV_CONSTANTS

class Environment:
    '''
        Represents our environment with 4 traffic lights
    '''

    def __init__(self, time):
        # [0] = north-west
        # [1] = north-east
        # [2] = south-east
        # [3] = south-west
        self.__init_lights()
        self.currentTime = time
        self.lights = self.__init_lights()
        self.MAX_CARS = ENV_CONSTANTS["MAX_CARS"]
        self.isRushHour = self.__highTraffic(time)

    def __init_lights(self):
        lights = [None,None,None,None]
        for key in ENV_CONSTANTS["LIGHT_POSITIONS"]:
            # NW light has a key at 0, this is the index in the lights array that it will reside
            position = ENV_CONSTANTS["LIGHT_POSITIONS"][key]
            lights[position] = TrafficLight(key)   
        NW = ENV_CONSTANTS["LIGHT_POSITIONS"]["NW"]
        NE = ENV_CONSTANTS["LIGHT_POSITIONS"]["NE"]
        SE = ENV_CONSTANTS["LIGHT_POSITIONS"]["SE"]
        SW = ENV_CONSTANTS["LIGHT_POSITIONS"]["SW"]
        lights[NW].addNeighbour('e', lights[NE])
        lights[NW].addNeighbour('s', lights[SW])

        lights[NE].addNeighbour('w', lights[NW])
        lights[NE].addNeighbour('s', lights[SE])

        lights[SE].addNeighbour('n', lights[NE])
        lights[SE].addNeighbour('w', lights[SW])

        lights[SW].addNeighbour('n', lights[NW])
        lights[SW].addNeighbour('e', lights[SE])
        return lights

    def addCarToQueue(self, car, time):
        position = car.route.pop(0)
        lightIdx = position[0]
        light = self.lights[lightIdx]
        queueIdx = position[1]
        queue = light.queues[queueIdx]

        queue.pushCar(car, time)

    def __highTraffic(self,time):
        return any(t[0] <= time <= t[1] for t in ENV_CONSTANTS["RUSH_HOUR_TIMES"])

    # TODO: create path through update for all_routes
    def addAllCars(self, time, allRoutes):
        """
            Probabilistically determines how many cars should be added at a given
            time step
        """

        highTraffic = self.__highTraffic(time)
        numCarsToAdd = 0

        if highTraffic:
            numCarsToAdd = random.randint(5, 10)
        else:
            numCarsToAdd = random.randint(0, 4)

        numCarsToAdd = min(self.MAX_CARS - self.getNumCars(), numCarsToAdd)

        for _ in range(numCarsToAdd):
            route = random.choice(allRoutes)[:]
            newCar = Car(route, startTime=time)
            self.addCarToQueue(newCar, time)

    def update(self, time, allRoutes):
        self.addAllCars(time, allRoutes)
        travelTimes = []
        for light in self.lights:
            travelTimes += light.updateQueues(time) # concat
        self.currentTime = time
        self.isRushHour = self.__highTraffic(time)
        if self.getNumCars():
            return self.getCost(time)/self.getNumCars(), travelTimes
        return 0, travelTimes

    def getNumCars(self):
        """
            Returns the total number of cars in the system.
        """
        return sum([light.getNumCars() for light in self.lights])

    def getCarWaits(self, time):
        """
            Returns the total wait time for that time step
        """
        waits = []
        for light in self.lights:
            for queue in light.queues:
                for car in queue.cars:
                    waits.append(time - car.startTime)
        return waits

    def getCarTravelDuration(self, time):
        """
            Returns the total wait time for that time step
        """
        waits = []
        for light in self.lights:
            for queue in light.queues:
                for car in queue.cars:
                    waits.append(time - car.enteredEnvironment)
        return waits

    def toState(self, time):
        """
            returns the state based on the environment
            [
                L1Direction,...,L4Direction,
                f(L1CulmTime(N/S)),f(L1CulmTime(E/W)),...,f(L4CulmTime(N/S)),f(L4CulmTime(E/W)),
                timeOfDay
            ]
        """
        state = [1 if light.directionIsNorthSouth else 0 for light in self.lights]
        for light in self.lights:
            NSTotalTime, EWTotalTime = light.getWaitTimes(time, sum(self.getCarWaits(time)))
            state += [NSTotalTime, EWTotalTime]
        # timeOfDay = 0
        # for ind,timeTup in enumerate(ENV_CONSTANTS["TIME_INTERVALS"]):
        #     if timeTup[0] <= time <= timeTup[1]:
        #         timeOfDay = ind
        #         break
        # state.append(timeOfDay)
        return state


    def getCost(self, time):
        return sum(self.toState(time)[4:-1])

    def generateRoutes(self):
        """
            Returns a list of all possible routes a car can take
            Each route is a list where the first element is a tuple (start light, queue direction) and
            subsequent elements are optimal actions for the car
        """

       #====================== Helper functions here ======================
        def BFS(g, startPoint, endPoint):
            """
                Breadth first search for directed graph with no weights
            """
            explored = []
            queue = [[startPoint]]

            if startPoint == endPoint:
                return []

            while queue:
                path = queue.pop(0)
                node = path[-1]
                if node not in explored:
                    neighbours = g[node]
                    # Expand to neighbours and check if we have a complete path
                    for neighbour in neighbours:
                        newPath = list(path) + [neighbour]
                        queue.append(newPath)
                        if neighbour == endPoint:
                            return newPath

                    explored.append(node)

            return []

        allRoutes = []

        def getExitAction(exitPoint):
            """
                Returns finaction a car should take to exit at the correct location
            """
            if exitPoint == 1 or exitPoint == 2:
                return "n"
            elif exitPoint == 3 or exitPoint == 4:
                return "e"
            elif exitPoint == 5 or exitPoint == 6:
                return "s"
            else:
                return "w"

        # Construct graph with the value of each vertex being a list of its neighbours
        # Vertices 1, 2, 3, etc. are start/exit points beginning from the NW light north point
        # going clockwise. Light queues are represented as a tuple (Traffic light, direction)
        NW = ENV_CONSTANTS["LIGHT_POSITIONS"]["NW"]
        NE = ENV_CONSTANTS["LIGHT_POSITIONS"]["NE"]
        SE = ENV_CONSTANTS["LIGHT_POSITIONS"]["SE"]
        SW = ENV_CONSTANTS["LIGHT_POSITIONS"]["SW"]

        graph = {(NW, "s"): [8, (NE, "e"), (SW, "s")],
                 (NW, "w"): [NE, 8, (SW, "s")],
                 (NW, "n"): [8, 1, (NE, "e")],
                 (NW, "e"): [1, (NE, "e"), (SW, "s")],
                 (NE, "s"): [3, (SE, "s"), (NW, "w")],
                 (NE, "w"): [2, (NW, "w"), (SE, "s")],
                 (NE, "n"): [3, 2, (NW, "w")],
                 (NE, "e"): [2, 3, (SE, "s")],
                 (SE, "s"): [4, 5, (SW, "w")],
                 (SE, "w"): [5, (NE, "n"), (SW, "w")],
                 (SE, "n"): [4, (NE, "n"), (SW, "w")],
                 (SE, "e"): [5, 4, (NE, "n")],
                 (SW, "s"): [7, 6, (SE, "e")],
                 (SW, "w"): [6, 7, (NW, "n")],
                 (SW, "n"): [7, (NW, "n"), (SE, "e")],
                 (SW, "e"): [6, (SE, "e"), (NW, "n")],
                 1: [(NW, "s")],
                 2: [(NE, "s")],
                 3: [(NE, "w")],
                 4: [(SE, "w")],
                 5: [(SE, "n")],
                 6: [(SW, "n")],
                 7: [(SW, "e")],
                 8: [(NW, "e")]}

        # Shortest point from point a to point b can be found with BFS
        # "Start points" are represented as ints in the graph whereas queues are represented as tuples
        for start in set(graph.keys()):
            if type(start) is int: 
                # Exclude start point and iterate through every possible end point
                newGraph = {k: graph[k] for k in set(
                    list(graph.keys())) - set([start])}
                for end in set(newGraph.keys()):
                    if type(end) is int:
                        route = BFS(graph, start, end)
                        allRoutes.append(route)

        # Currently a route has the form [start, (light, dir), ..., (light, dir), end]. We need to
        # modify the list so that each route has first element as tuple (starting light, direction) and
        # subsequent elements as actions.
        # e.g. [(0, 2), "s", "s"] ==> starting at NW light's queue facing south, go south, go south
        dirs = ENV_CONSTANTS["QUEUE_DIR"]
        for idx, route in enumerate(allRoutes):
            newRoute = []
            startLight = route[1][0]  # Second element in route is a tuple, first element in tuple is light
            startDir = dirs[route[1][1]]  # Second element in tuple is queue direction
            newRoute.append((startLight, startDir))  # Add on starting light and queue
            for queue in route[2:-1]:
                newRoute.append(queue[1])  # Add on action
            newRoute.append(getExitAction(route[-1]))
            allRoutes[idx] = newRoute
            
        return allRoutes

    def __str__(self):
        NW  = ENV_CONSTANTS["LIGHT_POSITIONS"]["NW"]
        NE  = ENV_CONSTANTS["LIGHT_POSITIONS"]["NE"]
        SE  = ENV_CONSTANTS["LIGHT_POSITIONS"]["SE"]
        SW  = ENV_CONSTANTS["LIGHT_POSITIONS"]["SW"]
        n   = ENV_CONSTANTS["QUEUE_DIR"]["n"]
        e   = ENV_CONSTANTS["QUEUE_DIR"]["e"]
        s   = ENV_CONSTANTS["QUEUE_DIR"]["s"]
        w   = ENV_CONSTANTS["QUEUE_DIR"]["w"]

        nw = self.lights[NW]
        ne = self.lights[NE]
        sw = self.lights[SW]
        se = self.lights[SE]
        to_str = "\t   {} \t\t  {}\n".format(
            nw.queues[s].getNumCars(), ne.queues[s].getNumCars())
        to_str += "\t {} NW {}\t\t{} NE {}\n".format(nw.queues[e].getNumCars(
        ), nw.queues[w].getNumCars(), ne.queues[e].getNumCars(), nw.queues[w].getNumCars())
        to_str += "\t   {}\t\t  {}\n".format(
            nw.queues[n].getNumCars(), ne.queues[n].getNumCars())
        to_str += "\n\n"
        to_str += "\t   {} \t\t  {}\n".format(
            sw.queues[s].getNumCars(), se.queues[s].getNumCars())
        to_str += "\t {} SW {}\t\t{} SE {}\n".format(sw.queues[e].getNumCars(
        ), sw.queues[w].getNumCars(), se.queues[e].getNumCars(), sw.queues[w].getNumCars())
        to_str += "\t   {} \t\t  {}".format(sw.queues[n].getNumCars(), se.queues[n].getNumCars())
        return to_str
