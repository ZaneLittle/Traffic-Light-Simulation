from Environment import Environment
from Agent import Agent
from config import ENV_CONSTANTS
import matplotlib.pyplot as plt

def plot(rewardHistory, carsHistory):
    plt.subplot(2, 1, 1)
    plt.plot(rewardHistory)
    plt.ylabel('Average Reward')

    plt.subplot(2, 1, 2)
    plt.plot(carsHistory)
    plt.xlabel('time')
    plt.ylabel('Number of Cars')

    plt.show()


if __name__ == "__main__":
    environment = Environment(0)
    agent = Agent(environment)
    # Create all possible routes
    routes = environment.generateRoutes()
    # Rush hour from traffic Lights 
    routesFromTop = []  # Routes starting from light 0 or light 1
    routesFromBottom = []  # Routes starting from light 2 or light 3
    for route in routes:
        if route[0][0] in [0, 1]:
            routesFromTop.append(route)
        else:
            routesFromBottom.append(route)
    state_tracker = []

    #========================================================================#
    #                       ~   START SIMULATION   ~                         #
    #========================================================================#
    rewardHistory = []
    carsHistory = []
    for time in range(ENV_CONSTANTS["EPISODE_LENGTH"]):
        #print("Time step: {}".format(time))
        lightDirections = [
            "north/south" if light.directionIsNorthSouth
            else "east/west"
            for light in environment.lights
        ]
        #print("Directions for traffic lights: {}".format(lightDirections))
        environment.update(time,routes)
        #print(str(environment))
        #print("state: {}, cost: {}".format(environment.toState(time),environment.getCost(time)))
        rewardHistory.append(agent.update(time, environment))
        carsHistory.append(environment.getNumCars())
    plot(rewardHistory, carsHistory)
    

