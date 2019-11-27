from Environment import Environment
from Agent import Agent
from Graphing import * 
import numpy as np
from config import ENV_CONSTANTS, CAR_CONSTS, FILES
import copy
import json
import os
import math

class Main():
    def __init__(self, visualizerCallback=None):
        self.environment = Environment(0)
        self.visualizerCallback = visualizerCallback
    
    def startSimulation(self,route=None):
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
        rewardHistory, carsHistory, avgTravelTimes = self.runSimulation(self.agent,True, saveFile=saveFileFunction)
        assert(len(rewardHistory) == ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]*ENV_CONSTANTS["EPISODE_LENGTH"]),"{},{}".format(len(rewardHistory),ENV_CONSTANTS["NUM_YEARS"]*ENV_CONSTANTS["NUM_DAYS"]*ENV_CONSTANTS["EPISODE_LENGTH"])
        # plot(rewardHistory,carsHistory)
        # plotDays(rewardHistory, carsHistory, avgTravelTimes)
        # plotCulminativeCO2(avgTravelTimes)

        naiveRewards, naiveCarsHistory, naiveTravel = self.runSimulation(Agent(Environment(0)),True, saveFile=saveFileFunction,learn=False)
        plotCulminativeCO2(trainedTravelTimes=avgTravelTimes,naiveTravelTimes=naiveTravel)
        dualDailyPlot(rewardHistory,naiveRewards,carsHistory,naiveCarsHistory,avgTravelTimes,naiveTravel)

    def culminativeCO2(self, travelTimes):
        return np.cumsum([x * CAR_CONSTS["CO2_PER_TICK"] for x in travelTimes])

    def runSimulation(self, agent,resetOnDay=True, loadFile=None, saveFile=None,naive=False,learn=True):
        routes = self.environment.generateRoutes()

        #========================================================================#
        #                       ~   START SIMULATION   ~                         #
        #========================================================================#
        stateTracker = set(self.agent.qTable.keys())
        
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
                    if learn: _ = agent.updateQTable(state,newState,action,waitTime=waitTimes)
                    stateTracker.add(str(state))
                    yearHistory.append(waitTimes)
                    carsHistory.append(self.environment.getNumCars())
                    
                    avg = self.approxRollingAvg(avg, waitTimes)
                    if self.visualizerCallback is not None:
                        self.visualizerCallback(self.environment, time, False, avg, self.environment.isRushHour)
                dayTravels += self.environment.getCarTravelDuration(ENV_CONSTANTS["EPISODE_LENGTH"]) # get the rest of the waits in the environment
                avgTravelTimes.append(sum(dayTravels)/len(dayTravels)) # Add average of the day's travels 
            yearHistory = np.array(yearHistory)
            print("Finished year {},  \tavg cost: {:.4f}".format(year+1,np.mean(yearHistory)))
            percVisited = (len(stateTracker)/agent.numStates)*100
            print("\t-> states visisted: {}, % visited: {:.4f}%".format(len(stateTracker),percVisited))
            if learn: saveFile()
            # print("\t-> travel times: {}".format(avgTravelTimes))
        return waitTimeList, carsHistory, avgTravelTimes

    def saveQTable(self, qTable,filePath):
        print("\t-> model saved to {}".format(filePath))
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

    def approxRollingAvg(self, avg, newCost):
        N = 30
        avg -= avg / N
        avg += newCost / N
        return avg

    



class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    main = Main()
    main.startSimulation()
    


