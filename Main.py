from Environment import Environment
from Agent import Agent

MAX_CARS = 10

environment = Environment(0, MAX_CARS)
agent = Agent(environment)

# Testing route generation
routes = environment.generateRoutes()

for time in range(10):
    print("Time step: {}".format(time))
    lightDirections = [
        "north/south" if light.directionIsNorthSouth
        else "east/west"
        for light in environment.lights
    ]
    print("Directions for traffic lights: {}".format(lightDirections))
    environment.update(time)
    print(str(environment))
    print("state: {}".format(environment.mapEnvironmentToState(time)))
