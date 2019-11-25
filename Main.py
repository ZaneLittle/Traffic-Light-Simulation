from Environment import Environment
from Agent import Agent
import numpy as np
from config import ENV_CONSTANTS
import json
import os
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
    for year in range(ENV_CONSTANTS["NUM_YEARS"]):
        yearHistory = []
        for day in range(ENV_CONSTANTS["NUM_DAYS"]):
            environment = Environment(0)
            agent.environment = environment
            previousWaitTime = 0
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
                # print(previousWaitTime,waitTimes)
                agent.updateQTable(state,newState,action,waitTimeDelta=previousWaitTime-waitTimes)
                previousWaitTime = waitTimes
                stateTracker.add(str(state))
                yearHistory.append(waitTimes)
                carsHistory.append(environment.getNumCars())
            rewardHistory += yearHistory
        yearHistory = np.array(yearHistory)
        print("Finished year {},  \tavg cost: {:.4f}".format(year+1,np.mean(yearHistory)))
        percVisited = (len(stateTracker)/agent.numStates)*100
        print("\t-> states visisted: {}, % visited: {:.4f}%".format(len(stateTracker),percVisited))
    return rewardHistory, carsHistory

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def saveQTable(qTable,name):
    filePath = "qTables/{}.json".format(name)
    print("model => {}".format(filePath))
    if not os.path.exists(os.path.dirname(filePath)):
        try:
            os.makedirs(os.path.dirname(filePath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    test = json.dumps(qTable,sort_keys=True, indent=4,cls=NumpyEncoder)
    # Write-Overwrites 
    file1 = open(filePath,"w")#write mode 
    file1.write(test) 
    file1.close() 


if __name__ == "__main__":
    environment = Environment(0)
    agent = Agent(environment)
    rewardHistory, carsHistory = runSimulation(environment,agent,True)
    saveQTable(agent.qTable,"50YearQTable")
    


