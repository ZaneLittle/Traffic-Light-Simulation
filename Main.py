from Environment import Environment
from Agent import Agent
import numpy as np
from config import ENV_CONSTANTS
import math
import matplotlib.pyplot as plt

def plot(rewardHistory, carsHistory):
    tickSpacing = [ENV_CONSTANTS["EPISODE_LENGTH"]*day for day in range(ENV_CONSTANTS["NUM_DAYS"])]
    plt.subplot(2, 1, 1)
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

def plotDays(rewardHistory,carsHistory):
    _, ax = plt.subplots()
    episodeLength = ENV_CONSTANTS["EPISODE_LENGTH"]
    rewardHistory,carsHistory = np.array(rewardHistory),np.array(carsHistory)
    dailyAverage = np.mean(rewardHistory.reshape(-1, episodeLength), axis=1)
    dailyCars = np.mean(carsHistory.reshape(-1, episodeLength), axis=1)

    assert(dailyAverage.shape[0] == ENV_CONSTANTS["NUM_DAYS"] )
    plt.subplot(2, 1, 1)
    plt.plot(dailyAverage)
    plt.ylabel('Average Wait Time/Day')
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    labelbottom=False) # labels along the bottom edge are off

    plt.subplot(2, 1, 2)
    ymin, ymax = ax.get_ylim()
    plt.plot(dailyCars)
    plt.xlabel('Day (600 timesteps each)')
    plt.ylabel('Avg NUmber of Cars')
   
    plt.show()

def runSimulation(environment,agent,resetOnDay=True):
    routes = environment.generateRoutes()

    #========================================================================#
    #                       ~   START SIMULATION   ~                         #
    #========================================================================#
    stateTracker = set()
    rewardHistory = []
    carsHistory = []
    for day in range(ENV_CONSTANTS["NUM_DAYS"]):
        dayHistory =[]
        environment = Environment(0)
        agent.environment = environment
        previousReward = 0
        for time in range(ENV_CONSTANTS["EPISODE_LENGTH"]):
            """
            Steps 
                1) Read in state
                2) make a decision
                3) observe reward -> environment.update()
                4) update q table for old state using new reward.

            """
            state = environment.toState(time)
            action = agent.updateLights(time)
            waitTimes = environment.update(time,routes)
            newState = environment.toState(time+1)
            agent.updateQTable(state,newState,action,waitTimes)
            stateTracker.add(str(state))
            dayHistory.append(waitTimes)
            carsHistory.append(environment.getNumCars())
        rewardHistory += dayHistory
        dayHistory = np.array(dayHistory)
        print("Finished day {},  \tavg cost: {:.4f}".format(day+1,np.mean(dayHistory)))
        percVisited = (len(stateTracker)/agent.numStates)*100
        print("\t-> states visisted: {}, % visited: {:.4f}%".format(len(stateTracker),percVisited))
    return rewardHistory, carsHistory


if __name__ == "__main__":
    environment = Environment(0)
    agent = Agent(environment)
    rewardHistory, carsHistory = runSimulation(environment,agent,True)
    plotDays(rewardHistory,carsHistory)
    # plot(rewardHistory,carsHistory)
    # rewardHistory, carsHistory = runSimulation(environment,agent,True)



