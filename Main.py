from Environment import Environment
from Agent import Agent
import numpy as np
from config import ENV_CONSTANTS, CAR_CONSTS, FILES
import json
import os
import math
import matplotlib.pyplot as plt

class Main():
    def __init__(self, visualizerCallback=None):
        self.environment = Environment(0)
        self.visualizerCallback = visualizerCallback
    
    def startSimulation(self):
        saveFileName = FILES["SAVE_FILE"]
        if input("Save qTable to SAVE_FILE: {}? (yes/no) ".format(saveFileName))[0].lower() != "y":
            print("Aborting simulation. Change SAVE_FILE in config.py")
            exit()
        
        continueTraining = False
        if input("Continue training from LOAD_FILE: {}? (yes/no) ".format(FILES["LOAD_FILE"]))[0].lower() == "y":
            continueTraining = True
        else:
            print("Training from scratch")
        
        self.agent = Agent(self.environment, continueTraining=continueTraining)
        saveFileFunction = lambda: self.saveQTable(self.agent.qTable,saveFileName)
        rewardHistory, carsHistory, avgDailyWaitTimes = self.runSimulation(self.agent,True, saveFile=saveFileFunction)
        assert(len(rewardHistory) == ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]*ENV_CONSTANTS["EPISODE_LENGTH"]),"{},{}".format(len(rewardHistory),ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]*ENV_CONSTANTS["EPISODE_LENGTH"])
        self.plotDays(rewardHistory, carsHistory, avgDailyWaitTimes)
        self.plotCulminativeCO2(culminativeCO2(avgDailyWaitTimes))
        
        saveFileFunction()

    def approxRollingAvg(self, avg, newCost):
        N = 30
        avg -= avg / N;
        avg += newCost / N;
        return avg;

    def plot(self, rewardHistory, carsHistory):
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
    
    def plotDays(self, rewardHistory,carsHistory, avgDailyWaitTimes):
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

    def plotCulminativeCO2(self, culminativeCO2):
        plt.plot(culminativeCO2)
        plt.title('Culminative CO2 (kg)')
        plt.ylabel('CO2 Emitted (kg)')
        plt.xlabel('Day')
        plt.show()

    def culminativeCO2(self, travelTimes):
        return np.cumsum([x * CAR_CONSTS["CO2_PER_TICK"] for x in travelTimes])

    def runSimulation(self, agent,resetOnDay=True, loadFile=None, saveFile=None):
        routes = self.environment.generateRoutes(loopy=True)

        #========================================================================#
        #                       ~   START SIMULATION   ~                         #
        #========================================================================#
        stateTracker = set()
        
        carsHistory = []
        waitTimeList = []
        avgTravelTimes = [] # average travel times by separated day
        print("Starting simulation. Num epochs {}".format(ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]))
        avg = 0
        for year in range(ENV_CONSTANTS["NUM_YEARS"]):
            sumWaitTime = 0
            yearHistory = []
            for day in range(ENV_CONSTANTS["NUM_DAYS"]):
                self.environment = Environment(0)
                agent.environment = self.environment
                dayTravels = []
                for time in range(ENV_CONSTANTS["EPISODE_LENGTH"]):
                    """
                    Steps 
                        1) Read in state
                        2) make a decision
                        3) observe reward -> environment.update()
                        4) update q table for old state using new reward.

                    """
                    state = self.environment.toState(time)
                    action = agent.updateLights(time)
                    waitTimes, travels = self.environment.update(time,routes)
                    sumWaitTime += waitTimes
                    waitTimeList.append(waitTimes)
                    dayTravels += travels
                    newState = self.environment.toState(time+1)
                    stateIsNew = agent.updateQTable(state,newState,action,waitTime=waitTimes)
                    stateTracker.add(str(state))
                    yearHistory.append(waitTimes)
                    carsHistory.append(self.environment.getNumCars())
                    
                    avg = self.approxRollingAvg(avg, waitTimes)
                    if self.visualizerCallback is not None:
                        self.visualizerCallback(self.environment, time, stateIsNew, avg, self.environment.isRushHour)
                dayTravels += self.environment.getCarTravelDuration(ENV_CONSTANTS["EPISODE_LENGTH"]) # get the rest of the waits in the environment
                avgTravelTimes.append(sum(dayTravels)/len(dayTravels)) # Add average of the day's travels 
            yearHistory = np.array(yearHistory)
            print("Finished year {},  \tavg cost: {:.4f}".format(year+1,np.mean(yearHistory)))
            saveFile()
            percVisited = (len(stateTracker)/agent.numStates)*100
            print("\t-> states visisted: {}, % visited: {:.4f}%".format(len(stateTracker),percVisited))
            # print("\t-> travel times: {}".format(avgTravelTimes))
        return waitTimeList, carsHistory, avgTravelTimes

    def saveQTable(self, qTable,filePath):
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


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    main = Main()
    main.startSimulation()
    


