from Environment import Environment
from Agent import Agent
import numpy as np
from config import ENV_CONSTANTS, CAR_CONSTS, FILES
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

def plotDays(rewardHistory,carsHistory, avgDailyWaitTimes):
    _, ax = plt.subplots()
    episodeLength = ENV_CONSTANTS["EPISODE_LENGTH"]
    rewardHistory,carsHistory = np.array(rewardHistory),np.array(carsHistory)
    dailyAverage = np.mean(rewardHistory.reshape(-1, episodeLength), axis=1)
    dailyCars = np.mean(carsHistory.reshape(-1, episodeLength), axis=1)


    plt.subplot(3, 1, 1)
    plt.title('Daily Averages')
    plt.plot(dailyAverage)
    plt.ylabel('Wait Time/Day')
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    labelbottom=False) # labels along the bottom edge are off

    plt.subplot(3, 1, 2)
    plt.plot(dailyCars)
    plt.ylabel('Number of Cars')

    plt.subplot(3, 1, 3)
    plt.plot(avgDailyWaitTimes)
    plt.ylabel('Travel Time')
   
    ymin, ymax = ax.get_ylim()
    plt.xlabel('Day (600 timesteps each)')
    plt.show()

def plotCulminativeCO2(culminativeCO2):
    plt.plot(culminativeCO2)
    plt.title('Culminative CO2 (kg)')
    plt.ylabel('CO2 Emitted (kg)')
    plt.xlabel('Day')
    plt.show()

def culminativeCO2(travelTimes):
    return np.cumsum([x * CAR_CONSTS["CO2_PER_TICK"] for x in travelTimes])

def runSimulation(environment,agent,resetOnDay=True, loadFile=None, saveFile=None):
    routes = environment.generateRoutes()

    #========================================================================#
    #                       ~   START SIMULATION   ~                         #
    #========================================================================#
    stateTracker = set()
    carsHistory = []
    waitTimeList = []
    avgTravelTimes = [] # average travel times by separated day
    print("Starting simulation. Num epochs {}".format(ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]))
    for year in range(ENV_CONSTANTS["NUM_YEARS"]):
        yearHistory = []
        for day in range(ENV_CONSTANTS["NUM_DAYS"]):
            environment = Environment(0)
            agent.environment = environment
            previousWaitTime = 0
            dayTravels = []
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
                waitTimes, travels = environment.update(time,routes)
                waitTimeList.append(waitTimes)
                dayTravels += travels
                newState = environment.toState(time+1)
                agent.updateQTable(state,newState,action,waitTimeDelta=previousWaitTime-waitTimes)
                previousWaitTime = waitTimes
                stateTracker.add(str(state))
                yearHistory.append(waitTimes)
                carsHistory.append(environment.getNumCars())
            dayTravels += environment.getCarTravelDuration(ENV_CONSTANTS["EPISODE_LENGTH"]) # get the rest of the waits in the environment
            avgTravelTimes.append(sum(dayTravels)/len(dayTravels)) # Add average of the day's travels 
        yearHistory = np.array(yearHistory)
        print("Finished year {},  \tavg cost: {:.4f}".format(year+1,np.mean(yearHistory)))
        saveFile()
        percVisited = (len(stateTracker)/agent.numStates)*100
        print("\t-> states visisted: {}, % visited: {:.4f}%".format(len(stateTracker),percVisited))
        # print("\t-> travel times: {}".format(avgTravelTimes))
    return waitTimeList, carsHistory, avgTravelTimes

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def saveQTable(qTable,filePath):
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
    saveFileName = FILES["SAVE_FILE"]
    if input("Save qTable to file {}? (yes/no) ".format(saveFileName))[0].lower() != "y":
        print("Aborting simulation. Change save file in config.py")
        exit
    saveFileFunction = lambda: saveQTable(agent.qTable,saveFileName)
    continueTraining = False
    if input("Continue training from file {}? (yes/no) ".format(FILES["LOAD_FILE"]))[0].lower() == "y":
        continueTraining = True
    else:
        print("Training from scratch")
    agent = Agent(environment, continueTraining=continueTraining)
    rewardHistory, carsHistory, avgDailyWaitTimes = runSimulation(environment,agent,True, saveFile=saveFileFunction)
    assert(len(rewardHistory) == ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]*ENV_CONSTANTS["EPISODE_LENGTH"]),"{},{}".format(len(rewardHistory),ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]*ENV_CONSTANTS["EPISODE_LENGTH"])
    plotDays(rewardHistory, carsHistory, avgDailyWaitTimes)
    plotCulminativeCO2(culminativeCO2(avgDailyWaitTimes))
    saveFileFunction()
    


