import random
import numpy as np

class Agent:

    def __init__(self, environment, discount=0.5, epsilon=0.01, lr=0.9 ,lights=4, discreteCosts=3, numCctions=16, numDayTime=5):
        ''' 
        init as equiprobable
        the policy for each light is represented as an index of the policy array
        p[a|s]

        State representation:
            [
                L1Direction,...,L4Direction,
                f(L1CulmTime(N/S)),f(L1CulmTime(E/W)),...,f(L4CulmTime(N/S)),f(L4CulmTime(E/W))
            ]
        '''
        self.discount = discount
        self.epsilon = epsilon
        self.lr = lr
        self.environment = environment
        self.numStates = (2**lights)*(discreteCosts**(2**(lights)))*numDayTime # Number of possible lights * traffic wait times * times of day
        self.numActions = numActions
        self.qTable = np.zeros((self.numStates, self.numActions))

        self.policy = [0.5, 0.5, 0.5, 0.5]
        # Parameter used to alter how long the naive lights stay on for before switching direction
        self.phaseTimeBound = 1
        # Time elapses since lights have last changed direction
        self.currentPhaseTime = 0


    def stateToQind(self, state):
        """
            returns the state based on the environment
            [
                L1Direction,...,L4Direction,
                f(L1CulmTime(N/S)),f(L1CulmTime(E/W)),...,f(L4CulmTime(N/S)),f(L4CulmTime(E/W)),
                timeOfDay
            ]
        """
        # Stores the number of possible values that a particular entry in state might have,
        # e.g. size_of_states[0] = 2 means that state[0] can take on one of only two possible values 
        sizeOfStates = [2]*4 # Four traffic lights
        sizeOfStates += [3]*8 # 8 queues
        sizeOfStates += [5]
        
        dotProduct = np.dot(vec1,vec) 

        index = state[11]* + state[12]
        


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

        return np.random.choice(np.arrange(len(policy)), p=policy)    


    def update(self, time, env=None):
        ''' update for given time step '''
        self.currentPhaseTime = self.currentPhaseTime + 1
        # For now, test with a naive, constant policy of light changing
        if not env:
            self.constantPolicy(time) 
        else:
            # Retrieve e-greedy action and take it
            oldState = env.mapEnvToState(time)
            action = self.eGreedy(oldState)
            reward = 0
            for newLighDir, oldLightDir, i in zip(action, oldState[:4], range(0,4)): 
                if newLightDir not oldLightDir:
                    env.lights(i).changeLight(time)        
                    reward -= 1
    
            # Get indecies
            S_qind = self.state_to_qind(new_state)
            qind = self.state_to_qind(old_state)
            greedy_next = np.max(self.q_table[S_qind])
            old_val = self.q_table[q_ind][action]

            reward -= self.env.getCost(time)

            # Update Q table
            self.q_table[q_ind][action] = self.lr * (reward + self.discount * greedy_next - old_val)


    def constant_policy(self, time):
        # If enough time has elapsed, change light direction
        if self.current_phase_time >= self.phase_time_bound:
            self.current_phase_time = 0
            for light in self.environment.lights:
                # Toggle light direction
                light.changeLight(time)


    def learning_policy(self, env):
        for i in range(len(self.policy)):
            if(random.random() > self.policy[i]):
                env.lights[i].direction = False
            else:
                env.lights[i].direction = False
