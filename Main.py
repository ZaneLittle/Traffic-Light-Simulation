from Environment import Environment
from Agent import Agent

environment = Environment(0)
agent = Agent(environment)

# Testing route generation
routes = environment.generateRoutes()
# print(routes)

for time in range(5):
    print("Time step: {}".format(time))
    lightDirections = [
        "north/south" if light.directionIsNorthSouth else "east/west" for light in environment.lights]
    print("Direction for traffic lights: {}".format(lightDirections))
    # print("Env num cars: sum({}) = {}"
    #       .format([light.getNumCars() for light in environment.lights],
    #               environment.getNumCars()))

    # print(environment.mapEnvironmentToState(time))
    # print("Total wait time: {}".format(environment.getWaitTime(time)))

    environment.update(time)
    print(str(environment))
    agent.update(time)
