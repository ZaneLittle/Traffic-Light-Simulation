import random
import json
import numpy as np
from itertools import permutations
from config import STATE_COSTANTS

class Agent:

    def __init__(self, environment, discount=0.5, epsilon=0.01, lr=0.9 ,lights=4, discreteCosts=3, numActions=16, numDayTime=5):
        ''' 
        init as equiprobable
        the policy for each light is represented as an index of the policy array
        p[a|s]

        State representation:
            [
                L1Direction,...,L4Direction,
                f(L1CulmTime(N/S)),f(L1CulmTime(E/W)),...,f(L4CulmTime(N/S)),f(L4CulmTime(E/W)),
                timeOfDay
            ]
        '''
        self.discount = discount
        self.epsilon = epsilon
        self.lr = lr
        self.environment = environment
        self.numStates = (2**lights)*(discreteCosts**(2*lights))*numDayTime # Number of possible lights * traffic wait times * times of day
        self.numActions = numActions
        self.qTable = {}
        self.lightChangeCost = -1
        self.actionMap = self.generateActionMap()

        self.policy = [0.5, 0.5, 0.5, 0.5]
     
      
    def generateActionMap(self):
        lst = [0,0,0,0]
        actionMap = []
        for i in range(4):
            perms = set(permutations(lst))
            for action in perms:
                actionMap.append(action)
            lst[i] = 1
        actionMap.append(lst)
        return actionMap

    def qVal(self,state):
        """
            Returns the action values of a particular state for the Q-table. 
            Note the state variable is of the form:
            state = [
                L1Direction,...,L4Direction,
                f(L1CulmTime(N/S)),f(L1CulmTime(E/W)),...,f(L4CulmTime(N/S)),f(L4CulmTime(E/W)),
                timeOfDay
            ]
        """
        state = str(state)
        if state in self.qTable:
            return self.qTable[state]
        else:
            self.qTable[state] = np.zeros(self.numActions)
            return self.qTable[state]

    def eGreedy(self, state):
        ''' 
            Return the e-greedy action for a given state
        '''
        policy = np.zeros(self.numActions)
        actions = self.qVal(state)
        allEqual = actions == actions[0]
        if np.all(allEqual):
            # If all the elements are equal, random walk
            policy = np.ones(self.numActions) / self.numActions
        else:
            policy = np.ones(self.numActions) * (self.epsilon / self.numActions)
            bestAction = np.argmax(actions)
            policy[bestAction] += 1.0 - self.epsilon

        return np.random.choice(np.arange(len(policy)), p=policy)    

    def greedyAction(self,state):
        """
            state is defined in Environment.toState()

            Returns (column in the QTable with the highest value, that value)
        """
        actions = self.qVal(state)
        return np.argmax(actions), np.max(actions)

    def updateLights(self,time,greedy=False):
        """ 
            Update lights based on policy
            returns the "column" in the qtable that we updated
        """
        state = self.environment.toState(time)
        actionIndex = self.eGreedy(state)
        if greedy:
            actionIndex, _ = self.greedyAction(state)
        action = self.actionMap[actionIndex]
        for newLightDir, oldLightDir, i in zip(action, state[:4], range(0,4)): 
            if not newLightDir == oldLightDir:
                self.environment.lights[i].changeLight(time) 
        return actionIndex

    def updateQTable(self,previousState,newState,action,waitTimeDelta):
        newLights = self.actionMap[action]
        oldLights = previousState[:4]
        reward = waitTimeDelta
        for oldDirection,newDirection in zip(oldLights,newLights):
            if oldDirection != newDirection:
                r = reward
                reward+=self.lightChangeCost
        _ , greedyNext = self.greedyAction(newState)
        oldVal = self.qVal(previousState)[action]
        update = oldVal + self.lr * (reward + self.discount * greedyNext - oldVal)
        # assert(update <= 0),"update: {}, oldVal: {}, greedyNext: {}, reward: {}, wait time delta: {}".format(update,oldVal,greedyNext,reward,waitTimeDelta)
        self.__updateQTable(previousState,action,update)

    def __updateQTable(self,state,action,value):
        state = str(state)
        if not state in self.qTable:
            self.qTable[state] = np.zeros(self.numActions)
        self.qTable[state][action] = value
