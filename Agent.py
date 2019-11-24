import random
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
        self.numStates = 541280
        print(self.numStates)
        self.numActions = numActions
        self.qTable = np.zeros((self.numStates, self.numActions))
        self.lightChangeCost = -1
        self.actionMap = self.generateActionMap()

        self.policy = [0.5, 0.5, 0.5, 0.5]
        # Parameter used to alter how long the naive lights stay on for before switching direction
        self.phaseTimeBound = 1
        # Time elapses since lights have last changed direction
        self.currentPhaseTime = 0

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

    def stateToQind(self, state):
        """
            Returns the index of a particular state for the Q-table. 
            Note the state variable is of the form:
            state = [
                L1Direction,...,L4Direction,
                f(L1CulmTime(N/S)),f(L1CulmTime(E/W)),...,f(L4CulmTime(N/S)),f(L4CulmTime(E/W)),
                timeOfDay
            ]
        """
        numStates = len(state)
        # Stores the number of possible values that a particular entry in state might have,
        # e.g. size_of_states[0] = 2 means that state[0] can take on one of only two possible values 
        sizeOfStates = [STATE_COSTANTS["LIGHTS"]["numStates"]] * STATE_COSTANTS["LIGHTS"]["quantity"]  
        sizeOfStates += [STATE_COSTANTS["QUEUES"]["numStates"]] * STATE_COSTANTS["QUEUES"]["quantity"]  
        sizeOfStates += [STATE_COSTANTS["TIME_OF_DAY"]["numStates"]] * STATE_COSTANTS["TIME_OF_DAY"]["quantity"]
        assert numStates == len(sizeOfStates)
        coeff = [0]*numStates
        coeff[-1] = 1
        for i in range(2,len(coeff)+1):
            coeff[-i] = coeff[-i+1]*sizeOfStates[-i+1]
        index = np.dot(np.array(state),np.array(coeff))

        return index


    def eGreedy(self, state):
        ''' 
        Return the e-greedy action for a given state
        '''
        policy = np.zeros(self.numActions)
        qind = self.stateToQind(state)
        
        if len(set(self.qTable[qind])) == 1:
            # If all the elements are equal, random walk
            policy = np.ones(self.numActions) / self.numActions
        else:
            policy = np.ones(self.numActions) * (self.epsilon / self.numActions)
            bestAction = np.argmax(self.qTable[qind])
            policy[bestAction] += 1.0 - self.epsilon

        return np.random.choice(np.arange(len(policy)), p=policy)    

    def greedy_action(self,time,env=None):
        state = env.toState(time)
        qInd = self.stateToQind(state)
        return np.max(self.qTable[qInd])

    def update(self, time, env=None):
        ''' 
        Update for given time step 
        Return reward ratio based on number of cars in the environment
        '''
        self.currentPhaseTime = self.currentPhaseTime + 1
        # For now, test with a naive, constant policy of light changing
        if not env:
            self.constantPolicy(time) 
            return None
        else:
            # Retrieve e-greedy action and take it
            oldState = env.toState(time)
            actionIndex = self.eGreedy(oldState)
            action = self.actionMap[actionIndex]
            reward = 0
            for newLightDir, oldLightDir, i in zip(action, oldState[:4], range(0,4)): 
                if not newLightDir is oldLightDir:
                    env.lights[i].changeLight(time) 
                    reward += self.lightChangeCost
    
            # Get indices
            newState = env.toState(time)
            newStateQind = self.stateToQind(newState)
            qind = self.stateToQind(oldState)
            try:
                greedyNext = np.max(self.qTable[newStateQind])
            except:
                print("Invalid state: {}, qInd: {}, maxQind: {}".format(newState,newStateQind,self.qTable.shape[0]))
            oldVal = self.qTable[qind][actionIndex]

            reward -= env.getCost(time)

            # Update Q table
            self.qTable[qind][actionIndex] = self.lr * (reward + self.discount * greedyNext - oldVal)
            
            
            numCars = env.getNumCars()
            # print("time: {} \t reward: {} \t num cars: {}".format(time, reward, numCars))
             
            if numCars:
                return reward/numCars
            else:
                return 0

    def constantPolicy(self, time):
        # If enough time has elapsed, change light direction
        if self.currentPhaseTime >= self.phaseTimeBound:
            self.currentPhaseTime = 0
            for light in self.environment.lights:
                # Toggle light direction
                light.changeLight(time)
