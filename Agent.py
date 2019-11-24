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
        self.numStates = (2**lights)*(discreteCosts**(2**(lights)))*numDayTime # Number of possible lights * traffic wait times * times of day
        self.numActions = numActions
        self.qTable = np.zeros((self.numStates, self.numActions))
        self.actionMap = self.generateActionMap()


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


    def update(self, time, env):
        ''' 
        Update for given time step 
        Return reward ratio based on number of cars in the environment
        '''
        # Retrieve e-greedy action and take it
        oldState = env.toState(time)
        actionIndex = self.eGreedy(oldState)
        action = self.actionMap[actionIndex]
        reward = 0
        for newLightDir, oldLightDir, i in zip(action, oldState[:4], range(0,4)): 
            if not newLightDir is oldLightDir:
                # print("toggling light {}".format(env.lights[i])) # debug
                env.lights[i].changeLight(time) 
                reward += env.lightChangeCost

        # Get indices
        newState = env.toState(time)
        newStateQind = self.stateToQind(newState)
        qind = self.stateToQind(oldState)
        greedyNext = np.max(self.qTable[newStateQind])
        oldVal = self.qTable[qind][actionIndex]

        reward -= env.getCost(time)

        # Update Q table
        self.qTable[qind][actionIndex] = self.lr * (reward + self.discount * greedyNext - oldVal)
        
        
        numCars = env.getNumCars()
        # print("time: {} \t reward: {} \t num cars: {}".format(time, reward, numCars)) # debug
            
        if numCars:
            return reward/numCars
        else:
            return 0
