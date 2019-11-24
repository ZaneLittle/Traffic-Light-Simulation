from Environment import Environment
from Agent import Agent
import numpy as np
from config import ENV_CONSTANTS
import math
import matplotlib.pyplot as plt

def plot(rewardHistory, carsHistory):
    tickSpacing = [ENV_CONSTANTS["EPISODE_LENGTH"]*day for day in range(ENV_CONSTANTS["NUM_DAYS"])]
    plt.subplot(2, 1, 1)
    rewardHistory = np.array(rewardHistory)*-1
    plt.plot(rewardHistory)
    plt.ylabel('Average Cost')
    plt.xticks(tickSpacing)
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    labelbottom=False) # labels along the bottom edge are off

    plt.subplot(2, 1, 2)
    plt.plot(carsHistory)
    plt.xlabel('time')
    plt.ylabel('Number of Cars')
    plt.xticks(tickSpacing,labels=["Day {}".format(day+1) for day in range(ENV_CONSTANTS["NUM_DAYS"])],rotation=45)
    plt.show()

def runSimulation(agent,environment):
    routes = environment.generateRoutes()
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
    encounteredStates = []
    numStatesEncountered = 0
    for day in range(ENV_CONSTANTS["NUM_DAYS"]):
        dayHistory =[]
        for time in range(ENV_CONSTANTS["EPISODE_LENGTH"]):
            time = time+(day*ENV_CONSTANTS["EPISODE_LENGTH"])
            environment.update(time,routes)
            dayHistory.append(agent.update(time, environment))
            carsHistory.append(environment.getNumCars())
        rewardHistory += dayHistory
        dayHistory = np.array(dayHistory)
        currentState = int(''.join(map(str, environment.toState())))
        print("Finished day {}, avg cost: {}, \% states encountered".format(day+1,np.mean(dayHistory), percentStates))
    plot(rewardHistory, carsHistory)


if __name__ == "__main__":
    environment = Environment(0)
    agent = Agent(environment)
    runSimulation(agent,environment)
    

