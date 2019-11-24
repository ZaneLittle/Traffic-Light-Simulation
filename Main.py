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

def plotDays(rewardHistory,carsHistory):
    _, ax = plt.subplots()
    episodeLength = ENV_CONSTANTS["EPISODE_LENGTH"]
    rewardHistory,carsHistory = np.array(rewardHistory),np.array(carsHistory)
    dailyAverage = np.mean(rewardHistory.reshape(-1, episodeLength), axis=1)*-1
    dailyCars = np.mean(carsHistory.reshape(-1, episodeLength), axis=1)

    assert(dailyAverage.shape[0] == ENV_CONSTANTS["NUM_DAYS"] )
    plt.subplot(2, 1, 1)
    plt.plot(dailyAverage)
    plt.ylabel('Average Cost/Day')
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    labelbottom=False) # labels along the bottom edge are off

    plt.subplot(2, 1, 2)
    ymin, ymax = ax.get_ylim()
    plt.plot(dailyCars)
    plt.xlabel('time')
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
        if resetOnDay: 
            environment = Environment(0)
            agent.environment = environment
        for time in range(ENV_CONSTANTS["EPISODE_LENGTH"]):
            if not resetOnDay:
                time = time+(day*ENV_CONSTANTS["EPISODE_LENGTH"]) # keep continuous time going
            environment.update(time,routes)
            qInd = agent.stateToQind(environment.toState(time))
            stateTracker.add(qInd)
            dayHistory.append(agent.update(time, environment))
            carsHistory.append(environment.getNumCars())
        rewardHistory += dayHistory
        dayHistory = np.array(dayHistory)
        print("Finished day {}, avg cost: {}".format(day+1,np.mean(dayHistory)))
        percVisited = (len(stateTracker)/agent.qTable.shape[0])*100
        print("\t-> states visisted: {}, % visited: {:.4f}%".format(len(stateTracker),percVisited))
    return rewardHistory, carsHistory


if __name__ == "__main__":
    environment = Environment(0)
    agent = Agent(environment)
    rewardHistory, carsHistory = runSimulation(environment,agent,False)
    plotDays(rewardHistory,carsHistory)

