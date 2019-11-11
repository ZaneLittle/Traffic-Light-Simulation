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

    def generateRoutes(self):
        """
        Returns a list of all possible routes a car can take
        Each route is a list where the first and last elements are the start and end points, and all elements
        in between are the queues (in order) that the car will take 
        """
        all_routes = []

        nw_light = self.lights[0]
        ne_light = self.lights[1]
        sw_light = self.lights[2]
        se_light = self.lights[3]
        # Construct graph with the value of each vertex being a list of its neighbours
        # Vertices 1, 2, 3, etc. are start/exit points beginning from the nw light north point
        # going clockwise. Representing queues as strings and start/end points as ints for
        # now just for testing
        graph = {"nw_light.qN": [8, "ne_light.qW", "sw_light.qN"],
                    "nw_light.qE": [1, 8, "sw_light.qN"],
                    "nw_light.qS": [8, 1, "ne_light.qW"],
                    "nw_light.qW": [1, "ne_light.qW", "sw_light.qN"],
                    "ne_light.qN": [3, "se_light.qN", "nw_light.qE"],
                    "ne_light.qE": [2, "nw_light.qE", "se_light.qN"],
                    "ne_light.qS": [3, 2, "nw_light.qE"],
                    "ne_light.qW": [2, 3, "se_light.qN"],
                    "se_light.qN": [4, 5, "sw_light.qE"],
                    "se_light.qE": [5, "ne_light.qS", "sw_light.qE"],
                    "se_light.qS": [4, "ne_light.qS", "sw_light.qE"],
                    "se_light.qW": [5, 4, "ne_light.qS"],
                    "sw_light.qN": [7, 6, "se_light.qW"],
                    "sw_light.qE": [6, 7, "nw_light.qS"],
                    "sw_light.qS": [7, "nw_light.qS", "se_light.qW"],
                    "sw_light.qW": [6, "se_light.qW", "nw_light.qS"],
                    1: ["nw_light.qN"],
                    2: ["ne_light.qN"],
                    3: ["ne_light.qE"],
                    4: ["se_light.qE"],
                    5: ["se_light.qS"],
                    6: ["sw_light.qS"],
                    7: ["sw_light.qW"],
                    8: ["nw_light.qW"]}

        # Breadth first search for directed graph with no weights
        def  BFS(g, start_point, end_point):
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
        
        # Shortest point from point a to point b can be found with BFS
        for start in set(graph.keys()):
            if type(start) is int:
                # Exclude start point and iterate through every possible end point
                new_graph = {k: graph[k] for k in set(list(graph.keys())) - set([start])}
                for end in set(new_graph.keys()):
                    if type(end) is int:
                        route = BFS(graph, start, end)
                        all_routes.append(route)
        
        return all_routes